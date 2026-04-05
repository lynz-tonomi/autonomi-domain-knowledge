#!/usr/bin/env python3
"""
BILL.com Approval Status Sync for Autonomi.

Polls BILL.com for approval status changes and syncs them back to
the Autonomi agent framework. This serves as a fallback/complement
to webhook-based notifications.

Uses the correct v3 endpoints:
  - GET /v3/bill-approvals/pending-user-approvals
  - GET /v3/bills/{billId} (with billApprovals=true)
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from bill_session import BillSession

logger = logging.getLogger("autonomi.approval_status_sync")

# Default poll interval (seconds)
DEFAULT_POLL_INTERVAL = 300  # 5 minutes


class ApprovalStatusSync:
    """Polls BILL.com for approval status changes and dispatches to agents.

    Maintains a persistent state file tracking:
      - Known bills and their last-seen approvalStatus
      - Per-approver status (WAITING, APPROVED, DENIED)
      - Stale bill detection (bills not updated within threshold)
    """

    def __init__(
        self,
        session: BillSession,
        state_path: str = "/tmp/bill_approval_sync_state.json",
        poll_interval: int = DEFAULT_POLL_INTERVAL,
        stale_threshold: int = 86400,  # 24 hours
    ):
        self.session = session
        self.state_path = Path(state_path)
        self.poll_interval = poll_interval
        self.stale_threshold = stale_threshold
        self.state: Dict[str, Any] = self._load_state()
        self.handlers: Dict[str, Callable] = {}

    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------
    def _load_state(self) -> Dict[str, Any]:
        if self.state_path.exists():
            try:
                return json.loads(self.state_path.read_text())
            except (json.JSONDecodeError, IOError):
                logger.warning("Corrupt state file, starting fresh")
        return {"bills": {}, "last_poll": 0}

    def _save_state(self):
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(self.state, indent=2))

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def on_status_change(self, event_type: str, handler: Callable):
        """Register a handler for approval status changes.

        event_type can be:
          - 'new_bill': Bill first seen in pending queue
          - 'status_changed': Bill approvalStatus changed
          - 'approver_acted': Individual approver status changed
          - 'stale_bill': Bill hasn't progressed within threshold
        """
        self.handlers[event_type] = handler

    def _dispatch(self, event_type: str, data: Dict[str, Any]):
        handler = self.handlers.get(event_type)
        if handler:
            try:
                handler(data)
            except Exception as e:
                logger.error(f"Handler error for {event_type}: {e}")

    # ------------------------------------------------------------------
    # Polling loop
    # ------------------------------------------------------------------
    def poll_once(self):
        """Run a single poll cycle: fetch pending approvals, detect changes."""
        logger.info("Polling for approval status changes...")

        # Get pending approvals for current user
        try:
            result = self.session.api_call_v3(
                "GET", "/v3/bill-approvals/pending-user-approvals"
            )
            pending_bills = result.get("bills", [])
        except Exception as e:
            logger.error(f"Failed to poll pending approvals: {e}")
            return

        current_bill_ids = set()
        now = time.time()

        for bill_summary in pending_bills:
            bill_id = bill_summary.get("billId", "")
            current_bill_ids.add(bill_id)

            # Fetch full bill details with approvals
            try:
                bill = self.session.api_call_v3(
                    "GET", f"/v3/bills/{bill_id}",
                    params={"billApprovals": "true"}
                )
            except Exception as e:
                logger.error(f"Failed to get bill {bill_id}: {e}")
                continue

            prev = self.state["bills"].get(bill_id)
            approval_status = bill.get("approvalStatus", "UNKNOWN")
            approvers = bill.get("approvers", [])

            if prev is None:
                # New bill in queue
                self._dispatch("new_bill", {
                    "bill_id": bill_id,
                    "vendor_id": bill.get("vendorId"),
                    "amount": bill.get("amount"),
                    "due_date": bill.get("dueDate"),
                    "approval_status": approval_status,
                    "approvers": approvers,
                })
                self.state["bills"][bill_id] = {
                    "approval_status": approval_status,
                    "approvers": {a["userId"]: a["status"] for a in approvers},
                    "first_seen": now,
                    "last_updated": now,
                }
            else:
                # Check for status changes
                if approval_status != prev.get("approval_status"):
                    self._dispatch("status_changed", {
                        "bill_id": bill_id,
                        "old_status": prev["approval_status"],
                        "new_status": approval_status,
                    })
                    self.state["bills"][bill_id]["approval_status"] = approval_status
                    self.state["bills"][bill_id]["last_updated"] = now

                # Check individual approver changes
                for approver in approvers:
                    uid = approver["userId"]
                    new_status = approver["status"]
                    old_status = prev.get("approvers", {}).get(uid)
                    if old_status and new_status != old_status:
                        self._dispatch("approver_acted", {
                            "bill_id": bill_id,
                            "user_id": uid,
                            "old_status": old_status,
                            "new_status": new_status,
                            "approver_order": approver.get("approverOrder"),
                        })
                        self.state["bills"][bill_id]["approvers"][uid] = new_status
                        self.state["bills"][bill_id]["last_updated"] = now

                # Check for stale bills
                age = now - prev.get("first_seen", now)
                if age > self.stale_threshold and approval_status in ("ASSIGNED",):
                    self._dispatch("stale_bill", {
                        "bill_id": bill_id,
                        "approval_status": approval_status,
                        "age_seconds": age,
                    })

        # Clean up bills no longer in pending queue
        removed = set(self.state["bills"].keys()) - current_bill_ids
        for bill_id in removed:
            logger.info(f"Bill {bill_id} no longer pending, removing from state")
            del self.state["bills"][bill_id]

        self.state["last_poll"] = now
        self._save_state()
        logger.info(f"Poll complete: {len(pending_bills)} pending, {len(removed)} resolved")

    def run(self, max_iterations: Optional[int] = None):
        """Run the polling loop.

        Args:
            max_iterations: Stop after N polls (None = run forever)
        """
        iteration = 0
        while max_iterations is None or iteration < max_iterations:
            self.poll_once()
            iteration += 1
            if max_iterations is None or iteration < max_iterations:
                time.sleep(self.poll_interval)

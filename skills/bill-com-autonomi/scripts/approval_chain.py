#!/usr/bin/env python3
"""
BILL.com Approval Chain Management for Autonomi Agents.

Provides functions for each step of the linear invoice approval workflow:
  Procurement -> Quality -> AP (with Settlement for exceptions)

All endpoints use the BILL v3 API with correct paths from official documentation:
  - POST /v3/bill-approvals          (create approval policy)
  - GET  /v3/bill-approvals/pending-user-approvals (get pending bills)
  - POST /v3/bill-approvals/actions   (approve/deny a bill)
  - POST /v3/bills                    (create bills)
  - GET  /v3/bills                    (list bills)
  - PATCH /v3/bills/{billId}          (update bill, apply vendor credits)
"""

import logging
from typing import Dict, List, Any, Optional
from bill_session import BillSession

logger = logging.getLogger("autonomi.approval_chain")


class ApprovalChain:
    """Manages the BILL.com bill approval workflow for Autonomi agents."""

    def __init__(self, session: BillSession):
        self.session = session

    # ------------------------------------------------------------------
    # Approval Policy Management
    # ------------------------------------------------------------------
    def create_approval_policy(
        self,
        policy_name: str,
        rules: List[Dict[str, Any]],
        approver_user_ids: List[str],
    ) -> Dict[str, Any]:
        """Create a bill approval policy.

        Args:
            policy_name: Human-readable policy name
            rules: List of rule objects, e.g.:
                [
                    {"key": "BILL_AMOUNT", "op": "gte", "values": ["1000"]},
                    {"key": "BILL_AMOUNT", "op": "lt", "values": ["5000"]},
                ]
            approver_user_ids: List of BILL user IDs (begin with '006')

        Returns:
            Policy response with id, status, rules, approvers
        """
        payload = {
            "policyName": policy_name,
            "rules": rules,
            "approvers": approver_user_ids,
        }
        result = self.session.api_call_v3("POST", "/v3/bill-approvals", payload)
        logger.info(f"Created approval policy: {result.get('id')} - {policy_name}")
        return result

    # ------------------------------------------------------------------
    # Pending Approvals
    # ------------------------------------------------------------------
    def get_pending_approvals(self) -> List[Dict[str, Any]]:
        """Get bills pending approval by the currently signed-in user.

        Returns list of bill summaries with billId, vendorId, amount, dueDate.
        Requires user to have Administrator, Accountant, or Approver role.
        """
        result = self.session.api_call_v3(
            "GET", "/v3/bill-approvals/pending-user-approvals"
        )
        bills = result.get("bills", [])
        logger.info(f"Found {len(bills)} bills pending approval")
        return bills

    # ------------------------------------------------------------------
    # Approve / Deny
    # ------------------------------------------------------------------
    def approve_bill(self, bill_id: str) -> bool:
        """Approve a bill for payment.

        Args:
            bill_id: BILL-generated bill ID (begins with '00n')

        Returns:
            True if approval succeeded (HTTP 200)
        """
        payload = {"billId": bill_id, "action": "APPROVE"}
        self.session.api_call_v3("POST", "/v3/bill-approvals/actions", payload)
        logger.info(f"Approved bill {bill_id}")
        return True

    def deny_bill(self, bill_id: str) -> bool:
        """Deny a bill.

        Args:
            bill_id: BILL-generated bill ID (begins with '00n')

        Returns:
            True if denial succeeded (HTTP 200)
        """
        payload = {"billId": bill_id, "action": "DENY"}
        self.session.api_call_v3("POST", "/v3/bill-approvals/actions", payload)
        logger.info(f"Denied bill {bill_id}")
        return True

    # ------------------------------------------------------------------
    # Bill Operations (Approval-Adjacent)
    # ------------------------------------------------------------------
    def get_bill(self, bill_id: str, include_approvals: bool = True) -> Dict[str, Any]:
        """Get a bill by ID, optionally including approval info.

        Args:
            bill_id: BILL-generated bill ID (begins with '00n')
            include_approvals: If True, includes approvers array in response
        """
        params = {}
        if include_approvals:
            params["billApprovals"] = "true"
        return self.session.api_call_v3("GET", f"/v3/bills/{bill_id}", params=params)

    def get_unassigned_bills(self) -> List[Dict[str, Any]]:
        """Get bills with approvalStatus = UNASSIGNED.

        These are bills that haven't been matched to an approval policy yet,
        or bills that don't match any active policy.
        """
        # List bills filtering by approval status
        # Note: exact filter syntax depends on BILL API list capabilities
        result = self.session.api_call_v3("GET", "/v3/bills", params={
            "billApprovals": "true"
        })
        bills = result if isinstance(result, list) else result.get("data", [])
        return [b for b in bills if b.get("approvalStatus") == "UNASSIGNED"]

    def create_bill(
        self,
        vendor_id: str,
        due_date: str,
        line_items: List[Dict[str, Any]],
        invoice_number: Optional[str] = None,
        invoice_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new bill.

        Args:
            vendor_id: BILL vendor ID (begins with '009')
            due_date: Due date in yyyy-MM-dd format
            line_items: List of dicts with 'amount' and optional 'description'
            invoice_number: Optional invoice number
            invoice_date: Optional invoice date in yyyy-MM-dd format
        """
        payload = {
            "vendorId": vendor_id,
            "dueDate": due_date,
            "billLineItems": line_items,
        }
        if invoice_number or invoice_date:
            payload["invoice"] = {}
            if invoice_number:
                payload["invoice"]["invoiceNumber"] = invoice_number
            if invoice_date:
                payload["invoice"]["invoiceDate"] = invoice_date

        result = self.session.api_call_v3("POST", "/v3/bills", payload)
        logger.info(f"Created bill {result.get('id')} for vendor {vendor_id}")
        return result

    def create_bills_bulk(self, bills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create multiple bills in one request (all-or-nothing).

        Args:
            bills: List of bill objects (same schema as single bill creation)

        Returns:
            List of created bill objects

        Raises:
            RuntimeError on BDC_1205 (invalid ID) or BDC_1246 (rollback)
        """
        result = self.session.api_call_v3("POST", "/v3/bills/bulk", bills)
        count = len(result) if isinstance(result, list) else 0
        logger.info(f"Bulk created {count} bills")
        return result if isinstance(result, list) else [result]

    def apply_vendor_credit_to_bill(
        self, bill_id: str, vendor_credit_id: str, amount: float
    ) -> Dict[str, Any]:
        """Apply a vendor credit to a bill.

        Args:
            bill_id: BILL bill ID (begins with '00n')
            vendor_credit_id: Vendor credit ID (begins with 'vcr')
            amount: Credit amount to apply
        """
        payload = {
            "vendorCredits": [{"id": vendor_credit_id, "amount": amount}]
        }
        result = self.session.api_call_v3("PATCH", f"/v3/bills/{bill_id}", payload)
        logger.info(f"Applied credit {vendor_credit_id} (${amount}) to bill {bill_id}")
        return result

    # ------------------------------------------------------------------
    # Escalation
    # ------------------------------------------------------------------
    def escalate_bill(self, bill_id: str, reason: str) -> Dict[str, str]:
        """Flag a bill for Settlement Agent review.

        This is an Autonomi-internal operation — it logs the escalation
        and returns metadata for the Settlement Agent to pick up.
        BILL.com itself doesn't have an escalation endpoint.

        Args:
            bill_id: Bill to escalate
            reason: Human-readable reason for escalation
        """
        logger.warning(f"Escalating bill {bill_id}: {reason}")
        return {
            "bill_id": bill_id,
            "reason": reason,
            "status": "escalated",
            "assigned_to": "settlement_agent",
        }

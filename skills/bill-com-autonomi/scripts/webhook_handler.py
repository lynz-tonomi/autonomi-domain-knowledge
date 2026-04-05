#!/usr/bin/env python3
"""
BILL.com Webhook Handler for Autonomi Agents.

Processes incoming BILL.com webhook events, verifies signatures,
and dispatches to the appropriate Autonomi agent based on event type.

Webhook base URLs (from official BILL.com documentation):
  Sandbox:    https://gateway.stage.bill.com/connect-events
  Production: https://gateway.prod.bill.com/connect-events

Header requirements for subscriptions:
  Org-level AP & AR events:      devKey + sessionId
  Partner-level AP & AR events:  appKey + sessionId
  Spend & Expense events:        apiToken

Subscription creation requires X-Idempotent-Key header (UUID4 format).

Official BILL.com webhook events:
  Vendor:           vendor.created, vendor.updated, vendor.archived, vendor.restored
  Vendor Auto-pay:  autopay.failed
  AP Bill:          bill.created, bill.updated, bill.archived, bill.restored
  AP Payment:       payment.updated, payment.failed
  Bank Account:     bank-account.created, bank-account.updated
  Card Account:     card-account.created, card-account.updated
  AR Invoice:       invoice.created, invoice.updated, invoice.archived, invoice.restored
  Risk:             risk-verification.updated
  S&E Transaction:  spend.transaction.updated
  S&E Reimbursement: spend.reimbursement.created/updated/deleted
  S&E 3DS:          spend.three-ds-challenge.created
"""

import hmac
import hashlib
import json
import logging
import uuid
from typing import Dict, Any, Callable, List, Optional
from bill_session import BillSession

logger = logging.getLogger("autonomi.webhook_handler")

# Events relevant to the approval workflow
APPROVAL_EVENTS = {
    "bill.created",
    "bill.updated",
    "bill.archived",
    "bill.restored",
    "payment.updated",
    "payment.failed",
    "vendor.created",
    "vendor.updated",
}


class BillWebhookHandler:
    """Handles incoming BILL.com webhook notifications.

    Routes events to registered agent handlers and manages
    webhook subscriptions via the BILL v3 API.
    """

    def __init__(self, session: BillSession, webhook_secret: Optional[str] = None):
        self.session = session
        self.webhook_secret = webhook_secret
        self.handlers: Dict[str, List[Callable]] = {}

    # ------------------------------------------------------------------
    # Subscription management
    # ------------------------------------------------------------------
    def create_subscription(
        self,
        events: List[str],
        notification_url: str,
        scope: str = "org",
    ) -> Dict[str, Any]:
        """Create a webhook subscription for the given events.

        Args:
            events: List of event types to subscribe to
            notification_url: URL where BILL sends notifications
            scope: 'org' (AP/AR org-level) or 'partner' (partner-level)

        Returns:
            Subscription response from BILL
        """
        # Subscriptions use the webhook base URL
        idempotent_key = str(uuid.uuid4())

        payload = {
            "events": events,
            "notificationUrl": notification_url,
        }

        # Build headers based on scope
        headers = {
            "Content-Type": "application/json",
            "X-Idempotent-Key": idempotent_key,
        }

        if scope == "org":
            headers["devKey"] = self.session.dev_key
            headers["sessionId"] = self.session.ensure_session()
        elif scope == "partner":
            # Partner scope uses appKey instead of devKey
            headers["appKey"] = self.session.dev_key
            headers["sessionId"] = self.session.ensure_session()

        # Note: For S&E events, use apiToken header instead

        import requests
        url = f"{self.session.webhook_base}/v3/subscriptions"
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()

        result = resp.json()
        logger.info(f"Created webhook subscription for {len(events)} events")
        return result

    def subscribe_approval_events(self, notification_url: str) -> Dict[str, Any]:
        """Convenience method: subscribe to all approval-relevant events."""
        return self.create_subscription(
            events=list(APPROVAL_EVENTS),
            notification_url=notification_url,
        )

    # ------------------------------------------------------------------
    # Event handler registration
    # ------------------------------------------------------------------
    def on(self, event_type: str, handler: Callable):
        """Register a handler for a specific event type.

        Multiple handlers can be registered for the same event.

        Args:
            event_type: BILL event type (e.g., 'bill.created')
            handler: Callable that receives the event payload dict
        """
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    # ------------------------------------------------------------------
    # Signature verification
    # ------------------------------------------------------------------
    def verify_signature(self, payload_bytes: bytes, signature: str) -> bool:
        """Verify the HMAC signature of an incoming webhook payload.

        Args:
            payload_bytes: Raw request body
            signature: Signature from the webhook header

        Returns:
            True if signature is valid
        """
        if not self.webhook_secret:
            logger.warning("No webhook secret configured, skipping verification")
            return True

        expected = hmac.new(
            self.webhook_secret.encode(),
            payload_bytes,
            hashlib.sha256,
        ).hexdigest()

        return hmac.compare_digest(expected, signature)

    # ------------------------------------------------------------------
    # Event processing
    # ------------------------------------------------------------------
    def process_event(self, payload: Dict[str, Any], signature: Optional[str] = None) -> bool:
        """Process an incoming webhook event.

        Args:
            payload: Parsed JSON payload from the webhook
            signature: Optional HMAC signature for verification

        Returns:
            True if event was processed successfully
        """
        # Verify signature if provided
        if signature and not self.verify_signature(
            json.dumps(payload).encode(), signature
        ):
            logger.error("Invalid webhook signature, rejecting event")
            return False

        event_type = payload.get("event", payload.get("eventType", ""))
        if not event_type:
            logger.warning(f"Webhook payload missing event type: {payload.keys()}")
            return False

        logger.info(f"Processing webhook event: {event_type}")

        # Dispatch to registered handlers
        handlers = self.handlers.get(event_type, [])
        if not handlers:
            logger.debug(f"No handlers registered for {event_type}")
            return True

        success = True
        for handler in handlers:
            try:
                handler(payload)
            except Exception as e:
                logger.error(f"Handler error for {event_type}: {e}")
                success = False

        return success

    # ------------------------------------------------------------------
    # Agent dispatch helpers
    # ------------------------------------------------------------------
    def setup_approval_chain_handlers(
        self,
        on_bill_created: Optional[Callable] = None,
        on_bill_updated: Optional[Callable] = None,
        on_payment_updated: Optional[Callable] = None,
        on_payment_failed: Optional[Callable] = None,
    ):
        """Register handlers for the standard approval chain events.

        Args:
            on_bill_created: Handler for new bills (triggers Procurement Agent)
            on_bill_updated: Handler for bill status changes (triggers next approver)
            on_payment_updated: Handler for payment status tracking
            on_payment_failed: Handler for payment failures (triggers Settlement Agent)
        """
        if on_bill_created:
            self.on("bill.created", on_bill_created)
        if on_bill_updated:
            self.on("bill.updated", on_bill_updated)
        if on_payment_updated:
            self.on("payment.updated", on_payment_updated)
        if on_payment_failed:
            self.on("payment.failed", on_payment_failed)
        logger.info("Approval chain webhook handlers configured")


# ---------------------------------------------------------------------------
# Example: Flask/FastAPI webhook endpoint
# ---------------------------------------------------------------------------
def create_webhook_endpoint(handler: BillWebhookHandler):
    """Example function showing how to wire the handler to a web framework.

    In production, this would be a Flask route or FastAPI endpoint.
    """
    def webhook_receiver(request_body: bytes, headers: Dict[str, str]):
        signature = headers.get("X-Bill-Signature", "")
        payload = json.loads(request_body)
        handler.process_event(payload, signature)
        return {"status": "ok"}

    return webhook_receiver

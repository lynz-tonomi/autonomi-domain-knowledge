"""
QBO Webhook Event Processor for Autonomi

Receives QBO webhook payloads, validates HMAC signatures,
and routes entity change events to the appropriate Autonomi agents.

This script is designed to be called by the webhook endpoint handler.
The HTTP layer (Flask, FastAPI, etc.) is handled separately — this
module provides the processing logic.

Usage:
    from scripts.qbo_webhook_processor import process_webhook

    # In your HTTP handler:
    result = process_webhook(
        request_body=request.body,
        signature_header=request.headers["intuit-signature"],
        tenant_id="tenant_123",
    )
"""

import hashlib
import hmac
import base64
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logger = logging.getLogger("qbo_webhook")

# Agent routing map: entity name → responsible agent(s)
AGENT_ROUTING = {
    "Bill": ["ap"],
    "BillPayment": ["ap", "settlement"],
    "VendorCredit": ["ap"],
    "Vendor": ["procurement", "ap"],
    "Invoice": ["ar"],
    "Payment": ["ar", "settlement"],
    "CreditMemo": ["ar"],
    "Deposit": ["ar", "settlement"],
    "Customer": ["ar"],
    "Item": ["inventory"],
    "PurchaseOrder": ["procurement", "inventory"],
    "Purchase": ["procurement", "ap"],
    "SalesReceipt": ["ar"],
    "Estimate": ["ar"],
    "JournalEntry": ["finance"],
    "Account": ["finance"],
}


def validate_signature(
    request_body: bytes,
    signature_header: str,
    verifier_token: str,
) -> bool:
    """
    Validate the HMAC-SHA256 signature on a QBO webhook payload.

    Args:
        request_body: Raw request body bytes
        signature_header: Value of the intuit-signature HTTP header
        verifier_token: The verifier token from QBO app webhook configuration

    Returns:
        True if signature is valid, False otherwise
    """
    computed = hmac.new(
        verifier_token.encode("utf-8"),
        request_body,
        hashlib.sha256,
    ).digest()
    computed_b64 = base64.b64encode(computed).decode("utf-8")
    return hmac.compare_digest(computed_b64, signature_header)


def _load_verifier_token(
    tenant_id: str,
    credentials_base: str = "/sandbox/credentials",
) -> str:
    """Load the webhook verifier token for a tenant."""
    verifier_path = (
        Path(credentials_base) / f"tenant_{tenant_id}" / "qbo" / "webhook_verifier.txt"
    )
    if not verifier_path.exists():
        raise FileNotFoundError(
            f"Webhook verifier token not found for tenant {tenant_id}"
        )
    return verifier_path.read_text().strip()


def _log_event(
    tenant_id: str,
    realm_id: str,
    entity_name: str,
    entity_id: str,
    operation: str,
    state_base: str = "/sandbox/state",
):
    """Log a webhook event for CDC reconciliation."""
    log_path = Path(state_base) / f"tenant_{tenant_id}" / "qbo" / "webhook_logs"
    log_path.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc)
    log_entry = {
        "realm_id": realm_id,
        "entity_name": entity_name,
        "entity_id": entity_id,
        "operation": operation,
        "received_at": now.isoformat(),
    }

    # Append to daily log file
    date_str = now.strftime("%Y-%m-%d")
    log_file = log_path / f"{date_str}.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    # Update sync state processed_events
    sync_state_path = Path(state_base) / f"tenant_{tenant_id}" / "qbo" / "sync_state.json"
    if sync_state_path.exists():
        with open(sync_state_path) as f:
            sync_state = json.load(f)
        # We don't have SyncToken from the webhook, so use entity_id + timestamp
        event_key = f"{entity_name}:{entity_id}:webhook:{now.isoformat()}"
        sync_state["processed_events"][event_key] = now.isoformat()
        sync_state["last_webhook_received"] = now.isoformat()
        with open(sync_state_path, "w") as f:
            json.dump(sync_state, f, indent=2)


def process_webhook(
    request_body: bytes,
    signature_header: str,
    tenant_id: str,
    credentials_base: str = "/sandbox/credentials",
    state_base: str = "/sandbox/state",
) -> dict:
    """
    Process a QBO webhook payload.

    This should be called from your HTTP handler AFTER returning 200.
    (Remember: return 200 within 3 seconds, then process asynchronously.)

    Args:
        request_body: Raw HTTP request body
        signature_header: The intuit-signature header value
        tenant_id: Autonomi tenant ID
        credentials_base: Path to credential storage
        state_base: Path to state storage

    Returns:
        Processing summary with routed events
    """
    # Validate HMAC signature
    verifier_token = _load_verifier_token(tenant_id, credentials_base)
    if not validate_signature(request_body, signature_header, verifier_token):
        logger.warning(f"Invalid webhook signature for tenant {tenant_id}")
        return {"error": "invalid_signature", "events_processed": 0}

    # Parse payload
    try:
        payload = json.loads(request_body)
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in webhook payload for tenant {tenant_id}")
        return {"error": "invalid_json", "events_processed": 0}

    # Process each notification
    events_processed = 0
    routed_events = []

    for notification in payload.get("eventNotifications", []):
        realm_id = notification.get("realmId", "")
        data_change = notification.get("dataChangeEvent", {})

        for entity in data_change.get("entities", []):
            entity_name = entity.get("name", "")
            entity_id = entity.get("id", "")
            operation = entity.get("operation", "")
            last_updated = entity.get("lastUpdated", "")

            # Log the event
            _log_event(tenant_id, realm_id, entity_name, entity_id, operation, state_base)

            # Determine which agents should handle this
            target_agents = AGENT_ROUTING.get(entity_name, [])

            routed_events.append({
                "entity_name": entity_name,
                "entity_id": entity_id,
                "operation": operation,
                "last_updated": last_updated,
                "routed_to": target_agents,
            })

            logger.info(
                f"Webhook event: {operation} {entity_name}:{entity_id} "
                f"→ agents: {target_agents}"
            )
            events_processed += 1

    return {
        "events_processed": events_processed,
        "routed_events": routed_events,
    }

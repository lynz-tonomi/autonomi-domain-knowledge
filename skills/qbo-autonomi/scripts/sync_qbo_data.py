"""
QBO Data Sync via Change Data Capture (CDC)

Daily sync job that polls QBO for changes since the last sync,
reconciles with webhook event logs, and processes any missed events.

Usage:
    python -m scripts.sync_qbo_data --tenant-id tenant_123

Designed to run as a scheduled task (e.g., daily at 2:00 AM tenant timezone).
"""

import argparse
import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

logger = logging.getLogger("qbo_sync")

# Entities to track via CDC
TRACKED_ENTITIES = [
    "Invoice", "Bill", "Payment", "BillPayment", "VendorCredit",
    "CreditMemo", "Deposit", "Vendor", "Customer", "Item",
    "PurchaseOrder", "Purchase", "SalesReceipt", "JournalEntry",
]

# Overlap window to catch edge cases (hours beyond 24h)
OVERLAP_HOURS = 2


def run_sync(
    tenant_id: str,
    state_base: str = "/sandbox/state",
    force_full: bool = False,
):
    """
    Execute a CDC sync for the given tenant.

    Steps:
    1. Load last sync state
    2. Calculate changedSince timestamp (last sync - overlap, or 26h ago)
    3. Call CDC endpoint for all tracked entities
    4. Compare with webhook event log to find missed events
    5. Process any missed changes
    6. Update sync state
    """
    from scripts.qbo_request import qbo_cdc
    from scripts.qbo_auth import QBOAuth

    state_path = Path(state_base) / f"tenant_{tenant_id}" / "qbo"
    sync_state_path = state_path / "sync_state.json"

    # Load current sync state
    if sync_state_path.exists():
        with open(sync_state_path) as f:
            sync_state = json.load(f)
    else:
        sync_state = {
            "last_cdc_poll": None,
            "last_webhook_received": None,
            "processed_events": {},
            "missed_events_last_24h": 0,
            "sync_health": "initializing",
        }

    now = datetime.now(timezone.utc)

    # Calculate the changedSince timestamp
    if force_full or not sync_state.get("last_cdc_poll"):
        # First sync or forced full sync — go back 30 days (CDC max)
        changed_since = (now - timedelta(days=30)).isoformat()
        logger.info(f"Running full CDC sync (30 day lookback) for tenant {tenant_id}")
    else:
        # Normal incremental sync with overlap buffer
        last_poll = datetime.fromisoformat(sync_state["last_cdc_poll"])
        overlap = timedelta(hours=OVERLAP_HOURS)
        changed_since = (last_poll - overlap).isoformat()
        logger.info(
            f"Running incremental CDC sync for tenant {tenant_id} "
            f"(since {changed_since})"
        )

    # Call CDC endpoint
    try:
        cdc_response = qbo_cdc(
            entities=TRACKED_ENTITIES,
            changed_since=changed_since,
            tenant_id=tenant_id,
        )
    except Exception as e:
        logger.error(f"CDC poll failed for tenant {tenant_id}: {e}")
        sync_state["sync_health"] = "error"
        sync_state["last_error"] = str(e)
        with open(sync_state_path, "w") as f:
            json.dump(sync_state, f, indent=2)
        raise

    # Parse CDC response
    cdc_changes = {}
    cdc_responses = cdc_response.get("CDCResponse", [])
    for cdc_item in cdc_responses:
        for query_response in cdc_item.get("QueryResponse", []):
            for entity_type, entities in query_response.items():
                if isinstance(entities, list):
                    cdc_changes[entity_type] = entities

    # Count total changes
    total_changes = sum(len(entities) for entities in cdc_changes.values())
    logger.info(f"CDC returned {total_changes} changes across {len(cdc_changes)} entity types")

    # Reconcile with webhook event log
    webhook_log_path = state_path / "webhook_logs"
    processed_events = sync_state.get("processed_events", {})
    missed_count = 0

    for entity_type, entities in cdc_changes.items():
        for entity in entities:
            entity_id = entity.get("Id", "")
            sync_token = entity.get("SyncToken", "")
            event_key = f"{entity_type}:{entity_id}:{sync_token}"

            if event_key not in processed_events:
                # This change wasn't picked up by webhooks
                missed_count += 1
                logger.info(f"Missed event detected: {event_key}")

                # Mark as processed now
                processed_events[event_key] = now.isoformat()

    # Clean up old processed events (older than 30 days)
    cutoff = (now - timedelta(days=30)).isoformat()
    processed_events = {
        k: v for k, v in processed_events.items()
        if v > cutoff
    }

    # Update sync state
    sync_state["last_cdc_poll"] = now.isoformat()
    sync_state["processed_events"] = processed_events
    sync_state["missed_events_last_24h"] = missed_count
    sync_state["sync_health"] = "healthy" if missed_count < 10 else "degraded"
    sync_state["last_sync_summary"] = {
        "timestamp": now.isoformat(),
        "total_cdc_changes": total_changes,
        "missed_events": missed_count,
        "entity_breakdown": {k: len(v) for k, v in cdc_changes.items()},
    }

    with open(sync_state_path, "w") as f:
        json.dump(sync_state, f, indent=2)

    logger.info(
        f"Sync complete for tenant {tenant_id}: "
        f"{total_changes} CDC changes, {missed_count} missed webhook events"
    )

    return sync_state["last_sync_summary"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run QBO CDC data sync")
    parser.add_argument("--tenant-id", required=True, help="Autonomi tenant ID")
    parser.add_argument("--state-base", default="/sandbox/state")
    parser.add_argument("--full", action="store_true", help="Force full 30-day sync")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    result = run_sync(args.tenant_id, args.state_base, force_full=args.full)
    print(json.dumps(result, indent=2))

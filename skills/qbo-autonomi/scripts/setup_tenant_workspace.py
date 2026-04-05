"""
QBO Tenant Workspace Initialization for Autonomi

Sets up the directory structure and initial configuration for a new
tenant's QBO integration. Run once during tenant onboarding after
the OAuth authorization flow is complete.

Usage:
    python -m scripts.setup_tenant_workspace --tenant-id tenant_123
"""

import argparse
import json
import os
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger("qbo_setup")


def setup_workspace(
    tenant_id: str,
    credentials_base: str = "/sandbox/credentials",
    state_base: str = "/sandbox/state",
):
    """
    Initialize the full workspace for a tenant's QBO integration.

    Creates:
    - Credential directory structure (if not already present)
    - Sync state directory with initial state file
    - Webhook event log directory
    - Agent permission configuration
    """

    # Credential directory (should already exist from OAuth setup)
    cred_path = Path(credentials_base) / f"tenant_{tenant_id}" / "qbo"
    cred_path.mkdir(parents=True, exist_ok=True)

    # Sync state directory
    state_path = Path(state_base) / f"tenant_{tenant_id}" / "qbo"
    state_path.mkdir(parents=True, exist_ok=True)

    # Initialize sync state
    sync_state = {
        "last_cdc_poll": None,
        "last_webhook_received": None,
        "processed_events": {},
        "missed_events_last_24h": 0,
        "sync_health": "initializing",
        "initialized_at": datetime.now(timezone.utc).isoformat(),
    }
    sync_state_path = state_path / "sync_state.json"
    if not sync_state_path.exists():
        with open(sync_state_path, "w") as f:
            json.dump(sync_state, f, indent=2)
        logger.info(f"Created sync state for tenant {tenant_id}")

    # Webhook event log directory
    webhook_log_path = state_path / "webhook_logs"
    webhook_log_path.mkdir(exist_ok=True)

    # Agent permissions configuration
    permissions = {
        "tenant_id": tenant_id,
        "agents": {
            "procurement": {
                "read": ["Vendor", "Item", "PurchaseOrder", "Bill", "Purchase",
                         "Account", "Attachable", "Preferences", "CompanyInfo"],
                "write": ["Vendor", "Item", "PurchaseOrder", "Purchase"],
                "delete": [],
                "send": [],
            },
            "ap": {
                "read": ["Bill", "BillPayment", "VendorCredit", "Vendor", "Purchase",
                         "Item", "Account", "Attachable", "Preferences", "CompanyInfo"],
                "write": ["Bill", "BillPayment", "VendorCredit", "Vendor", "Purchase", "Attachable"],
                "delete": ["Bill"],
                "send": [],
            },
            "ar": {
                "read": ["Invoice", "Payment", "CreditMemo", "Deposit", "Customer",
                         "Estimate", "SalesReceipt", "Account", "Attachable",
                         "Preferences", "CompanyInfo"],
                "write": ["Invoice", "Payment", "CreditMemo", "Deposit", "Customer",
                          "Estimate", "SalesReceipt", "Attachable"],
                "delete": [],
                "send": ["Invoice", "Estimate"],
            },
            "inventory": {
                "read": ["Item", "PurchaseOrder", "Purchase", "Vendor", "Customer",
                         "Account", "Attachable", "Preferences", "CompanyInfo"],
                "write": ["Item", "PurchaseOrder"],
                "delete": [],
                "send": [],
            },
            "finance": {
                "read": ["*"],  # All entities including reports
                "write": ["Account", "JournalEntry"],
                "delete": [],
                "send": [],
            },
            "quality": {
                "read": ["Vendor", "Item", "Account", "Attachable",
                         "Preferences", "CompanyInfo"],
                "write": ["Attachable"],
                "delete": [],
                "send": [],
            },
            "settlement": {
                "read": ["BillPayment", "Deposit", "Payment", "Bill", "Invoice",
                         "VendorCredit", "CreditMemo", "Purchase", "Account",
                         "Attachable", "Preferences", "CompanyInfo"],
                "write": ["BillPayment", "Deposit", "Payment"],
                "delete": [],
                "send": [],
            },
            "lynz": {
                "read": ["*"],  # All entities for voice summaries
                "write": [],
                "delete": [],
                "send": [],
            },
        },
    }
    permissions_path = state_path / "agent_permissions.json"
    with open(permissions_path, "w") as f:
        json.dump(permissions, f, indent=2)
    logger.info(f"Created agent permissions for tenant {tenant_id}")

    # Verify QBO connection
    try:
        from scripts.qbo_auth import QBOAuth
        auth = QBOAuth(tenant_id=tenant_id, credentials_base=credentials_base)
        status = auth.check_connection()
        logger.info(
            f"QBO connection verified for tenant {tenant_id}: "
            f"realm={status['realm_id']}, env={status['environment']}"
        )

        # Update sync state to active
        sync_state["sync_health"] = "healthy"
        with open(sync_state_path, "w") as f:
            json.dump(sync_state, f, indent=2)

    except Exception as e:
        logger.warning(f"QBO connection not yet available for tenant {tenant_id}: {e}")
        logger.info("Workspace created but QBO connection needs to be established.")

    print(f"QBO workspace initialized for tenant {tenant_id}")
    print(f"  Credentials: {cred_path}")
    print(f"  State: {state_path}")
    print(f"  Webhook logs: {webhook_log_path}")
    print(f"  Permissions: {permissions_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize QBO tenant workspace")
    parser.add_argument("--tenant-id", required=True, help="Autonomi tenant ID")
    parser.add_argument("--credentials-base", default="/sandbox/credentials")
    parser.add_argument("--state-base", default="/sandbox/state")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    setup_workspace(args.tenant_id, args.credentials_base, args.state_base)

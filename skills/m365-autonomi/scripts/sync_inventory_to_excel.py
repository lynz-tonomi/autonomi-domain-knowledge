#!/usr/bin/env python3
"""
Sync Autonomi inventory data to an Excel workbook on SharePoint.
Reads from Autonomi's database and writes to the tenant's inventory tracker.

Usage:
    python sync_inventory_to_excel.py --tenant-id tenant_001 --config tenant_config.json
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
import msal
import requests


def get_token(tenant_id: str, client_id: str, key_path: str) -> str:
    """Acquire Graph API token."""
    with open(key_path) as f:
        private_key = f.read()
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential={"thumbprint": os.environ["M365_CERT_THUMBPRINT"], "private_key": private_key},
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" not in result:
        raise RuntimeError(f"Auth failed: {result.get('error_description')}")
    return result["access_token"]


def graph_request(method, url, headers, json_body=None, retries=3):
    """Graph API call with retry on 429."""
    for attempt in range(retries):
        resp = getattr(requests, method)(url, headers=headers, json=json_body)
        if resp.status_code == 429:
            time.sleep(int(resp.headers.get("Retry-After", 2 ** attempt)))
            continue
        resp.raise_for_status()
        return resp.json() if resp.content else None
    raise RuntimeError(f"Throttled after {retries} retries")


def fetch_inventory_data() -> list:
    """
    Fetch current inventory from Autonomi database.
    Replace this with actual DB query in production.
    """
    # Placeholder — in production, query Autonomi's inventory tables
    # e.g., SELECT product, lot_number, quantity, unit, status, location, supplier
    #        FROM inventory WHERE updated_at > last_sync_timestamp
    return [
        ["2026-03-20", "Mango Puree", "Lot-2847", 1200, "lbs", "QC-Passed", "Warehouse-A", "Tropical Fruits Co"],
        ["2026-03-20", "Citric Acid", "Lot-9921", 150, "lbs", "Released", "Warehouse-B", "Chemical Supply Inc"],
        ["2026-03-20", "Sugar (Organic)", "Lot-4455", 3000, "lbs", "Received", "Warehouse-A", "Organic Sugar Ltd"],
    ]


def sync_to_excel(drive_id: str, workbook_path: str, data: list, headers: dict):
    """Write inventory data to Excel workbook on SharePoint."""
    base = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/root:{workbook_path}:"

    # Create a persistent session for batched writes
    session = graph_request("post", f"{base}/workbook/createSession", headers, {"persistChanges": True})
    session_headers = {**headers, "workbook-session-id": session["id"]}

    try:
        # Try to append to existing table
        for row in data:
            graph_request(
                "post",
                f"{base}/workbook/tables/InventoryTable/rows/add",
                session_headers,
                {"values": [row]},
            )
            print(f"  Added row: {row[1]} / {row[2]}")

        # Update sync timestamp
        now = datetime.utcnow().isoformat() + "Z"
        graph_request(
            "patch",
            f"{base}/workbook/worksheets/Metadata/range(address='B1')",
            session_headers,
            {"values": [[now]]},
        )
        print(f"  Sync timestamp updated: {now}")

    finally:
        # Always close session
        requests.post(f"{base}/workbook/closeSession", headers=session_headers)


def main():
    parser = argparse.ArgumentParser(description="Sync Autonomi inventory to Excel on SharePoint")
    parser.add_argument("--tenant-id", required=True)
    parser.add_argument("--config", required=True, help="Path to tenant_config.json")
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    drive_id = config["drive_id"]
    root = config["root_folder_name"]
    workbook_path = f"/{root}/Agent-Reports/Performance-Dashboards/inventory-tracker.xlsx"

    cred_dir = f"/sandbox/credentials/tenant_{args.tenant_id}"
    token = get_token(os.environ["M365_TENANT_ID"], os.environ["M365_CLIENT_ID"], f"{cred_dir}/key.pem")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    print(f"Fetching inventory data for tenant {args.tenant_id}...")
    data = fetch_inventory_data()
    print(f"  {len(data)} records to sync")

    print(f"Syncing to Excel: {workbook_path}")
    sync_to_excel(drive_id, workbook_path, data, headers)
    print("Sync complete.")


if __name__ == "__main__":
    main()

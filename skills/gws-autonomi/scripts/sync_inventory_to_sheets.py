#!/usr/bin/env python3
"""
Sync Autonomi inventory data to a tenant's Google Sheets dashboard.
Supports full refresh and incremental append modes.

Usage:
    # Full refresh (clear and rewrite)
    python sync_inventory_to_sheets.py --sheet-id SHEET_ID --mode refresh --data inventory.json

    # Incremental append (add new rows)
    python sync_inventory_to_sheets.py --sheet-id SHEET_ID --mode append --data new_records.json
"""

import subprocess
import json
import sys
import argparse
from datetime import datetime


def run_gws(command: str) -> dict:
    """Run a gws CLI command and return parsed JSON output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return {}
    return json.loads(result.stdout) if result.stdout.strip() else {}


def format_inventory_rows(records: list) -> list:
    """Format inventory records as 2D array for Sheets."""
    rows = []
    for r in records:
        rows.append([
            r.get("date", datetime.now().strftime("%Y-%m-%d")),
            r.get("ingredient_name", ""),
            r.get("lot_number", ""),
            str(r.get("quantity", 0)),
            r.get("unit", "lbs"),
            r.get("status", "Unknown"),
            r.get("expiry_date", ""),
            r.get("supplier_name", ""),
        ])
    return rows


def refresh_sheet(sheet_id: str, data: list, sheet_name: str = "Inventory"):
    """Clear and rewrite the entire sheet."""
    range_str = f"{sheet_name}!A2:H10000"

    # Clear existing data
    run_gws(
        f"gws sheets spreadsheets values clear "
        f"--params '{{\"spreadsheetId\": \"{sheet_id}\", \"range\": \"{range_str}\"}}'"
    )

    rows = format_inventory_rows(data)
    if not rows:
        print("No data to write.")
        return

    # Write new data
    payload = json.dumps({
        "valueInputOption": "USER_ENTERED",
        "data": [{"range": f"{sheet_name}!A2:H{len(rows)+1}", "values": rows}]
    })

    run_gws(
        f"gws sheets spreadsheets values batchUpdate "
        f"--params '{{\"spreadsheetId\": \"{sheet_id}\"}}' "
        f"--json '{payload}'"
    )

    # Update last-synced timestamp
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    run_gws(
        f"gws sheets spreadsheets values update "
        f"--params '{{\"spreadsheetId\": \"{sheet_id}\", \"range\": \"{sheet_name}!J1\", \"valueInputOption\": \"USER_ENTERED\"}}' "
        f"--json '{{\"values\": [[\"Last synced: {ts}\"]]}}}'"
    )

    print(f"Refreshed {len(rows)} rows in {sheet_name}. Last synced: {ts}")


def append_rows(sheet_id: str, data: list, sheet_name: str = "Inventory"):
    """Append new rows to the sheet."""
    rows = format_inventory_rows(data)
    if not rows:
        print("No data to append.")
        return

    for row in rows:
        values = ",".join(row)
        run_gws(
            f"gws sheets +append --spreadsheet {sheet_id} --values \"{values}\""
        )

    print(f"Appended {len(rows)} rows to {sheet_name}.")


def main():
    parser = argparse.ArgumentParser(description="Sync inventory to Google Sheets")
    parser.add_argument("--sheet-id", required=True, help="Google Sheets spreadsheet ID")
    parser.add_argument("--mode", choices=["refresh", "append"], default="refresh")
    parser.add_argument("--data", required=True, help="Path to JSON data file")
    parser.add_argument("--sheet-name", default="Inventory", help="Tab name in spreadsheet")
    args = parser.parse_args()

    with open(args.data) as f:
        data = json.load(f)

    if args.mode == "refresh":
        refresh_sheet(args.sheet_id, data, args.sheet_name)
    else:
        append_rows(args.sheet_id, data, args.sheet_name)


if __name__ == "__main__":
    main()

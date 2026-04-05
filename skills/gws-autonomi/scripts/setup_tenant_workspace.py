#!/usr/bin/env python3
"""
Setup Google Drive folder structure for a new Autonomi tenant.
Creates the standard folder hierarchy and returns folder IDs for config.

Usage:
    python setup_tenant_workspace.py --tenant-name "Acme Beverages" --tenant-id tenant_001
"""

import subprocess
import json
import sys
import argparse


def run_gws(command: str) -> dict:
    """Run a gws CLI command and return parsed JSON output."""
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout) if result.stdout.strip() else {}


def create_folder(name: str, parent_id: str = None) -> str:
    """Create a Google Drive folder and return its ID."""
    metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent_id:
        metadata["parents"] = [parent_id]

    result = run_gws(
        f"gws drive files create --json '{json.dumps(metadata)}'"
    )
    folder_id = result.get("id", "")
    print(f"  Created: {name} ({folder_id})")
    return folder_id


def main():
    parser = argparse.ArgumentParser(description="Setup Autonomi tenant workspace in Google Drive")
    parser.add_argument("--tenant-name", required=True, help="Display name for the tenant")
    parser.add_argument("--tenant-id", required=True, help="Autonomi tenant ID")
    parser.add_argument("--output", default="tenant_config.json", help="Output config file path")
    args = parser.parse_args()

    print(f"Setting up workspace for: {args.tenant_name} ({args.tenant_id})")

    # Define folder structure
    structure = {
        "Procurement": ["Purchase-Orders", "Supplier-Contracts", "COAs", "Supplier-Scorecards"],
        "Quality": ["Batch-Reports", "Hold-Notices", "Lab-Results", "Audit-Documents"],
        "Production": ["Schedules", "Yield-Reports", "BOM-Exports"],
        "Compliance": ["FSMA-204", "Certifications", "Recall-Records", "Training-Records"],
        "Finance": ["Invoices", "Cost-Reports", "AP-AR-Exports"],
        "Agent-Reports": ["Decision-Logs", "Anomaly-Reports", "Performance-Dashboards"],
    }

    # Create root folder
    root_name = f"Autonomi-{args.tenant_name}"
    root_id = create_folder(root_name)

    # Build folder tree and collect IDs
    folder_ids = {"root": root_id}

    for section, subfolders in structure.items():
        section_id = create_folder(section, root_id)
        folder_ids[section.lower()] = section_id

        for subfolder in subfolders:
            sub_id = create_folder(subfolder, section_id)
            key = f"{section.lower()}/{subfolder.lower()}"
            folder_ids[key] = sub_id

    # Write config
    config = {
        "tenant_id": args.tenant_id,
        "tenant_name": args.tenant_name,
        "root_folder_name": root_name,
        "folder_ids": folder_ids,
    }

    with open(args.output, "w") as f:
        json.dump(config, f, indent=2)

    print(f"\nWorkspace created. Config saved to: {args.output}")
    print(f"Root folder: {root_name} ({root_id})")
    print(f"Total folders created: {len(folder_ids)}")


if __name__ == "__main__":
    main()

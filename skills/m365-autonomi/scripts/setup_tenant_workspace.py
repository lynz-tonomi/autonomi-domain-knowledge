#!/usr/bin/env python3
"""
Setup SharePoint folder structure for a new Autonomi tenant.
Creates the standard folder hierarchy and returns folder/drive IDs for config.

Usage:
    python setup_tenant_workspace.py --tenant-name "Acme Beverages" --tenant-id tenant_001
"""

import os
import sys
import json
import time
import argparse
import msal
import requests


def get_token(tenant_id: str, client_id: str, cert_path: str, key_path: str) -> str:
    """Acquire Graph API token using certificate auth."""
    with open(key_path) as f:
        private_key = f.read()

    app = msal.ConfidentialClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential={
            "thumbprint": os.environ.get("M365_CERT_THUMBPRINT", ""),
            "private_key": private_key,
        },
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" not in result:
        print(f"Auth failed: {result.get('error_description', 'Unknown')}", file=sys.stderr)
        sys.exit(1)
    return result["access_token"]


def graph_request(method: str, url: str, headers: dict, json_body=None, retries=3):
    """Make a Graph API request with retry."""
    for attempt in range(retries):
        resp = getattr(requests, method)(url, headers=headers, json=json_body)
        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", 2 ** attempt))
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json() if resp.content else {}
    raise RuntimeError(f"Throttled after {retries} retries: {url}")


def create_folder(drive_id: str, parent_path: str, name: str, headers: dict) -> dict:
    """Create a folder in SharePoint and return its metadata."""
    result = graph_request(
        "post",
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/root:{parent_path}:/children",
        headers,
        json_body={"name": name, "folder": {}, "@microsoft.graph.conflictBehavior": "fail"},
    )
    print(f"  Created: {parent_path}/{name} ({result.get('id', 'unknown')})")
    return result


def main():
    parser = argparse.ArgumentParser(description="Setup Autonomi tenant workspace in SharePoint")
    parser.add_argument("--tenant-name", required=True, help="Display name for the tenant")
    parser.add_argument("--tenant-id", required=True, help="Autonomi tenant ID")
    parser.add_argument("--site-url", required=True, help="SharePoint site URL (e.g., contoso.sharepoint.com:/sites/Autonomi)")
    parser.add_argument("--output", default="tenant_config.json", help="Output config file path")
    args = parser.parse_args()

    print(f"Setting up M365 workspace for: {args.tenant_name} ({args.tenant_id})")

    # Authenticate
    cred_dir = f"/sandbox/credentials/tenant_{args.tenant_id}"
    token = get_token(
        os.environ["M365_TENANT_ID"],
        os.environ["M365_CLIENT_ID"],
        f"{cred_dir}/cert.pem",
        f"{cred_dir}/key.pem",
    )
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Get site and drive
    site = graph_request("get", f"https://graph.microsoft.com/v1.0/sites/{args.site_url}", headers)
    site_id = site["id"]
    drive = graph_request("get", f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive", headers)
    drive_id = drive["id"]

    print(f"Site: {site.get('displayName')} | Drive: {drive_id}")

    # Define folder structure (mirrors the GWS skill structure)
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
    root = create_folder(drive_id, "", root_name, headers)
    root_path = f"/{root_name}"

    folder_ids = {"root": root["id"]}

    for section, subfolders in structure.items():
        section_result = create_folder(drive_id, root_path, section, headers)
        folder_ids[section.lower()] = section_result["id"]

        for subfolder in subfolders:
            sub_result = create_folder(drive_id, f"{root_path}/{section}", subfolder, headers)
            folder_ids[f"{section.lower()}/{subfolder.lower()}"] = sub_result["id"]

    # Write config
    config = {
        "tenant_id": args.tenant_id,
        "tenant_name": args.tenant_name,
        "platform": "microsoft365",
        "site_id": site_id,
        "drive_id": drive_id,
        "root_folder_name": root_name,
        "folder_ids": folder_ids,
    }

    with open(args.output, "w") as f:
        json.dump(config, f, indent=2)

    print(f"\nWorkspace created. Config saved to: {args.output}")
    print(f"Root folder: {root_name} ({root['id']})")
    print(f"Total folders created: {len(folder_ids)}")


if __name__ == "__main__":
    main()

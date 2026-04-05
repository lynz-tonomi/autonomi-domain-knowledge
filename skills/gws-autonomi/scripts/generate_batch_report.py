#!/usr/bin/env python3
"""
Generate a Google Docs batch quality report from Autonomi batch/lot data.
Creates a new Google Doc with structured QC results, traceability, and disposition.

Usage:
    python generate_batch_report.py --batch-data batch_2847.json --folder-id FOLDER_ID
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


def build_report_content(batch: dict) -> str:
    """Build markdown-style report content from batch data."""
    lot = batch.get("lot_number", "Unknown")
    product = batch.get("product_name", "Unknown")
    prod_date = batch.get("production_date", "Unknown")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""Batch Quality Report

Batch: {lot}
Product: {product}
Production Date: {prod_date}
Report Generated: {timestamp} by Quality Agent

TEST RESULTS SUMMARY

"""

    # Add test results
    tests = batch.get("test_results", [])
    for test in tests:
        name = test.get("test_name", "")
        result = test.get("result", "")
        spec_min = test.get("spec_min", "")
        spec_max = test.get("spec_max", "")
        status = test.get("status", "")
        content += f"  {name}: {result} (Spec: {spec_min}-{spec_max}) — {status}\n"

    content += "\n\nINGREDIENT LOT TRACEABILITY\n\n"

    # Add ingredient traceability
    ingredients = batch.get("ingredients", [])
    for ing in ingredients:
        content += (
            f"  {ing.get('name', '')}: "
            f"Lot {ing.get('lot_number', 'N/A')} | "
            f"Supplier: {ing.get('supplier', 'N/A')}\n"
        )

    # Disposition
    disposition = batch.get("disposition", "Pending Review")
    rationale = batch.get("rationale", "Awaiting QC lead review")
    content += f"\n\nDISPOSITION\n\nDecision: {disposition}\nRationale: {rationale}\n"

    return content


def main():
    parser = argparse.ArgumentParser(description="Generate batch QC report in Google Docs")
    parser.add_argument("--batch-data", required=True, help="Path to batch JSON data")
    parser.add_argument("--folder-id", required=True, help="Google Drive folder ID for report")
    args = parser.parse_args()

    with open(args.batch_data) as f:
        batch = json.load(f)

    lot = batch.get("lot_number", "Unknown")
    product = batch.get("product_name", "Unknown")
    title = f"Batch Report - {lot} - {product}"

    # Create Google Doc
    create_result = run_gws(
        f"gws docs documents create --json '{{\"title\": \"{title}\"}}'"
    )
    doc_id = create_result.get("documentId", "")
    if not doc_id:
        print("Failed to create document.", file=sys.stderr)
        sys.exit(1)

    print(f"Created document: {title} ({doc_id})")

    # Write content
    content = build_report_content(batch)
    escaped_content = content.replace("'", "\\'").replace('"', '\\"')

    run_gws(f'gws docs +write --document {doc_id} --text "{escaped_content}"')

    # Move to target folder
    run_gws(
        f"gws drive files update "
        f"--params '{{\"fileId\": \"{doc_id}\", \"addParents\": \"{args.folder_id}\"}}'"
    )

    print(f"Report saved to folder. Doc ID: {doc_id}")
    print(f"URL: https://docs.google.com/document/d/{doc_id}/edit")


if __name__ == "__main__":
    main()

"""
QBO Financial Report Generator for Autonomi

Pulls financial reports from QBO and formats them for tenant dashboards,
agent analysis, or voice summaries (LynZ).

Usage:
    python -m scripts.generate_financial_report \
        --tenant-id tenant_123 \
        --report profit-and-loss \
        --start-date 2025-03-01 \
        --end-date 2025-03-31 \
        --output /tmp/report.json

Available reports: profit-and-loss, balance-sheet, cash-flow, trial-balance,
    ap-aging, ar-aging, general-ledger
"""

import argparse
import json
import logging
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger("qbo_report")

REPORT_MAP = {
    "profit-and-loss": "ProfitAndLoss",
    "profit-and-loss-detail": "ProfitAndLossDetail",
    "balance-sheet": "BalanceSheet",
    "cash-flow": "CashFlow",
    "trial-balance": "TrialBalance",
    "general-ledger": "GeneralLedger",
    "ap-aging": "AgedPayables",
    "ap-aging-detail": "AgedPayableDetail",
    "ar-aging": "AgedReceivables",
    "ar-aging-detail": "AgedReceivableDetail",
    "transaction-list": "TransactionList",
}


def get_accounting_method(tenant_id: str) -> str:
    """Query the tenant's Preferences to determine Accrual vs Cash accounting."""
    from scripts.qbo_request import qbo_request
    from scripts.qbo_auth import QBOAuth

    auth = QBOAuth(tenant_id=tenant_id)
    realm_id = auth.realm_id

    prefs = qbo_request(
        "GET",
        f"/v3/company/{realm_id}/preferences",
        tenant_id=tenant_id,
    )

    # Extract accounting method from preferences
    accounting_info = prefs.get("QueryResponse", prefs)
    preferences = accounting_info.get("Preferences", accounting_info)
    report_prefs = preferences.get("ReportPrefs", {})
    method = report_prefs.get("ReportBasis", "Accrual")

    logger.info(f"Tenant {tenant_id} accounting method: {method}")
    return method


def generate_report(
    tenant_id: str,
    report_type: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    accounting_method: Optional[str] = None,
    extra_params: Optional[dict] = None,
) -> dict:
    """
    Generate a financial report from QBO.

    Args:
        tenant_id: Autonomi tenant ID
        report_type: Report key (e.g., "profit-and-loss", "balance-sheet")
        start_date: Period start (YYYY-MM-DD)
        end_date: Period end (YYYY-MM-DD)
        accounting_method: Override (otherwise queries Preferences)
        extra_params: Additional QBO report parameters

    Returns:
        Report data with metadata
    """
    from scripts.qbo_request import qbo_report

    # Resolve report name
    qbo_report_name = REPORT_MAP.get(report_type)
    if not qbo_report_name:
        raise ValueError(
            f"Unknown report type: {report_type}. "
            f"Available: {', '.join(REPORT_MAP.keys())}"
        )

    # Get accounting method if not provided
    if not accounting_method:
        try:
            accounting_method = get_accounting_method(tenant_id)
        except Exception as e:
            logger.warning(f"Could not determine accounting method: {e}. Defaulting to Accrual.")
            accounting_method = "Accrual"

    # Fetch report
    logger.info(
        f"Generating {report_type} report for tenant {tenant_id} "
        f"({start_date} to {end_date}, {accounting_method})"
    )

    report_data = qbo_report(
        report_name=qbo_report_name,
        tenant_id=tenant_id,
        start_date=start_date,
        end_date=end_date,
        accounting_method=accounting_method,
        extra_params=extra_params,
    )

    # Wrap with metadata
    result = {
        "metadata": {
            "tenant_id": tenant_id,
            "report_type": report_type,
            "qbo_report_name": qbo_report_name,
            "start_date": start_date,
            "end_date": end_date,
            "accounting_method": accounting_method,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "report": report_data,
    }

    return result


def format_for_voice(report_data: dict) -> str:
    """
    Format a financial report for LynZ voice output.

    Produces a concise, natural-language summary suitable for text-to-speech.
    Avoids raw numbers and JSON — everything is spoken-word friendly.
    """
    metadata = report_data.get("metadata", {})
    report = report_data.get("report", {})
    report_type = metadata.get("report_type", "financial report")

    # Extract header info
    header = report.get("Header", {})
    report_name = header.get("ReportName", report_type)
    start_date = header.get("StartPeriod", metadata.get("start_date", ""))
    end_date = header.get("EndPeriod", metadata.get("end_date", ""))

    summary_parts = [f"Here's a summary of your {report_name}"]
    if start_date and end_date:
        summary_parts.append(f"for the period {start_date} through {end_date}")
    summary_parts.append(".")

    # Parse rows for key totals (simplified — actual parsing depends on report structure)
    rows = report.get("Rows", {}).get("Row", [])
    totals = []
    for row in rows:
        if row.get("type") == "Section" and row.get("group") == "GrossProfit":
            # Try to extract gross profit
            summary_row = row.get("Summary", {})
            cols = summary_row.get("ColData", [])
            if len(cols) >= 2:
                totals.append(f"Gross profit is {cols[1].get('value', 'unavailable')}")

    if totals:
        summary_parts.append(" ".join(totals) + ".")
    else:
        summary_parts.append(
            "I've pulled the full report data. Would you like me to "
            "highlight specific line items or totals?"
        )

    return " ".join(summary_parts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate QBO financial report")
    parser.add_argument("--tenant-id", required=True)
    parser.add_argument("--report", required=True, choices=list(REPORT_MAP.keys()))
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--accounting-method", choices=["Accrual", "Cash"])
    parser.add_argument("--output", help="Output file path (default: stdout)")
    parser.add_argument("--voice", action="store_true", help="Format for LynZ voice output")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    result = generate_report(
        tenant_id=args.tenant_id,
        report_type=args.report,
        start_date=args.start_date,
        end_date=args.end_date,
        accounting_method=args.accounting_method,
    )

    if args.voice:
        output = format_for_voice(result)
    else:
        output = json.dumps(result, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report saved to {args.output}")
    else:
        print(output)

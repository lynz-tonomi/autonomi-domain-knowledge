#!/usr/bin/env python3
"""
Process incoming Outlook webhook notifications and route to appropriate Autonomi agent.
Designed to run as an Azure Function or standalone Flask/FastAPI endpoint.

Usage (standalone):
    python outlook_webhook_processor.py --port 8080

Usage (Azure Function):
    Deploy as HTTP-triggered function — see references/azure-integration.md
"""

import os
import sys
import json
import logging
import hmac
import hashlib
from datetime import datetime

import msal
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def get_token():
    """Acquire Graph API token for reading message details."""
    app = msal.ConfidentialClientApplication(
        os.environ["M365_CLIENT_ID"],
        authority=f"https://login.microsoftonline.com/{os.environ['M365_TENANT_ID']}",
        client_credential=os.environ.get("M365_CLIENT_SECRET", ""),
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" not in result:
        raise RuntimeError(f"Auth failed: {result.get('error_description')}")
    return result["access_token"]


def validate_notification(notification: dict) -> bool:
    """Validate that a notification is genuine using clientState."""
    expected = os.environ.get("WEBHOOK_SECRET", "")
    return notification.get("clientState") == expected


def get_message_details(user_id: str, message_id: str, headers: dict) -> dict:
    """Fetch full message details from Graph API."""
    resp = requests.get(
        f"https://graph.microsoft.com/v1.0/users/{user_id}/messages/{message_id}"
        "?$select=id,subject,from,receivedDateTime,body,hasAttachments,importance",
        headers=headers,
    )
    resp.raise_for_status()
    return resp.json()


def route_to_agent(message: dict, headers: dict):
    """Route incoming email to appropriate Autonomi agent based on content."""
    subject = (message.get("subject") or "").lower()
    sender = message.get("from", {}).get("emailAddress", {}).get("address", "")
    has_attachments = message.get("hasAttachments", False)

    logger.info(f"Routing: '{message.get('subject')}' from {sender}")

    # Route by subject keywords
    if any(kw in subject for kw in ["invoice", "bill", "payment"]):
        route_to_ap_agent(message, headers)

    elif any(kw in subject for kw in ["po", "purchase order", "order confirmation"]):
        route_to_procurement_agent(message, headers)

    elif any(kw in subject for kw in ["coa", "certificate", "lab result", "test result"]):
        route_to_quality_agent(message, headers)

    elif any(kw in subject for kw in ["shipping", "tracking", "delivery", "eta"]):
        route_to_logistics_handler(message, headers)

    elif any(kw in subject for kw in ["recall", "withdrawal", "safety alert"]):
        route_to_recall_agent(message, headers)

    elif any(kw in subject for kw in ["price", "quote", "quotation", "bid"]):
        route_to_cost_agent(message, headers)

    else:
        logger.info(f"No routing match for: '{message.get('subject')}' — queued for manual review")
        log_unrouted(message)


def route_to_ap_agent(message, headers):
    """Route invoice/payment emails to AP Automation Agent."""
    logger.info(f"→ AP Automation Agent: {message.get('subject')}")
    log_agent_decision("ap_automation", "email_received", message)
    # In production: push to AP agent's queue


def route_to_procurement_agent(message, headers):
    """Route PO-related emails to Procurement Agent."""
    logger.info(f"→ Procurement Agent: {message.get('subject')}")
    log_agent_decision("procurement", "email_received", message)


def route_to_quality_agent(message, headers):
    """Route COA/lab results to Quality Agent."""
    logger.info(f"→ Quality Agent: {message.get('subject')}")
    if message.get("hasAttachments"):
        logger.info("  Has attachments — will download and file COAs")
    log_agent_decision("quality", "email_received", message)


def route_to_logistics_handler(message, headers):
    """Route shipping/delivery emails to logistics processing."""
    logger.info(f"→ Logistics Handler: {message.get('subject')}")
    log_agent_decision("procurement", "delivery_update", message)


def route_to_recall_agent(message, headers):
    """Route recall/safety alerts to Recall Agent (high priority)."""
    logger.warning(f"→ RECALL AGENT (HIGH PRIORITY): {message.get('subject')}")
    log_agent_decision("recall", "safety_alert", message)


def route_to_cost_agent(message, headers):
    """Route pricing/quote emails to Cost Agent."""
    logger.info(f"→ Cost Agent: {message.get('subject')}")
    log_agent_decision("finance", "pricing_update", message)


def log_unrouted(message):
    """Log emails that couldn't be auto-routed."""
    log_agent_decision("system", "unrouted_email", message)


def log_agent_decision(agent_id: str, decision_type: str, message: dict):
    """Log the routing decision to audit trail."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent_id": agent_id,
        "decision_type": decision_type,
        "subject": message.get("subject", ""),
        "sender": message.get("from", {}).get("emailAddress", {}).get("address", ""),
        "message_id": message.get("id", ""),
        "service": "outlook",
        "operation": "webhook_route",
    }
    logger.info(f"Audit: {json.dumps(log_entry)}")
    # In production: write to agent_decisions table


def process_webhook(request_body: dict, query_params: dict) -> tuple:
    """
    Process an incoming Graph API webhook notification.
    Returns (response_body, status_code).
    """
    # Handle validation request
    validation_token = query_params.get("validationToken")
    if validation_token:
        logger.info("Webhook validation request received")
        return validation_token, 200

    # Process change notifications
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    notifications = request_body.get("value", [])
    logger.info(f"Processing {len(notifications)} notification(s)")

    for notification in notifications:
        if not validate_notification(notification):
            logger.warning(f"Invalid clientState — skipping notification")
            continue

        resource = notification.get("resource", "")
        change_type = notification.get("changeType", "")

        if change_type == "created" and "/messages/" in resource:
            # Extract user and message ID from resource path
            # Resource format: Users/{userId}/Messages/{messageId}
            parts = resource.split("/")
            user_id = parts[1] if len(parts) > 1 else None
            message_id = parts[3] if len(parts) > 3 else None

            if user_id and message_id:
                try:
                    message = get_message_details(user_id, message_id, headers)
                    route_to_agent(message, headers)
                except Exception as e:
                    logger.error(f"Error processing message {message_id}: {e}")

    return "", 202


# --- Standalone server (for development) ---
if __name__ == "__main__":
    import argparse
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        print("Install Flask for standalone mode: pip install flask", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    app = Flask(__name__)

    @app.route("/api/m365-webhook", methods=["POST", "GET"])
    def webhook():
        if request.method == "GET" or request.args.get("validationToken"):
            body, status = process_webhook({}, request.args)
            return body, status, {"Content-Type": "text/plain"}

        body, status = process_webhook(request.json, request.args)
        return body, status

    print(f"Webhook processor running on port {args.port}")
    app.run(host="0.0.0.0", port=args.port)

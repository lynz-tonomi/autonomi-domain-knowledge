#!/usr/bin/env python3
"""
Process incoming Gmail webhook notifications and route to appropriate Autonomi agents.
Runs as a daemon or invoked per-event from the agent orchestration layer.

Usage:
    # Process a single notification
    python gmail_webhook_processor.py --notification notification.json

    # Route based on content analysis
    python gmail_webhook_processor.py --message-id MSG_ID --tenant-id tenant_001
"""

import subprocess
import json
import sys
import re
import argparse


def run_gws(command: str) -> dict:
    """Run a gws CLI command and return parsed JSON output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return {}
    return json.loads(result.stdout) if result.stdout.strip() else {}


# Routing rules: patterns → agent assignments
ROUTING_RULES = [
    {
        "name": "purchase_order",
        "agent": "procurement-agent",
        "patterns": {
            "subject": [r"(?i)PO\s*#?\d+", r"(?i)purchase\s+order", r"(?i)order\s+confirm"],
            "from": [r"(?i)supplier", r"(?i)vendor", r"(?i)procurement"],
        },
        "priority": "normal",
    },
    {
        "name": "quality_alert",
        "agent": "quality-agent",
        "patterns": {
            "subject": [r"(?i)COA", r"(?i)certificate\s+of\s+analysis", r"(?i)lab\s+result",
                       r"(?i)quality\s+alert", r"(?i)hold\s+notice", r"(?i)out\s+of\s+spec"],
            "body": [r"(?i)pH\s+\d", r"(?i)brix", r"(?i)micro\s*bio", r"(?i)pathogen"],
        },
        "priority": "high",
    },
    {
        "name": "payment_notification",
        "agent": "settlement-agent",
        "patterns": {
            "from": [r"(?i)bill\.com", r"(?i)notifications@bill", r"(?i)payment"],
            "subject": [r"(?i)payment\s+(confirm|complete|fail|process)",
                       r"(?i)invoice\s+(due|paid|overdue)"],
        },
        "priority": "normal",
    },
    {
        "name": "delivery_logistics",
        "agent": "inventory-agent",
        "patterns": {
            "subject": [r"(?i)shipping\s+confirm", r"(?i)delivery\s+notice",
                       r"(?i)tracking\s+#", r"(?i)BOL", r"(?i)bill\s+of\s+lading"],
            "body": [r"(?i)estimated\s+delivery", r"(?i)ETA", r"(?i)freight"],
        },
        "priority": "normal",
    },
    {
        "name": "compliance_regulatory",
        "agent": "compliance-agent",
        "patterns": {
            "subject": [r"(?i)FDA", r"(?i)FSMA", r"(?i)audit", r"(?i)recall",
                       r"(?i)regulatory", r"(?i)inspection"],
            "from": [r"(?i)fda\.gov", r"(?i)state.*health", r"(?i)certif"],
        },
        "priority": "urgent",
    },
    {
        "name": "customer_complaint",
        "agent": "customer-qa-agent",
        "patterns": {
            "subject": [r"(?i)complaint", r"(?i)quality\s+issue", r"(?i)return",
                       r"(?i)damaged", r"(?i)foreign\s+(material|object)"],
        },
        "priority": "high",
    },
]


def classify_email(message: dict) -> list:
    """Classify an email and return matching routing rules."""
    subject = message.get("subject", "")
    from_addr = message.get("from", "")
    body = message.get("body_snippet", "")

    matches = []
    for rule in ROUTING_RULES:
        matched = False
        for field, patterns in rule["patterns"].items():
            text = {"subject": subject, "from": from_addr, "body": body}.get(field, "")
            for pattern in patterns:
                if re.search(pattern, text):
                    matched = True
                    break
            if matched:
                break
        if matched:
            matches.append(rule)

    return matches


def get_message(message_id: str) -> dict:
    """Fetch and parse a Gmail message."""
    result = run_gws(
        f"gws gmail messages get --params '{{\"id\": \"{message_id}\", \"format\": \"metadata\"}}'"
    )

    headers = {h["name"]: h["value"] for h in result.get("payload", {}).get("headers", [])}
    return {
        "id": message_id,
        "subject": headers.get("Subject", ""),
        "from": headers.get("From", ""),
        "to": headers.get("To", ""),
        "date": headers.get("Date", ""),
        "body_snippet": result.get("snippet", ""),
    }


def route_to_agent(agent_id: str, message: dict, rule_name: str, priority: str):
    """Route the email to the appropriate Autonomi agent."""
    routing_event = {
        "event_type": "gmail_inbound",
        "agent_target": agent_id,
        "rule_matched": rule_name,
        "priority": priority,
        "message_id": message["id"],
        "subject": message["subject"],
        "from": message["from"],
        "snippet": message["body_snippet"][:200],
    }

    print(f"  → Routing to {agent_id} (rule: {rule_name}, priority: {priority})")
    print(f"    Subject: {message['subject']}")
    print(f"    From: {message['from']}")

    # In production: publish to agent message bus
    # For now: write to stdout as structured JSON
    return routing_event


def main():
    parser = argparse.ArgumentParser(description="Process Gmail webhooks for Autonomi agents")
    parser.add_argument("--message-id", help="Gmail message ID to process")
    parser.add_argument("--notification", help="Path to webhook notification JSON")
    parser.add_argument("--tenant-id", default="tenant_001", help="Tenant ID")
    args = parser.parse_args()

    if args.notification:
        with open(args.notification) as f:
            notification = json.load(f)
        message_id = notification.get("message_id", notification.get("emailAddress", ""))
    elif args.message_id:
        message_id = args.message_id
    else:
        print("Provide --message-id or --notification", file=sys.stderr)
        sys.exit(1)

    print(f"Processing message: {message_id}")
    message = get_message(message_id)

    matches = classify_email(message)

    if not matches:
        print(f"  No routing rule matched. Subject: {message['subject']}")
        print("  → Routing to lynz (default handler)")
        route_to_agent("lynz", message, "default", "low")
    else:
        events = []
        for rule in matches:
            event = route_to_agent(rule["agent"], message, rule["name"], rule["priority"])
            events.append(event)

        print(json.dumps(events, indent=2))


if __name__ == "__main__":
    main()

# Microsoft Teams Reference — Autonomi Agents

## Table of Contents
1. [Channel Messaging](#channel-messaging)
2. [Incoming Webhooks](#incoming-webhooks)
3. [Team & Channel Management](#team--channel-management)
4. [Meetings](#meetings)
5. [Adaptive Cards](#adaptive-cards)

## Channel Messaging

### Post message to channel (Graph API)

Requires `ChannelMessage.Send` permission (delegated) or application permission with RSC.

```python
def post_to_channel(headers, team_id, channel_id, message_html):
    """Post a message to a Teams channel."""
    resp = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        json={"body": {"contentType": "html", "content": message_html}}
    )
    resp.raise_for_status()
    return resp.json()
```

### Post with mention

```python
def post_with_mention(headers, team_id, channel_id, user_id, user_name, message):
    """Post a message that @mentions a specific user."""
    requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
        headers=headers,
        json={
            "body": {
                "contentType": "html",
                "content": f'<at id="0">{user_name}</at> {message}'
            },
            "mentions": [{
                "id": 0,
                "mentionText": user_name,
                "mentioned": {"user": {"id": user_id, "displayName": user_name}}
            }]
        }
    )
```

### Read channel messages

```python
# List recent messages in a channel
messages = requests.get(
    f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages"
    "?$top=25",
    headers=headers
).json()
```

## Incoming Webhooks

Simpler than Graph API — no app registration or auth required. Configured per-channel in Teams.

### Send a basic message

```python
def send_webhook_alert(webhook_url, title, facts, color="FF0000"):
    """Send an alert card via Teams incoming webhook."""
    requests.post(webhook_url, json={
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "summary": title,
        "themeColor": color,
        "sections": [{
            "activityTitle": title,
            "facts": [{"name": k, "value": str(v)} for k, v in facts.items()],
        }]
    })
```

### Autonomi alert templates

```python
# Quality hold alert
send_webhook_alert(
    os.environ["TEAMS_QUALITY_WEBHOOK"],
    "Quality Hold — Batch 2847",
    {
        "Product": "Mango Puree 500ml",
        "Lot": "Lot-2847",
        "Issue": "pH reading 3.2 (spec: 3.5-4.0)",
        "Action": "QC inspection scheduled 9am tomorrow",
        "Agent": "Quality Agent"
    },
    color="FF0000"  # Red for hold
)

# Delivery received
send_webhook_alert(
    os.environ["TEAMS_RECEIVING_WEBHOOK"],
    "Delivery Received — PO #12847",
    {
        "Supplier": "Tropical Fruits Co",
        "Items": "Mango Puree (1200 lbs), Passion Fruit Concentrate (500 lbs)",
        "Status": "Receiving & QC in progress",
        "Agent": "Procurement Agent"
    },
    color="00CC00"  # Green for received
)

# Low stock warning
send_webhook_alert(
    os.environ["TEAMS_INVENTORY_WEBHOOK"],
    "Low Stock Alert — Citric Acid",
    {
        "Current Stock": "150 lbs",
        "Reorder Point": "200 lbs",
        "Days of Supply": "3 days",
        "Recommended Action": "Place PO with Supplier-B (best lead time)",
        "Agent": "Inventory Agent"
    },
    color="FFAA00"  # Orange for warning
)
```

## Team & Channel Management

### List teams the service account belongs to

```python
teams = requests.get(
    "https://graph.microsoft.com/v1.0/groups"
    "?$filter=resourceProvisioningOptions/Any(x:x eq 'Team')"
    "&$select=id,displayName",
    headers=headers
).json()["value"]
```

### List channels in a team

```python
channels = requests.get(
    f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels",
    headers=headers
).json()["value"]
```

### Recommended channel structure for Autonomi

```
Autonomi Operations
├── General
├── #procurement — PO updates, supplier comms
├── #quality — QC results, hold notices
├── #production — Schedule updates, yield reports
├── #receiving — Delivery notifications
├── #compliance — Audit alerts, FSMA updates
├── #finance — Payment status, cost alerts
├── #agent-decisions — All agent decision logs
└── #alerts-critical — High-priority alerts only
```

## Meetings

### Create an online meeting

```python
def create_teams_meeting(headers, organizer_id, subject, start, end, attendees=None):
    """Create a Teams meeting and return the join URL."""
    body = {
        "subject": subject,
        "startDateTime": start,
        "endDateTime": end,
    }
    if attendees:
        body["participants"] = {
            "attendees": [{"upn": email, "role": "attendee"} for email in attendees]
        }
    meeting = requests.post(
        f"https://graph.microsoft.com/v1.0/users/{organizer_id}/onlineMeetings",
        headers=headers,
        json=body
    ).json()
    return meeting["joinUrl"]
```

### Create calendar event with Teams meeting

```python
def schedule_meeting_with_calendar(headers, organizer_id, subject, start, end, attendees, body_html=""):
    """Create a calendar event that includes a Teams meeting link."""
    event = requests.post(
        f"https://graph.microsoft.com/v1.0/users/{organizer_id}/events",
        headers=headers,
        json={
            "subject": subject,
            "body": {"contentType": "HTML", "content": body_html},
            "start": {"dateTime": start, "timeZone": "America/New_York"},
            "end": {"dateTime": end, "timeZone": "America/New_York"},
            "attendees": [
                {"emailAddress": {"address": email}, "type": "required"}
                for email in attendees
            ],
            "isOnlineMeeting": True,
            "onlineMeetingProvider": "teamsForBusiness"
        }
    ).json()
    return event
```

## Adaptive Cards

For richer Teams messages with interactive elements (buttons, forms):

```python
def send_adaptive_card(webhook_url, card_body):
    """Send an Adaptive Card via incoming webhook."""
    requests.post(webhook_url, json={
        "type": "message",
        "attachments": [{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "contentUrl": None,
            "content": card_body
        }]
    })

# Example: Quality hold card with approve/reject buttons
quality_hold_card = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.4",
    "body": [
        {"type": "TextBlock", "text": "Quality Hold — Batch 2847", "weight": "Bolder", "size": "Large"},
        {"type": "FactSet", "facts": [
            {"title": "Product", "value": "Mango Puree 500ml"},
            {"title": "Issue", "value": "pH 3.2 (spec: 3.5-4.0)"},
            {"title": "Recommended", "value": "Hold for re-test"},
        ]},
    ],
    "actions": [
        {"type": "Action.Submit", "title": "Approve Hold", "data": {"action": "approve", "batch": "2847"}},
        {"type": "Action.Submit", "title": "Override — Release", "data": {"action": "override", "batch": "2847"}},
    ]
}
```

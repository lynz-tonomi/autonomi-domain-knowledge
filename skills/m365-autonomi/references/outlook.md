# Outlook Integration Reference — Autonomi Agents

## Table of Contents
1. [Send Operations](#send-operations)
2. [Read & Triage](#read--triage)
3. [Attachments](#attachments)
4. [Mail Rules & Folders](#mail-rules--folders)
5. [Webhooks (Subscriptions)](#webhooks-subscriptions)

## Send Operations

### Send mail (app-only, on behalf of service account)

```python
def send_mail(headers, sender, to, subject, body_html, attachments=None, cc=None):
    """Send email via Graph API. Requires Mail.Send permission."""
    message = {
        "subject": subject,
        "body": {"contentType": "HTML", "content": body_html},
        "toRecipients": [{"emailAddress": {"address": addr}} for addr in (to if isinstance(to, list) else [to])],
    }
    if cc:
        message["ccRecipients"] = [{"emailAddress": {"address": addr}} for addr in cc]
    if attachments:
        message["attachments"] = [{
            "@odata.type": "#microsoft.graph.fileAttachment",
            "name": att["name"],
            "contentType": att.get("content_type", "application/octet-stream"),
            "contentBytes": att["base64_content"]
        } for att in attachments]

    response = requests.post(
        f"https://graph.microsoft.com/v1.0/users/{sender}/sendMail",
        headers={**headers, "Content-Type": "application/json"},
        json={"message": message, "saveToSentItems": True}
    )
    response.raise_for_status()
```

### Reply in thread

```python
def reply_to_message(headers, user_id, message_id, body_html):
    """Reply to an existing email thread."""
    requests.post(
        f"https://graph.microsoft.com/v1.0/users/{user_id}/messages/{message_id}/reply",
        headers=headers,
        json={"message": {"body": {"contentType": "HTML", "content": body_html}}}
    )
```

### Send with importance / read receipt

```python
message = {
    "subject": "URGENT: Batch Hold — Lot 2847",
    "importance": "high",
    "isDeliveryReceiptRequested": True,
    "isReadReceiptRequested": True,
    # ... rest of message
}
```

## Read & Triage

### Read unread messages

```python
def get_unread_messages(headers, user_id, max_results=25):
    """Get unread messages, newest first."""
    url = (
        f"https://graph.microsoft.com/v1.0/users/{user_id}/messages"
        f"?$filter=isRead eq false"
        f"&$orderby=receivedDateTime desc"
        f"&$top={max_results}"
        f"&$select=id,subject,from,receivedDateTime,bodyPreview,hasAttachments"
    )
    return get_all_pages(url, headers)
```

### Search messages

```python
# By sender and subject
GET /v1.0/users/{id}/messages?$search="from:supplier@example.com subject:PO"

# By date range
GET /v1.0/users/{id}/messages?$filter=receivedDateTime ge 2026-03-01T00:00:00Z

# Full-text search
GET /v1.0/users/{id}/messages?$search="mango puree quality hold"
```

### Agent triage pattern

The Procurement Agent processes supplier emails like this:

```python
def triage_procurement_inbox(headers, service_account):
    """Process unread supplier emails and route to appropriate action."""
    messages = get_unread_messages(headers, service_account)
    for msg in messages:
        subject = msg["subject"].lower()
        sender = msg["from"]["emailAddress"]["address"]

        if "invoice" in subject:
            route_to_ap_agent(msg)
        elif "shipping" in subject or "tracking" in subject:
            update_delivery_eta(msg)
        elif "coa" in subject or "certificate" in subject:
            download_and_file_coa(headers, service_account, msg)
        elif "price" in subject or "quote" in subject:
            route_to_cost_agent(msg)

        # Mark as read
        requests.patch(
            f"https://graph.microsoft.com/v1.0/users/{service_account}/messages/{msg['id']}",
            headers=headers,
            json={"isRead": True}
        )
```

## Attachments

### Download attachments from a message

```python
def get_attachments(headers, user_id, message_id):
    """Download all attachments from a message."""
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/messages/{message_id}/attachments"
    attachments = requests.get(url, headers=headers).json().get("value", [])
    files = []
    for att in attachments:
        if att["@odata.type"] == "#microsoft.graph.fileAttachment":
            import base64
            files.append({
                "name": att["name"],
                "content_type": att["contentType"],
                "content": base64.b64decode(att["contentBytes"]),
                "size": att["size"]
            })
    return files
```

### Large attachments (>3MB)

For large attachments, use item attachments with a reference link instead of inline base64:

```python
# Create upload session for large attachment
session = requests.post(
    f"https://graph.microsoft.com/v1.0/users/{user_id}/messages/{msg_id}/attachments/createUploadSession",
    headers=headers,
    json={
        "AttachmentItem": {
            "attachmentType": "file",
            "name": "large_report.pdf",
            "size": file_size
        }
    }
).json()
# Then upload in chunks to session["uploadUrl"]
```

## Mail Rules & Folders

### Create a mail rule (auto-route supplier emails)

```python
requests.post(
    f"https://graph.microsoft.com/v1.0/users/{user_id}/mailFolders/inbox/messageRules",
    headers=headers,
    json={
        "displayName": "Route supplier invoices",
        "sequence": 1,
        "isEnabled": True,
        "conditions": {"subjectContains": ["invoice", "payment"]},
        "actions": {"moveToFolder": invoices_folder_id, "markImportance": "high"}
    }
)
```

### Create folder

```python
folder = requests.post(
    f"https://graph.microsoft.com/v1.0/users/{user_id}/mailFolders",
    headers=headers,
    json={"displayName": "Autonomi-Processed"}
).json()
```

## Webhooks (Subscriptions)

### Subscribe to new mail

```python
subscription = requests.post(
    "https://graph.microsoft.com/v1.0/subscriptions",
    headers=headers,
    json={
        "changeType": "created",
        "notificationUrl": "https://autonomi.example.com/api/m365-webhook",
        "resource": f"/users/{service_account}/messages",
        "expirationDateTime": (datetime.utcnow() + timedelta(days=2)).isoformat() + "Z",
        "clientState": os.environ["WEBHOOK_SECRET"]
    }
).json()
```

### Subscription lifecycle
- **Max expiration**: 4230 minutes (~2.94 days) for messages
- **Renewal**: POST to `/v1.0/subscriptions/{id}` with new `expirationDateTime`
- **Validation**: Graph sends GET with `validationToken` query param — return it as plain text
- Set up a recurring task to renew subscriptions before expiry

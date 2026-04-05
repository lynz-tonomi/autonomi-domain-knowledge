---
name: m365-autonomi
description: >
  Microsoft 365 integration for Autonomi — connects 29 AI agents to tenant M365 via
  Microsoft Graph API. Handles Outlook email ops (PO emails, quality alerts), SharePoint/OneDrive
  file management (COA uploads, document libraries), Excel data sync (inventory, QC logs),
  Teams alerts (channel messages, meetings), and Calendar scheduling. Built for NemoClaw
  sandboxes with per-tenant Entra ID isolation.
  ALWAYS trigger on: Microsoft 365, M365, Office 365, Graph API, Microsoft Graph, Outlook,
  SharePoint, OneDrive, Teams, Excel Online, Entra ID, Azure AD, MSAL, service principal,
  Microsoft.Graph PowerShell, PnP PowerShell, or any reading/writing/sending through
  Microsoft services. Also trigger when agents need to notify tenants, sync data, or send
  emails via M365 — even if Microsoft isn't explicitly mentioned.
---

# Microsoft 365 Integration Agent for Autonomi

You are the integration layer between Autonomi's agentic supply chain platform and Microsoft 365. Your job is to enable Autonomi's 29 agents to read, write, and act through tenant M365 accounts — turning agent decisions into documents, emails, calendar events, Teams messages, and shared data that tenant teams actually use day-to-day.

The foundation is the **Microsoft Graph API** — Microsoft's unified API endpoint that provides access to Outlook, SharePoint, OneDrive, Teams, Planner, and all other M365 services through a single REST endpoint (`https://graph.microsoft.com`). For PowerShell-based admin tasks, the **Microsoft.Graph** and **PnP.PowerShell** modules provide cmdlet-based access.

## Why This Matters for Autonomi

Autonomi agents make decisions (reorder ingredients, flag quality issues, schedule production). But those decisions are useless if they stay inside the platform. Many tenants live in Microsoft 365 — their team reads Outlook, their finance team works in Excel, their ops meetings happen on Teams. This skill bridges that gap:

- **Procurement Agent** generates a PO → auto-emails supplier via Outlook + creates Excel tracking row in SharePoint
- **Quality Agent** flags a batch hold → sends alert email to QA manager + creates Word incident report in SharePoint
- **Inventory Agent** detects low stock → updates shared Excel dashboard on SharePoint + sends Teams channel alert
- **LynZ** answers a voice query about production status → pulls data from tenant's shared Excel on SharePoint

## Setup & Authentication

### App Registration (Entra ID)

Each tenant needs an app registration in Entra ID (Azure AD). This is the M365 equivalent of a Google service account.

1. Tenant admin goes to [Entra ID portal](https://entra.microsoft.com) → App registrations → New registration
2. Name: `Autonomi-Integration-{TenantName}`
3. Supported account types: Single tenant
4. Note the **Application (client) ID** and **Directory (tenant) ID**
5. Under Certificates & secrets: upload a certificate (production) or create a client secret (dev)
6. Under API permissions: add the required Microsoft Graph permissions per agent (see Scope Minimization)
7. **Grant admin consent** for application permissions

### Per-Tenant Authentication (NemoClaw Isolation)

Each tenant's M365 credentials must be isolated within their NemoClaw OpenShell sandbox. Never share credentials across tenants.

**Certificate-based (recommended for production):**
```python
import msal

TENANT_ID = os.environ["M365_TENANT_ID"]
CLIENT_ID = os.environ["M365_CLIENT_ID"]
CERT_PATH = f"/sandbox/credentials/tenant_{TENANT_ID}/cert.pem"
KEY_PATH = f"/sandbox/credentials/tenant_{TENANT_ID}/key.pem"

with open(KEY_PATH) as f:
    private_key = f.read()

app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    client_credential={"thumbprint": os.environ["M365_CERT_THUMBPRINT"], "private_key": private_key},
)
token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
headers = {"Authorization": f"Bearer {token['access_token']}"}
```

**Client secret (for development/testing):**
```python
app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    client_credential=os.environ["M365_CLIENT_SECRET"],
)
token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
```

**PowerShell (admin tasks):**
```powershell
Connect-MgGraph -TenantId $env:M365_TENANT_ID `
    -ClientId $env:M365_CLIENT_ID `
    -CertificateThumbprint $env:M365_CERT_THUMBPRINT
```

**Security constraints (OpenShell policy):**
- Credentials encrypted at rest (AES-256-GCM, OS keyring)
- Each agent sandbox gets read-only access to its tenant's credential file
- Network policy: only `graph.microsoft.com`, `login.microsoftonline.com` endpoints allowed from sandbox
- Model Armor sanitization on all responses: enabled by default on all Graph API reads

## Core Operations by Service

### Outlook — Agent Email Operations

Read the reference file `references/outlook.md` for full patterns including triage, threading, and attachment handling.

```python
# Send (agent notifications, PO confirmations, quality alerts)
requests.post(
    f"https://graph.microsoft.com/v1.0/users/{SERVICE_ACCOUNT}/sendMail",
    headers=headers,
    json={
        "message": {
            "subject": "PO #12847 — Mango Puree",
            "body": {"contentType": "HTML", "content": "<p>Purchase order attached.</p>"},
            "toRecipients": [{"emailAddress": {"address": "supplier@example.com"}}],
            "attachments": [{
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": "PO-12847.pdf",
                "contentType": "application/pdf",
                "contentBytes": base64_encoded_pdf
            }]
        },
        "saveToSentItems": True
    }
)

# Read inbox (process supplier responses)
messages = requests.get(
    f"https://graph.microsoft.com/v1.0/users/{SERVICE_ACCOUNT}/messages"
    "?$filter=isRead eq false&$orderby=receivedDateTime desc&$top=25",
    headers=headers
).json()

# Search (find related correspondence)
results = requests.get(
    f"https://graph.microsoft.com/v1.0/users/{SERVICE_ACCOUNT}/messages"
    '?$search="from:supplier@example.com subject:PO"',
    headers=headers
).json()
```

**Autonomi agent mapping:**
| Agent | Outlook Use Case |
|-------|-----------------|
| Procurement Agent | Send PO emails, receive supplier confirmations |
| Quality Agent | Send hold notifications, receive lab results |
| Settlement Agent | Send payment confirmations, receive invoices |
| AP Automation Agent | Forward approved bills, send payment reminders |
| LynZ | Draft and send emails on voice command |

### SharePoint & OneDrive — Document & File Management

Read `references/sharepoint.md` for site structure patterns and file organization.

```python
# Upload to SharePoint document library (COAs, audit docs, compliance certificates)
site_id = "contoso.sharepoint.com,site-guid,web-guid"
drive_id = requests.get(
    f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive",
    headers=headers
).json()["id"]

# Small file upload (<4MB)
requests.put(
    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/root:"
    f"/Autonomi/Procurement/COAs/COA-Batch-2847.pdf:/content",
    headers={**headers, "Content-Type": "application/pdf"},
    data=open("COA_batch_2847.pdf", "rb").read()
)

# List files in folder
files = requests.get(
    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/root:"
    "/Autonomi/Quality/Batch-Reports:/children",
    headers=headers
).json()

# Create folder
requests.post(
    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/root:/Autonomi:/children",
    headers=headers,
    json={"name": "QC-Reports-2026", "folder": {}, "@microsoft.graph.conflictBehavior": "rename"}
)
```

**Recommended tenant SharePoint folder structure:**
```
Autonomi-{TenantName}/
├── Procurement/
│   ├── Purchase-Orders/
│   ├── Supplier-Contracts/
│   ├── COAs/
│   └── Supplier-Scorecards/
├── Quality/
│   ├── Batch-Reports/
│   ├── Hold-Notices/
│   ├── Lab-Results/
│   └── Audit-Documents/
├── Production/
│   ├── Schedules/
│   ├── Yield-Reports/
│   └── BOM-Exports/
├── Compliance/
│   ├── FSMA-204/
│   ├── Certifications/
│   ├── Recall-Records/
│   └── Training-Records/
├── Finance/
│   ├── Invoices/
│   ├── Cost-Reports/
│   └── AP-AR-Exports/
└── Agent-Reports/
    ├── Decision-Logs/
    ├── Anomaly-Reports/
    └── Performance-Dashboards/
```

### Excel Online (via SharePoint) — Data Sync & Dashboards

Read `references/excel.md` for formula patterns, data validation, and dashboard templates.

```python
# Read data from Excel workbook on SharePoint
workbook_path = "/Autonomi/Inventory/inventory-tracker.xlsx"
data = requests.get(
    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/root:{workbook_path}:"
    "/workbook/worksheets/Inventory/range(address='A1:H100')",
    headers=headers
).json()

# Append row (log agent decisions, add inventory records)
requests.post(
    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/root:{workbook_path}:"
    "/workbook/tables/InventoryTable/rows/add",
    headers=headers,
    json={
        "values": [["2026-03-20", "Mango Puree", "Lot-2847", 1200, "lbs", "Received", "QC-Pending", "Supplier-A"]]
    }
)

# Update specific cell
requests.patch(
    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/root:{workbook_path}:"
    "/workbook/worksheets/Inventory/range(address='F2')",
    headers=headers,
    json={"values": [["QC-Passed"]]}
)
```

**Common Autonomi ↔ Excel sync patterns:**
| Autonomi Data | Excel Location | Sync Direction | Frequency |
|---------------|---------------|----------------|-----------|
| Inventory levels | `Inventory!A:H` | Autonomi → Excel | Hourly |
| Production schedule | `Production!A:F` | Bi-directional | Real-time on change |
| Quality results | `QC-Log!A:J` | Autonomi → Excel | On test completion |
| Supplier scorecard | `Suppliers!A:G` | Autonomi → Excel | Weekly |
| BOM cost rollup | `BOM-Costs!A:L` | Autonomi → Excel | On ingredient price change |
| Agent decisions | `Agent-Log!A:I` | Autonomi → Excel | Real-time |
| BILL.com payment status | `AP-Tracker!A:H` | BILL.com → Autonomi → Excel | On payment event |

### Microsoft Teams — Real-Time Alerts & Collaboration

Read `references/teams.md` for channel messaging, meeting scheduling, and bot patterns.

```python
# Post to Teams channel (real-time agent alerts)
team_id = os.environ["TEAMS_TEAM_ID"]
channel_id = os.environ["TEAMS_OPS_CHANNEL_ID"]

requests.post(
    f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages",
    headers=headers,
    json={
        "body": {
            "contentType": "html",
            "content": "<b>Quality Alert:</b> Batch 2847 placed on hold. "
                       "pH reading 3.2 (spec: 3.5-4.0). "
                       "QC inspection scheduled for 9am tomorrow."
        }
    }
)

# Incoming webhook (simpler alternative — no auth required)
webhook_url = os.environ["TEAMS_WEBHOOK_URL"]
requests.post(webhook_url, json={
    "@type": "MessageCard",
    "summary": "Quality Alert",
    "themeColor": "FF0000",
    "sections": [{
        "activityTitle": "Batch 2847 — Quality Hold",
        "facts": [
            {"name": "Product", "value": "Mango Puree"},
            {"name": "Issue", "value": "pH out of spec (3.2 vs 3.5-4.0)"},
            {"name": "Action", "value": "QC inspection scheduled 9am tomorrow"},
        ],
    }],
})

# Create online meeting
meeting = requests.post(
    f"https://graph.microsoft.com/v1.0/users/{SERVICE_ACCOUNT}/onlineMeetings",
    headers=headers,
    json={
        "subject": "Emergency QC Review — Batch 2847",
        "startDateTime": "2026-03-22T09:00:00Z",
        "endDateTime": "2026-03-22T10:00:00Z",
    }
).json()
join_url = meeting["joinUrl"]
```

**Agent → Teams triggers:**
| Agent Event | Teams Action |
|------------|-------------|
| Ingredient delivery ETA confirmed | Post in #receiving channel |
| Batch hold issued | Alert in #quality channel + schedule review meeting |
| Production schedule updated | Post in #production channel |
| Supplier contract renewal approaching | Alert in #procurement channel |
| BILL.com payment due | Notify in #finance channel |
| FSMA mock recall due | Alert in #compliance channel |

### Outlook Calendar — Scheduling & Coordination

```python
# Create event (schedule QC inspection, supplier call, production run)
requests.post(
    f"https://graph.microsoft.com/v1.0/users/{SERVICE_ACCOUNT}/events",
    headers=headers,
    json={
        "subject": "QC Inspection — Lot 2847 Mango Puree",
        "body": {"contentType": "HTML", "content": "<p>Triggered by Quality Agent: pH out of spec.</p>"},
        "start": {"dateTime": "2026-03-22T09:00:00", "timeZone": "America/New_York"},
        "end": {"dateTime": "2026-03-22T10:00:00", "timeZone": "America/New_York"},
        "attendees": [
            {"emailAddress": {"address": "qa_manager@tenant.com", "name": "QA Manager"}, "type": "required"}
        ],
        "isOnlineMeeting": True,
        "onlineMeetingProvider": "teamsForBusiness"
    }
)

# Check availability
schedule = requests.post(
    f"https://graph.microsoft.com/v1.0/users/{SERVICE_ACCOUNT}/calendar/getSchedule",
    headers=headers,
    json={
        "schedules": ["qa_manager@tenant.com", "plant_manager@tenant.com"],
        "startTime": {"dateTime": "2026-03-22T08:00:00", "timeZone": "America/New_York"},
        "endTime": {"dateTime": "2026-03-22T18:00:00", "timeZone": "America/New_York"},
        "availabilityViewInterval": 30
    }
).json()
```

### Word Online — Document Generation

For complex document generation (SOPs, compliance reports), use the Word REST API or generate `.docx` files with `python-docx` and upload to SharePoint:

```python
from docx import Document

def generate_batch_report(batch_data: dict, output_path: str):
    """Generate a batch traceability report as a Word document."""
    doc = Document()
    doc.add_heading(f"Batch Report: {batch_data['lot_number']}", 0)
    doc.add_paragraph(f"Product: {batch_data['product_name']}")
    doc.add_paragraph(f"Date: {batch_data['production_date']}")

    doc.add_heading("Quality Results", level=1)
    table = doc.add_table(rows=1, cols=3)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text = "Test", "Result", "Spec"
    for test in batch_data.get("qc_results", []):
        row = table.add_row().cells
        row[0].text, row[1].text, row[2].text = test["name"], str(test["value"]), test["spec"]

    doc.save(output_path)
    # Then upload to SharePoint via Graph API
```

**Agent-generated document types:**
- Quality hold notices (Quality Agent)
- Batch traceability reports (Recall Agent)
- Supplier performance summaries (Procurement Agent)
- Production yield reports (Production Agent)
- FSMA 204 CTE records (Compliance Agent)
- Cost variance reports (Finance Agent)
- Weekly operational summaries (LynZ)

### LynZ Voice Agent — M365 via Natural Language

LynZ is Autonomi's voice-first assistant. Operators interact conversationally — "send that PO," "what's on the calendar," "pull up the QC numbers." LynZ needs broad read access across all services plus Outlook send.

**Voice → Graph API command mapping:**

```python
# "What emails came in from our mango supplier?"
GET /v1.0/users/{svc}/messages?$search="from:supplier@example.com"&$top=10&$orderby=receivedDateTime desc

# "What's on the production calendar today?"
GET /v1.0/users/{svc}/calendarView?startDateTime=2026-03-21T00:00:00Z&endDateTime=2026-03-21T23:59:59Z

# "Pull up the latest inventory numbers"
GET /v1.0/drives/{id}/items/root:/Autonomi/Inventory/tracker.xlsx:/workbook/worksheets/Inventory/usedRange

# "Send that PO to the supplier"
POST /v1.0/users/{svc}/sendMail  (with confirmation prompt)

# "Schedule a QC review for tomorrow at 9"
POST /v1.0/users/{svc}/events

# "Post the QC results to the team"
POST /v1.0/teams/{id}/channels/{id}/messages
```

**LynZ-specific rules:**
- All email sends require voice confirmation ("Should I send this?")
- Read-only access to Excel, SharePoint, and OneDrive — LynZ reports data but doesn't modify it
- Calendar event creation delegated to scheduling agents unless user explicitly asks LynZ
- All M365 content screened through Model Armor before processing (LynZ's broad read scope makes her a high-value injection target)
- Summarize data for voice output — don't dump raw spreadsheet values

**LynZ tool definitions (for voice agent tool registry):**

```json
[
  {
    "name": "m365_outlook_search",
    "description": "Search tenant Outlook for messages matching a query",
    "parameters": {"query": "string", "max_results": "number"}
  },
  {
    "name": "m365_outlook_send",
    "description": "Send an email via Outlook. Always confirm with user before executing.",
    "parameters": {"to": "string", "subject": "string", "body": "string", "attachment_path": "string"}
  },
  {
    "name": "m365_calendar_agenda",
    "description": "Get today's calendar events or events for a specified date",
    "parameters": {"date": "string"}
  },
  {
    "name": "m365_calendar_create",
    "description": "Create an Outlook calendar event with optional Teams meeting link",
    "parameters": {"title": "string", "start_time": "string", "end_time": "string", "attendees": "array", "teams_meeting": "boolean"}
  },
  {
    "name": "m365_excel_read",
    "description": "Read data from a tenant Excel workbook on SharePoint by name or path",
    "parameters": {"workbook_path": "string", "sheet_name": "string", "range": "string"}
  },
  {
    "name": "m365_sharepoint_search",
    "description": "Search tenant SharePoint for files by name or content",
    "parameters": {"query": "string", "site": "string"}
  },
  {
    "name": "m365_teams_post",
    "description": "Post a message to a Teams channel",
    "parameters": {"channel": "string", "message": "string"}
  }
]
```

## Enterprise Patterns

These patterns are non-negotiable for production Autonomi integrations. Every script that calls Microsoft Graph API must include all three: pagination, retry with backoff, and proper error handling. Skipping retry logic is the #1 cause of silent failures in production — Graph API throttles aggressively under load, and a single 429 response without backoff can cause an entire agent workflow to fail. Always wrap Graph API calls in the `graph_request()` helper below (or equivalent) rather than calling `requests.get/post` directly.

### Pagination

Graph API returns paged results. Always handle `@odata.nextLink`:

```python
def get_all_pages(url: str, headers: dict) -> list:
    """Fetch all pages from a Graph API endpoint."""
    results = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        results.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    return results
```

### Throttling and Retry

Graph API uses HTTP 429 with a `Retry-After` header. This is critical — Autonomi agents can generate bursts of API calls (e.g., the Procurement Agent sending POs + uploading to SharePoint + posting to Teams in rapid succession), and without retry logic, one throttled call silently breaks the entire workflow. Use this helper for ALL Graph API calls:

```python
import time

def graph_request(method: str, url: str, headers: dict, json_body=None, data=None, max_retries=5):
    """Make a Graph API request with exponential backoff on throttling.
    Use this for EVERY Graph API call — never call requests.get/post directly."""
    for attempt in range(max_retries):
        response = getattr(requests, method)(url, headers=headers, json=json_body, data=data)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 2 ** attempt))
            time.sleep(retry_after)
            continue
        response.raise_for_status()
        return response.json() if response.content else None
    raise RuntimeError(f"Still throttled after {max_retries} retries")
```

Include this function in every script generated and use it consistently — even for "simple" one-off calls like sending a single email. Consistency prevents bugs.

### Batch Requests

Graph API supports batching up to 20 requests in a single call:

```python
def batch_graph(requests_list: list, headers: dict) -> list:
    """Send up to 20 Graph API requests in a single batch."""
    payload = {"requests": [
        {"id": str(i), "method": r["method"], "url": r["url"]}
        for i, r in enumerate(requests_list[:20])
    ]}
    resp = requests.post(
        "https://graph.microsoft.com/v1.0/$batch",
        headers={**headers, "Content-Type": "application/json"},
        json=payload
    )
    resp.raise_for_status()
    return resp.json()["responses"]
```

### Subscriptions (Webhooks)

For real-time event processing instead of polling:

```python
# Subscribe to new messages in a mailbox
subscription = requests.post(
    "https://graph.microsoft.com/v1.0/subscriptions",
    headers=headers,
    json={
        "changeType": "created",
        "notificationUrl": "https://autonomi-webhooks.example.com/api/m365",
        "resource": f"/users/{SERVICE_ACCOUNT}/messages",
        "expirationDateTime": "2026-03-28T12:00:00Z",
        "clientState": os.environ["WEBHOOK_SECRET"]
    }
).json()
```

### Error Handling

```python
def handle_graph_error(response):
    """Parse Graph API errors and raise meaningful exceptions."""
    try:
        response.raise_for_status()
    except requests.HTTPError:
        error = response.json().get("error", {})
        code, msg = error.get("code", "Unknown"), error.get("message", "No details")
        if response.status_code == 401:
            raise PermissionError(f"Auth expired — re-acquire token: {msg}")
        elif response.status_code == 403:
            raise PermissionError(f"Missing API permission in Entra ID app registration: {code}: {msg}")
        elif response.status_code == 404:
            raise FileNotFoundError(f"Resource not found: {msg}")
        else:
            raise RuntimeError(f"Graph API {response.status_code} [{code}]: {msg}")
```

## Security Architecture (NemoClaw Integration)

Read `references/security.md` for full OpenShell policy templates and scope matrices.

### Scope Minimization

Each agent type gets the minimum Microsoft Graph API permissions required:

| Agent | Mail | SharePoint/OneDrive | Teams | Calendar | Excel |
|-------|------|-------------------|-------|----------|-------|
| Procurement | Mail.Send, Mail.Read | Files.ReadWrite | ChannelMessage.Send | — | — |
| Quality | Mail.Send | Files.ReadWrite | ChannelMessage.Send | Calendars.ReadWrite | — |
| Inventory | — | Files.Read.All | ChannelMessage.Send | — | — |
| Settlement | Mail.Send | Files.Read.All | — | — | — |
| Recall | Mail.Send | Files.ReadWrite | ChannelMessage.Send | Calendars.ReadWrite | — |
| Compliance | — | Files.ReadWrite | — | — | — |
| AP Automation | Mail.Send, Mail.Read | Files.ReadWrite | ChannelMessage.Send | Calendars.ReadWrite | — |
| LynZ | Mail.Send, Mail.Read | Files.Read.All | ChannelMessage.Send | Calendars.Read | — |
| IoT Monitor | — | — | ChannelMessage.Send | — | — |
| Maintenance | — | — | ChannelMessage.Send | Calendars.ReadWrite | — |

### Model Armor Integration

All content read from M365 (email bodies, document text, Excel data) passes through the Prompt Injection Detection Engine before agent processing. Threat scenarios mirror the Google Workspace skill: malicious email bodies, tampered spreadsheet cells, poisoned documents, calendar invite injection.

## Scripts

Bundled scripts in `scripts/` automate common multi-step workflows:

- `scripts/sync_inventory_to_excel.py` — Full inventory sync from Autonomi DB → Excel on SharePoint
- `scripts/generate_batch_report.py` — Create Word doc batch report from lot/batch data and upload to SharePoint
- `scripts/setup_tenant_workspace.py` — Initialize SharePoint folder structure + Excel templates for new tenant
- `scripts/outlook_webhook_processor.py` — Process incoming Outlook webhook notifications → route to appropriate agent

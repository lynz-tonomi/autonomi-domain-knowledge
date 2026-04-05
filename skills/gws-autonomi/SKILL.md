---
name: gws-autonomi
description: >
  Google Workspace integration for Autonomi — connects 29 AI agents to tenant Google Workspace
  via the gws CLI. Handles document automation (SOPs, QC reports in Docs/Sheets), email ops
  (PO emails, quality alerts via Gmail), calendar management (production schedules, QC inspections),
  data sync (Autonomi ↔ Sheets), file management (Drive organization, COA uploads), and Meet
  integration. Built for NemoClaw sandboxes with per-tenant OAuth isolation.
  ALWAYS trigger on: Google Workspace, G Suite, Gmail, Google Drive, Google Docs, Google Sheets,
  Google Calendar, Google Meet, Google Chat, gws, workspace integration, email agent, document
  automation, spreadsheet sync, calendar scheduling, or any reading/writing/sending through Google
  services. Also trigger when agents need to notify tenants, generate reports, sync data to
  spreadsheets, or schedule meetings — even if Google isn't explicitly mentioned.
---

# Google Workspace Integration Agent for Autonomi

You are the integration layer between Autonomi's agentic supply chain platform and Google Workspace. Your job is to enable Autonomi's 29 agents to read, write, and act through tenant Google Workspace accounts — turning agent decisions into documents, emails, calendar events, and shared data that tenant teams actually use day-to-day.

The foundation is the **Google Workspace CLI (`gws`)** — Google's official CLI that dynamically builds its command surface from the Discovery Service and includes an MCP server mode for structured agent interaction. This means when Google adds APIs, the CLI picks them up automatically.

## Why This Matters for Autonomi

Autonomi agents make decisions (reorder ingredients, flag quality issues, schedule production). But those decisions are useless if they stay inside the platform. Tenants live in Google Workspace — their team reads Gmail, their finance team works in Sheets, their ops meetings happen on Calendar. This skill bridges that gap:

- **Procurement Agent** generates a PO → auto-emails supplier via Gmail + creates Sheets tracking row
- **Quality Agent** flags a batch hold → sends alert email to QA manager + creates Google Doc incident report
- **Inventory Agent** detects low stock → updates shared Sheets dashboard + sends Calendar reminder for reorder review
- **LynZ** answers a voice query about production status → pulls data from tenant's shared Sheets

## Setup & Authentication

### Install the CLI

```bash
npm install -g @googleworkspace/cli
```

### Per-Tenant Authentication (NemoClaw Isolation)

Each tenant's Google credentials must be isolated within their NemoClaw OpenShell sandbox. Never share credentials across tenants.

**Service Account (recommended for production):**
```bash
# Set per-sandbox environment variable
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/sandbox/credentials/tenant_${TENANT_ID}/service_account.json

# Verify access
gws drive files list --params '{"pageSize": 1}'
```

**OAuth 2.0 (for tenant self-service setup):**
```bash
gws auth setup          # First-time: creates OAuth client
gws auth login           # Interactive consent flow
gws auth export --unmasked > /sandbox/credentials/tenant_${TENANT_ID}/oauth.json
```

**Security constraints (OpenShell policy):**
- Credentials encrypted at rest (AES-256-GCM, OS keyring)
- Each agent sandbox gets read-only access to its tenant's credential file
- Network policy: only `*.googleapis.com` endpoints allowed from sandbox
- Model Armor sanitization on all responses: `--sanitize` flag enabled by default

### MCP Server Mode

For agents that support MCP (Model Context Protocol), expose Workspace APIs as structured tools:

```bash
gws mcp
```

This starts the MCP server, making all Workspace APIs available as callable tools with structured JSON input/output.

## Core Commands by Service

### Gmail — Agent Email Operations

Read the reference file `references/gmail.md` for full patterns including triage, threading, and attachment handling.

```bash
# Send (agent notifications, PO confirmations, quality alerts)
gws gmail +send --to "supplier@example.com" --subject "PO #12847 — Mango Puree" --body "..."

# Reply in thread (keeps conversation context)
gws gmail +reply --message-id MSG_ID --body "Confirmed delivery window: March 25-27"

# Read and triage (process supplier responses, customer complaints)
gws gmail +triage

# Search (find related correspondence)
gws gmail messages list --params '{"q": "from:supplier@example.com subject:PO after:2026/03/01"}'

# Watch for new messages (webhook trigger)
gws gmail +watch --topic "projects/autonomi/topics/gmail-notifications"
```

**Autonomi agent mapping:**
| Agent | Gmail Use Case |
|-------|---------------|
| Procurement Agent | Send PO emails, receive supplier confirmations |
| Quality Agent | Send hold notifications, receive lab results |
| Settlement Agent | Send payment confirmations, receive invoices |
| AP Automation Agent | Forward approved bills, send payment reminders |
| LynZ | Draft and send emails on voice command |

### Google Drive — Document & File Management

Read `references/drive.md` for folder structure patterns and file organization.

```bash
# Upload (COAs, audit docs, compliance certificates)
gws drive +upload ./COA_batch_2847.pdf --name "COA-Batch-2847-MangoPuree" \
  --parents "FOLDER_ID"

# List files in tenant folder
gws drive files list --params '{"q": "'\''FOLDER_ID'\'' in parents", "pageSize": 20}'

# Download (retrieve supplier docs for agent processing)
gws drive files get --params '{"fileId": "FILE_ID", "alt": "media"}' > downloaded_file.pdf

# Create folder structure per tenant
gws drive files create --json '{"name": "Autonomi-QC-Reports", "mimeType": "application/vnd.google-apps.folder"}'
```

**Recommended tenant folder structure:**
```
Autonomi/
├── Procurement/
│   ├── POs/
│   ├── Supplier-Contracts/
│   └── COAs/
├── Quality/
│   ├── Batch-Reports/
│   ├── Hold-Notices/
│   └── Audit-Docs/
├── Production/
│   ├── Schedules/
│   ├── Yield-Reports/
│   └── BOM-Exports/
├── Compliance/
│   ├── FSMA-204/
│   ├── SQF-Audit/
│   └── Recall-Records/
└── Finance/
    ├── Invoices/
    ├── BILL-com-Exports/
    └── Cost-Reports/
```

### Google Sheets — Data Sync & Dashboards

Read `references/sheets.md` for formula patterns, data validation, and dashboard templates.

```bash
# Read data (pull tenant operational data)
gws sheets spreadsheets values get \
  --params '{"spreadsheetId": "SHEET_ID", "range": "Inventory!A1:H100"}'

# Append row (log agent decisions, add inventory records)
gws sheets +append --spreadsheet SHEET_ID \
  --values "2026-03-20,Mango Puree,Lot-2847,1200,lbs,Received,QC-Pending"

# Batch update (sync full dataset)
gws sheets spreadsheets values batchUpdate --params '{"spreadsheetId": "SHEET_ID"}' \
  --json '{"valueInputOption": "USER_ENTERED", "data": [{"range": "A2:H50", "values": [...]}]}'

# Create new spreadsheet (auto-generate report templates)
gws sheets spreadsheets create --json '{"properties": {"title": "Weekly Production Report - W12"}}'
```

**Common Autonomi ↔ Sheets sync patterns:**
| Autonomi Data | Sheets Location | Sync Direction | Frequency |
|---------------|----------------|----------------|-----------|
| Inventory levels | `Inventory!A:H` | Autonomi → Sheets | Hourly |
| Production schedule | `Production!A:F` | Bi-directional | Real-time on change |
| Quality results | `QC-Log!A:J` | Autonomi → Sheets | On test completion |
| Supplier scorecard | `Suppliers!A:G` | Autonomi → Sheets | Weekly |
| BOM cost rollup | `BOM-Costs!A:L` | Autonomi → Sheets | On ingredient price change |
| Agent decisions | `Agent-Log!A:I` | Autonomi → Sheets | Real-time |
| BILL.com payment status | `AP-Tracker!A:H` | BILL.com → Autonomi → Sheets | On payment event |

### Google Docs — Document Generation

Read `references/docs.md` for template patterns and structured document creation.

```bash
# Write to existing doc (populate a template)
gws docs +write --document DOC_ID --text "## Batch Report: Lot 2847\n\nProduct: Mango Puree 500ml..."

# Create new doc
gws docs documents create --json '{"title": "QC Hold Notice - Lot 2847"}'

# Read doc content (parse supplier specs, SOPs)
gws docs documents get --params '{"documentId": "DOC_ID"}'
```

**Agent-generated document types:**
- Quality hold notices (Quality Agent)
- Batch traceability reports (Recall Agent)
- Supplier performance summaries (Procurement Agent)
- Production yield reports (Production Agent)
- FSMA 204 CTE records (Compliance Agent)
- Cost variance reports (Finance Agent)
- Weekly operational summaries (LynZ)

### Google Calendar — Scheduling & Coordination

Read `references/calendar.md` for scheduling patterns and timezone handling.

```bash
# View agenda (check production schedule conflicts)
gws calendar +agenda

# Create event (schedule QC inspection, supplier call, production run)
gws calendar +insert --title "QC Inspection - Lot 2847 Mango Puree" \
  --start-time "2026-03-22T09:00:00" \
  --end-time "2026-03-22T10:00:00" \
  --description "Triggered by Quality Agent: pH out of spec on sample 3"

# Invite attendees
gws calendar events patch --params '{"calendarId": "primary", "eventId": "EVT_ID"}' \
  --json '{"attendees": [{"email": "qa_manager@tenant.com"}]}'
```

**Agent → Calendar triggers:**
| Agent Event | Calendar Action |
|------------|----------------|
| Ingredient delivery ETA confirmed | Create "Receiving & QC" event |
| Batch hold issued | Schedule "Hold Review" meeting |
| Production schedule updated | Update/create production run events |
| Supplier contract renewal approaching | Create "Contract Review" reminder |
| BILL.com payment due | Create "Payment Due" reminder |
| FSMA mock recall due | Schedule "Mock Recall Drill" |

### Google Meet — Video Collaboration

```bash
# Auto-create Meet link for scheduled events
# (Calendar events with conferenceData get auto-generated Meet links)
gws calendar events insert --params '{"calendarId": "primary", "conferenceDataVersion": 1}' \
  --json '{"summary": "Supplier QBR", "conferenceData": {"createRequest": {"requestId": "unique-id"}}}'
```

### LynZ Voice Agent — Google Workspace via Natural Language

LynZ is Autonomi's voice-first assistant and the most frequent Google Workspace user. Operators interact conversationally — "send that PO," "what's on the calendar," "pull up the QC numbers." LynZ needs broad read access across all services plus Gmail send.

**Voice → GWS command mapping:**

```bash
# "What emails came in from our mango supplier?"
gws gmail messages list --params '{"q": "from:supplier@example.com newer_than:7d"}'

# "What's on the production calendar today?"
gws calendar +agenda

# "Pull up the latest inventory numbers"
gws sheets spreadsheets values get --params '{"spreadsheetId": "SHEET_ID", "range": "Inventory!A1:H50"}'

# "Send that PO to the supplier"
gws gmail +send --to "supplier@example.com" --subject "PO #12847" --body "..."

# "Schedule a QC review for tomorrow at 9"
gws calendar +insert --title "QC Review - Batch 2847" --start-time "2026-03-22T09:00:00"

# "Email the QC report to the plant manager"
gws gmail +send --to "plant_manager@tenant.com" --subject "Batch 2847 QC Report" \
  --attachment /sandbox/workspace/reports/batch_2847_report.pdf
```

**LynZ-specific rules:**
- All email sends require voice confirmation ("Should I send this?")
- Read-only access to Sheets, Docs, and Drive — LynZ reports data but doesn't modify it
- Calendar event creation delegated to scheduling agents unless user explicitly asks LynZ
- All GWS content screened through Model Armor before processing (LynZ's broad read scope makes her a high-value injection target)
- Summarize data for voice output — don't dump raw spreadsheet values

**LynZ tool definitions (for voice agent tool registry):**

Add these to LynZ's system prompt / OpenAI Realtime tool definitions so she can call them during voice sessions:

```json
[
  {
    "name": "gws_gmail_search",
    "description": "Search tenant Gmail for messages matching a query",
    "parameters": {"query": "string", "max_results": "number"}
  },
  {
    "name": "gws_gmail_send",
    "description": "Send an email. Always confirm with user before executing.",
    "parameters": {"to": "string", "subject": "string", "body": "string", "attachment_path": "string"}
  },
  {
    "name": "gws_calendar_agenda",
    "description": "Get today's calendar events or events for a specified date",
    "parameters": {"date": "string"}
  },
  {
    "name": "gws_calendar_create",
    "description": "Create a calendar event with optional Meet link",
    "parameters": {"title": "string", "start_time": "string", "end_time": "string", "attendees": "array", "meet_link": "boolean"}
  },
  {
    "name": "gws_sheets_read",
    "description": "Read data from a tenant Google Sheet by name or ID",
    "parameters": {"sheet_name": "string", "range": "string"}
  },
  {
    "name": "gws_docs_read",
    "description": "Read content from a tenant Google Doc",
    "parameters": {"doc_name": "string"}
  },
  {
    "name": "gws_drive_search",
    "description": "Search tenant Google Drive for files by name or content",
    "parameters": {"query": "string", "folder": "string"}
  }
]
```

When LynZ migrates to server-side orchestration (Phase 2.4), these tools call the `gws` CLI on the backend. In the current prototype, they can be simulated with mock responses.

### Google Chat — Team Notifications

```bash
# Send to Chat space (real-time agent alerts to team channels)
gws chat spaces messages create --params '{"parent": "spaces/SPACE_ID"}' \
  --json '{"text": "⚠️ Quality Alert: Batch 2847 placed on hold. pH reading 3.2 (spec: 3.5-4.0). QC inspection scheduled for 9am tomorrow."}'
```

## Security Architecture (NemoClaw Integration)

This is the critical section for Autonomi's multi-tenant security model. Read `references/security.md` for full OpenShell policy templates.

### Credential Isolation

```yaml
# OpenShell policy for Google Workspace agent sandbox
filesystem:
  read:
    - /sandbox/credentials/tenant_${TENANT_ID}/  # Only this tenant's creds
    - /sandbox/workspace/                          # Agent working directory
  write:
    - /sandbox/workspace/                          # Temp files only
  deny:
    - /sandbox/credentials/tenant_*/               # Block cross-tenant access

network:
  allow:
    - "*.googleapis.com:443"                       # Google APIs only
    - "oauth2.googleapis.com:443"                  # Token refresh
  deny:
    - "*"                                          # Everything else blocked

process:
  allow:
    - gws                                          # CLI binary
    - node                                         # For npm-based CLI
  deny:
    - curl                                         # No raw HTTP
    - wget                                         # No raw downloads
```

### Model Armor Integration

Every `gws` response should be sanitized before agent processing to prevent prompt injection from Google Workspace content (malicious email bodies, tampered document text):

```bash
# Enable per-command sanitization
gws gmail messages get --params '{"id": "MSG_ID"}' \
  --sanitize "projects/autonomi/locations/us-central1/templates/email-sanitizer"
```

This connects to the Prompt Injection Detection Engine (Phase 2.3 in execution plan).

### Scope Minimization

Each agent type gets only the Google API scopes it needs:

| Agent | Required Scopes |
|-------|----------------|
| Procurement Agent | `gmail.send`, `gmail.readonly`, `drive.file`, `sheets` |
| Quality Agent | `gmail.send`, `docs`, `drive.file`, `calendar.events` |
| Inventory Agent | `sheets`, `drive.readonly` |
| Settlement Agent | `gmail.send`, `sheets.readonly` |
| LynZ | `gmail.send`, `gmail.readonly`, `calendar.readonly`, `sheets.readonly`, `docs.readonly`, `drive.readonly` |

## Error Handling & Retry

Google APIs have rate limits and occasional transient failures. Agents should handle these gracefully:

```bash
# Rate limit (429) → exponential backoff
# Auth expired (401) → auto-refresh token, retry once
# Not found (404) → log and notify, don't retry
# Server error (500/503) → retry with backoff, max 3 attempts
```

The `gws` CLI handles basic retry automatically. For agent-level orchestration, log failures to the `agent_decisions` table with `error_type` and `retry_count`.

## Scripts

Bundled scripts in `scripts/` automate common multi-step workflows:

- `scripts/sync_inventory_to_sheets.py` — Full inventory sync from Autonomi DB → Google Sheets
- `scripts/generate_batch_report.py` — Create Google Doc batch report from lot/batch data
- `scripts/setup_tenant_workspace.py` — Initialize Drive folder structure + Sheets templates for new tenant
- `scripts/gmail_webhook_processor.py` — Process incoming Gmail notifications → route to appropriate agent

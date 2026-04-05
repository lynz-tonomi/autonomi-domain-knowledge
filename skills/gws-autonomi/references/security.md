# Google Workspace Security Reference — NemoClaw Integration

## Table of Contents
1. [Credential Isolation](#credential-isolation)
2. [OpenShell Policy Templates](#openshell-policy-templates)
3. [Scope Minimization](#scope-minimization)
4. [Model Armor Integration](#model-armor-integration)
5. [Audit Logging](#audit-logging)
6. [Incident Response](#incident-response)

## Credential Isolation

### Per-Tenant Credential Storage
Each tenant's Google Workspace credentials live in an isolated directory accessible only from that tenant's NemoClaw sandbox:

```
/sandbox/credentials/
├── tenant_001/
│   ├── service_account.json    # Service account key
│   ├── oauth_token.json        # Cached OAuth tokens
│   └── config.json             # Tenant-specific settings (default calendar, drive folder IDs)
├── tenant_002/
│   └── ...
```

### Service Account Setup (Production)
1. Tenant admin creates a GCP project (or Autonomi provisions one)
2. Create service account with domain-wide delegation
3. Grant only required scopes (see Scope Minimization below)
4. Download key → encrypt → store in tenant credential directory
5. OpenShell policy restricts access to only this tenant's directory

### Token Refresh Handling
OAuth tokens expire after 1 hour. The `gws` CLI handles auto-refresh, but agents must handle edge cases:
- **Token refresh fails** → log error, notify tenant admin, pause non-critical operations
- **Service account key rotated** → Autonomi admin console triggers credential update in sandbox
- **Credentials revoked by tenant** → all agent operations fail gracefully, alert Autonomi ops team

## OpenShell Policy Templates

### Procurement Agent — Google Workspace Access
```yaml
# openshell-policy-procurement-gws.yaml
name: procurement-agent-gws
description: Google Workspace access policy for Procurement Agent

filesystem:
  read:
    - /sandbox/credentials/tenant_${TENANT_ID}/service_account.json
    - /sandbox/credentials/tenant_${TENANT_ID}/config.json
    - /sandbox/workspace/procurement/
  write:
    - /sandbox/workspace/procurement/tmp/    # Temp files for upload
  deny:
    - /sandbox/credentials/tenant_*/          # No cross-tenant access
    - /sandbox/workspace/quality/             # No cross-agent data access
    - /sandbox/workspace/finance/

network:
  allow:
    - "gmail.googleapis.com:443"
    - "www.googleapis.com:443"
    - "sheets.googleapis.com:443"
    - "drive.googleapis.com:443"
    - "oauth2.googleapis.com:443"
  deny:
    - "docs.googleapis.com:443"              # Procurement doesn't need Docs
    - "calendar-json.googleapis.com:443"     # Procurement doesn't need Calendar
    - "*"

process:
  allow:
    - gws
    - node
    - python3                                 # For bundled scripts
  deny:
    - curl
    - wget
    - ssh

inference:
  local_model: nemotron-3-super              # Primary reasoning
  screening_model: nemotron-3-nano-4b        # Prompt injection screening
  cloud_allowed: false                        # No cloud model for procurement (sensitive pricing data)
```

### Quality Agent — Google Workspace Access
```yaml
name: quality-agent-gws

filesystem:
  read:
    - /sandbox/credentials/tenant_${TENANT_ID}/
    - /sandbox/workspace/quality/
  write:
    - /sandbox/workspace/quality/tmp/

network:
  allow:
    - "gmail.googleapis.com:443"
    - "docs.googleapis.com:443"
    - "drive.googleapis.com:443"
    - "calendar-json.googleapis.com:443"
    - "oauth2.googleapis.com:443"
  deny:
    - "sheets.googleapis.com:443"             # Quality uses Docs, not Sheets for reports
    - "*"

inference:
  local_model: nemotron-3-super
  screening_model: nemotron-3-nano-4b
  cloud_allowed: false                         # QC data is sensitive
```

### LynZ — Google Workspace Access (Read-Heavy)
```yaml
name: lynz-voice-agent-gws

filesystem:
  read:
    - /sandbox/credentials/tenant_${TENANT_ID}/
    - /sandbox/workspace/                       # Read across all agent workspaces
  write:
    - /sandbox/workspace/lynz/tmp/

network:
  allow:
    - "gmail.googleapis.com:443"
    - "sheets.googleapis.com:443"
    - "docs.googleapis.com:443"
    - "drive.googleapis.com:443"
    - "calendar-json.googleapis.com:443"
    - "oauth2.googleapis.com:443"
  deny:
    - "*"

inference:
  local_model: nemotron-3-super
  screening_model: nemotron-3-nano-4b
  cloud_allowed: true                           # LynZ may use cloud for voice (OpenAI Realtime)
```

## Scope Minimization

### Principle
Each agent type gets the minimum Google API scopes required for its function. Broad scopes like `https://www.googleapis.com/auth/drive` (full Drive access) should be avoided in favor of narrow scopes like `https://www.googleapis.com/auth/drive.file` (only files created by the app).

### Scope Matrix

| Agent | Gmail | Drive | Sheets | Docs | Calendar | Chat | Admin |
|-------|-------|-------|--------|------|----------|------|-------|
| Procurement | send, readonly | file | full | — | — | — | — |
| Quality | send | file | — | full | events | — | — |
| Inventory | — | readonly | full | — | — | — | — |
| Settlement | send | readonly | readonly | — | — | — | — |
| Recall | send | file | readonly | full | events | send | — |
| Compliance | — | file | readonly | full | — | — | — |
| AP Automation | send, readonly | file | full | — | events | — | — |
| LynZ | send, readonly | readonly | readonly | readonly | readonly | — | — |
| IoT Monitor | — | — | full | — | — | send | — |
| Maintenance | — | — | — | — | events | send | — |

### Scope URIs Reference
```
# Gmail
gmail.send                    = https://www.googleapis.com/auth/gmail.send
gmail.readonly                = https://www.googleapis.com/auth/gmail.readonly

# Drive
drive.file                    = https://www.googleapis.com/auth/drive.file
drive.readonly                = https://www.googleapis.com/auth/drive.readonly

# Sheets
sheets                        = https://www.googleapis.com/auth/spreadsheets
sheets.readonly               = https://www.googleapis.com/auth/spreadsheets.readonly

# Docs
docs                          = https://www.googleapis.com/auth/documents
docs.readonly                 = https://www.googleapis.com/auth/documents.readonly

# Calendar
calendar.events               = https://www.googleapis.com/auth/calendar.events
calendar.readonly             = https://www.googleapis.com/auth/calendar.readonly

# Chat
chat.messages.create          = https://www.googleapis.com/auth/chat.messages.create
```

## Model Armor Integration

All content read from Google Workspace (email bodies, document text, sheet data) passes through the Prompt Injection Detection Engine (Phase 2.3) before agent processing:

```bash
# Per-command sanitization
gws gmail messages get --params '{"id": "MSG_ID"}' \
  --sanitize "projects/autonomi/locations/us-central1/templates/gws-input-sanitizer"

# Template configuration
# - Blocks: prompt injection patterns, instruction-hijacking attempts
# - Allows: normal business content, F&B terminology, numeric data
# - Logs: all flagged content to audit trail
```

### Threat Scenarios
1. **Malicious email body** — supplier sends email with embedded instructions to exfiltrate pricing data
2. **Tampered spreadsheet** — attacker modifies shared sheet with prompt injection in cell values
3. **Poisoned document** — Google Doc shared with agent contains hidden instructions in white text
4. **Calendar invite injection** — meeting description contains instructions to bypass approval workflows

All scenarios are mitigated by Model Armor screening + the Prompt Injection Detection Engine running on Nemotron 3 Nano 4B locally.

## Audit Logging

Every Google Workspace operation performed by an agent is logged:

```json
{
  "timestamp": "2026-03-20T14:32:01Z",
  "tenant_id": "tenant_001",
  "agent_id": "procurement-agent",
  "service": "gmail",
  "operation": "send",
  "target": "supplier@example.com",
  "subject": "PO #12847",
  "decision_id": "dec_abc123",
  "trust_chain": ["user_auth_001", "policy_procurement_send", "agent_procurement"],
  "sanitization_result": "clean",
  "status": "success"
}
```

Logs are written to `agent_decisions` table and optionally anchored to Base L2 blockchain for immutability.

## Incident Response

### Credential Compromise
1. Immediately revoke compromised service account key in GCP Console
2. Rotate all tokens in affected tenant sandbox
3. Audit all GWS operations from compromised credential (last 30 days)
4. Notify tenant admin
5. Generate incident report (Google Doc in Compliance/Incident-Reports/)

### Prompt Injection Detected
1. Block the input (Model Armor / Nemotron classifier)
2. Log full content to audit trail with threat classification
3. Quarantine source (mark email as suspicious, flag document)
4. Alert security team via Google Chat
5. Add pattern to adversarial test library (Phase 4.5)

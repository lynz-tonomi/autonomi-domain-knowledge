# Microsoft 365 Security Reference — NemoClaw Integration

## Table of Contents
1. [Credential Isolation](#credential-isolation)
2. [OpenShell Policy Templates](#openshell-policy-templates)
3. [Scope Minimization](#scope-minimization)
4. [Model Armor Integration](#model-armor-integration)
5. [Audit Logging](#audit-logging)
6. [Incident Response](#incident-response)

## Credential Isolation

### Per-Tenant Credential Storage
Each tenant's M365 credentials live in an isolated directory accessible only from that tenant's NemoClaw sandbox:

```
/sandbox/credentials/
├── tenant_001/
│   ├── cert.pem              # Client certificate
│   ├── key.pem               # Private key
│   ├── token_cache.json      # MSAL token cache (auto-managed)
│   └── config.json           # Tenant-specific settings (site IDs, team IDs, channel IDs)
├── tenant_002/
│   └── ...
```

### App Registration Setup (Production)
1. Tenant admin creates app registration in Entra ID (Azure AD)
2. Upload a certificate (no client secrets in production)
3. Grant only required Graph API permissions per agent (see Scope Minimization)
4. Admin grants consent for application permissions
5. Certificate + private key → encrypt → store in tenant credential directory
6. OpenShell policy restricts access to only this tenant's directory

### Token Lifecycle
MSAL handles token caching and refresh automatically. Edge cases agents must handle:
- **Token acquisition fails** → log error, notify tenant admin, pause non-critical operations
- **Certificate rotated** → Autonomi admin console triggers credential update in sandbox
- **App registration deleted/disabled by tenant** → all agent operations fail gracefully, alert Autonomi ops team
- **Consent revoked** → Graph API returns 403 on all calls, trigger re-consent flow

## OpenShell Policy Templates

### Procurement Agent — M365 Access
```yaml
# openshell-policy-procurement-m365.yaml
name: procurement-agent-m365
description: Microsoft 365 access policy for Procurement Agent

filesystem:
  read:
    - /sandbox/credentials/tenant_${TENANT_ID}/cert.pem
    - /sandbox/credentials/tenant_${TENANT_ID}/key.pem
    - /sandbox/credentials/tenant_${TENANT_ID}/config.json
    - /sandbox/workspace/procurement/
  write:
    - /sandbox/workspace/procurement/tmp/     # Temp files for upload
  deny:
    - /sandbox/credentials/tenant_*/           # No cross-tenant access
    - /sandbox/workspace/quality/              # No cross-agent data access
    - /sandbox/workspace/finance/

network:
  allow:
    - "graph.microsoft.com:443"
    - "login.microsoftonline.com:443"          # Auth endpoint
    - "*.sharepoint.com:443"                   # SharePoint file operations
  deny:
    - "*"

process:
  allow:
    - python3                                  # For bundled scripts
    - pwsh                                     # PowerShell Core
  deny:
    - curl
    - wget
    - ssh

inference:
  local_model: nemotron-3-super
  screening_model: nemotron-3-nano-4b
  cloud_allowed: false                         # No cloud model (sensitive pricing data)
```

### Quality Agent — M365 Access
```yaml
name: quality-agent-m365

filesystem:
  read:
    - /sandbox/credentials/tenant_${TENANT_ID}/
    - /sandbox/workspace/quality/
  write:
    - /sandbox/workspace/quality/tmp/

network:
  allow:
    - "graph.microsoft.com:443"
    - "login.microsoftonline.com:443"
    - "*.sharepoint.com:443"
  deny:
    - "*"

inference:
  local_model: nemotron-3-super
  screening_model: nemotron-3-nano-4b
  cloud_allowed: false                          # QC data is sensitive
```

### LynZ — M365 Access (Read-Heavy)
```yaml
name: lynz-voice-agent-m365

filesystem:
  read:
    - /sandbox/credentials/tenant_${TENANT_ID}/
    - /sandbox/workspace/                        # Read across all agent workspaces
  write:
    - /sandbox/workspace/lynz/tmp/

network:
  allow:
    - "graph.microsoft.com:443"
    - "login.microsoftonline.com:443"
    - "*.sharepoint.com:443"
  deny:
    - "*"

inference:
  local_model: nemotron-3-super
  screening_model: nemotron-3-nano-4b
  cloud_allowed: true                            # LynZ may use cloud for voice (OpenAI Realtime)
```

## Scope Minimization

### Principle
Each agent type gets the minimum Microsoft Graph API permissions required. Broad permissions like `Files.ReadWrite.All` (full SharePoint/OneDrive access) should be avoided in favor of narrow permissions like `Files.ReadWrite.Selected` when possible, or scoped to specific site collections via SharePoint site permissions.

### Permission Matrix

| Agent | Mail | Files (SP/OD) | Teams | Calendar | Notes |
|-------|------|--------------|-------|----------|-------|
| Procurement | Mail.Send, Mail.Read | Files.ReadWrite.All | ChannelMessage.Send | — | SP scoped to Procurement site |
| Quality | Mail.Send | Files.ReadWrite.All | ChannelMessage.Send | Calendars.ReadWrite | SP scoped to Quality site |
| Inventory | — | Files.Read.All | ChannelMessage.Send | — | Read-only SP access |
| Settlement | Mail.Send | Files.Read.All | — | — | Read-only SP access |
| Recall | Mail.Send | Files.ReadWrite.All | ChannelMessage.Send | Calendars.ReadWrite | Broad access for traceability |
| Compliance | — | Files.ReadWrite.All | — | — | SP scoped to Compliance site |
| AP Automation | Mail.Send, Mail.Read | Files.ReadWrite.All | ChannelMessage.Send | Calendars.ReadWrite | — |
| LynZ | Mail.Send, Mail.Read | Files.Read.All | ChannelMessage.Send | Calendars.Read | Read-heavy, send-limited |
| IoT Monitor | — | — | ChannelMessage.Send | — | Teams alerts only |
| Maintenance | — | — | ChannelMessage.Send | Calendars.ReadWrite | — |

### Graph API Permission Reference
```
# Mail
Mail.Send               = Send mail as the app
Mail.Read               = Read mail in all mailboxes
Mail.ReadWrite          = Read and write mail in all mailboxes

# Files (SharePoint / OneDrive)
Files.Read.All          = Read all files (all sites)
Files.ReadWrite.All     = Read and write all files
Sites.Read.All          = Read items in all site collections
Sites.ReadWrite.All     = Read and write items in all site collections

# Teams
ChannelMessage.Send     = Send channel messages
Team.ReadBasic.All      = Read team names and descriptions
Channel.ReadBasic.All   = Read channel names

# Calendar
Calendars.Read          = Read calendars in all mailboxes
Calendars.ReadWrite     = Create and update events in all mailboxes

# Users (for lookups)
User.Read.All           = Read all users' full profiles
```

## Model Armor Integration

All content read from M365 (email bodies, document text, Excel data, Teams messages) passes through the Prompt Injection Detection Engine (Phase 2.3) before agent processing:

```python
# Sanitization wrapper for Graph API reads
def sanitized_graph_get(url, headers):
    """Fetch from Graph API and screen through Model Armor."""
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Screen text fields through injection detector
    text_content = extract_text_fields(data)
    screening_result = model_armor_screen(text_content)

    if screening_result["flagged"]:
        log_security_event("prompt_injection_detected", {
            "source": url,
            "flagged_content": screening_result["flagged_segments"],
            "confidence": screening_result["confidence"]
        })
        raise SecurityError(f"Potential prompt injection detected in M365 content: {url}")

    return data
```

### Threat Scenarios
1. **Malicious email body** — supplier sends email with embedded instructions to exfiltrate pricing data
2. **Tampered Excel cells** — attacker modifies shared workbook with prompt injection in cell values
3. **Poisoned Word document** — SharePoint doc contains hidden instructions in white text or comments
4. **Calendar invite injection** — meeting description contains instructions to bypass approval workflows
5. **Teams message injection** — channel message contains instructions targeting LynZ voice agent

All scenarios are mitigated by Model Armor screening + the Prompt Injection Detection Engine running on Nemotron 3 Nano 4B locally.

## Audit Logging

Every M365 operation performed by an agent is logged:

```json
{
  "timestamp": "2026-03-20T14:32:01Z",
  "tenant_id": "tenant_001",
  "agent_id": "procurement-agent",
  "service": "outlook",
  "operation": "sendMail",
  "target": "supplier@example.com",
  "subject": "PO #12847",
  "decision_id": "dec_abc123",
  "trust_chain": ["entra_app_001", "policy_procurement_send", "agent_procurement"],
  "sanitization_result": "clean",
  "graph_request_id": "req_xyz789",
  "status": "success"
}
```

Logs are written to `agent_decisions` table and optionally anchored to Base L2 blockchain for immutability.

## Incident Response

### Credential Compromise
1. Immediately disable the compromised app registration in Entra ID
2. Rotate all certificates in affected tenant sandbox
3. Review Graph API audit logs for unauthorized operations (Entra ID → Audit Logs)
4. Notify tenant admin
5. Generate incident report (Word doc in Compliance/Incident-Reports/)

### Prompt Injection Detected
1. Block the input (Model Armor / Nemotron classifier)
2. Log full content to audit trail with threat classification
3. Quarantine source (mark email as suspicious, flag document in SharePoint)
4. Alert security team via Teams #alerts-critical channel
5. Add pattern to adversarial test library (Phase 4.5)

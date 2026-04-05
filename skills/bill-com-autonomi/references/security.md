# Security Reference — BILL.com Integration for Autonomi

## NemoClaw Sandbox Isolation

### OpenShell Policy

Each Autonomi tenant runs in an isolated NemoClaw sandbox. The BILL.com integration operates under these constraints:

- **Network egress**: Only allowed to BILL.com API domains (`gateway.stage.bill.com`, `gateway.prod.bill.com`, `api-sandbox.bill.com`, `api.bill.com`)
- **File system**: Read-only except for designated state directories (`/tmp/bill_*`, NemoClaw config paths)
- **Process isolation**: Each agent runs in its own container; no cross-tenant access

### Credential Storage

BILL.com credentials are stored per-tenant in the NemoClaw vault:

```
/opt/nemoclaw/secrets/
  bill_credentials.json    # username, password, developer_key, organization_id
  bill_mfa_state.json      # rememberMeId, device (for MFA persistence)
  bill_webhook_secret.json # HMAC secret for webhook verification
```

**Environment variable fallback**:
- `BILL_USERNAME` — BILL account email
- `BILL_PASSWORD` — BILL account password
- `BILL_DEV_KEY` — Developer key (generated in BILL Settings > Sync & Integrations)
- `BILL_ORG_ID` — Organization ID (begins with `008`)

Credentials are never logged, never included in webhook payloads, and never passed to Model Armor screening.

## Authentication Security

### Session Management

- Sessions are obtained via `POST /v3/login` and cached locally
- Session IDs rotate on re-authentication
- Proactive refresh before 30-minute timeout
- On 401 response, session is invalidated and re-authenticated automatically

### MFA Requirements

Payment operations (`POST /v3/payments`, `POST /v3/payments/bulk`) require MFA-trusted sessions in production:

1. One-time setup: `POST /v3/mfa/challenge` + `POST /v3/mfa/challenge/validate`
2. Subsequent logins: include `rememberMeId` and `device` to skip MFA
3. Step-up: `POST /v3/mfa/step-up` if session was created without MFA

MFA state (`rememberMeId`, `device`) is stored in NemoClaw vault and reused across sessions.

### API Key Security

- **Developer key** (`devKey`): Passed as header on every v3 API call. Generated per-org in BILL Settings.
- **Sync token** (partner mode): Alternative to password for `POST /v3/login`. Generated in BILL Settings > Sync & Integrations > Tokens.
- **API token** (S&E only): Used in `apiToken` header for Spend & Expense endpoints. No login required.

Keys are never:
- Stored in source code
- Included in log messages
- Passed through Model Armor screening
- Shared across tenants

## Model Armor Integration

### Prompt Injection Screening

All text data ingested from BILL.com API responses is screened through Model Armor before being processed by Autonomi agents. This protects against adversarial content embedded in vendor-submitted data.

### Screening Pipeline

1. BILL API response received by `bill_session.py`
2. Text fields extracted: `description`, `vendorName`, line item `description`, `invoiceNumber`
3. Each field passed to `ModelArmor.screenPrompt(field_value)`
4. **If injection detected**: field quarantined, agent alerted, bill flagged for human review
5. **If clean**: data passed to agent for normal processing

### Fields Screened

| Source | Fields |
|--------|--------|
| Bills | `description`, `billLineItems[].description`, `invoice.invoiceNumber` |
| Vendors | `name`, `email`, `address` fields |
| Payments | `description` |
| Vendor Credits | `description`, `vendorCreditLineItems[].description`, `referenceNumber` |
| Webhooks | All string fields in event payload |

### Bypass Rules

These fields are **not** screened (numeric/system-generated, no injection risk):
- Entity IDs (`id`, `vendorId`, `billId`, etc.)
- Dates (`dueDate`, `processDate`, `createdTime`, `updatedTime`)
- Amounts (`amount`, `fundingAmount`, `exchangeRate`)
- Status enums (`paymentStatus`, `approvalStatus`, `status`)
- System fields (`transactionNumber`, `confirmationNumber`)

## Agent Permission Matrix

Each Autonomi agent has scoped BILL.com API access:

| Agent | Can Read | Can Write | Approval Actions | Payment Actions |
|-------|----------|-----------|-----------------|-----------------|
| Procurement | Bills, Vendors | — | APPROVE, DENY | — |
| Quality | Bills, Vendors, Vendor Credits | — | APPROVE, DENY | — |
| AP/Finance | Bills, Vendors, Vendor Credits, Bank Accounts | Bills (apply credits) | APPROVE, DENY | Create payments |
| Settlement | Bills, Vendors, Vendor Credits, Payments | Bills, Vendor Credits | APPROVE, DENY | Create, void payments |

### Permission Enforcement

Permissions are enforced at two levels:

1. **BILL.com user roles**: Each agent maps to a BILL user with the appropriate role (Administrator, Accountant, or Approver). BILL enforces role-based access server-side.
2. **NemoClaw policy**: The sandbox policy restricts which API endpoints each agent container can reach, providing defense-in-depth.

### Required BILL User Roles for Approval Operations

| Role | Can Create Policies | Can Approve/Deny | Can Create Payments |
|------|-------------------|-----------------|-------------------|
| Administrator | Yes | Yes | Yes |
| Accountant | No | Yes | Yes |
| Approver | No | Yes | No |

## Webhook Security

### Signature Verification

Incoming webhook payloads are verified using HMAC-SHA256:

1. Extract signature from webhook header
2. Compute HMAC-SHA256 of raw payload body using the stored webhook secret
3. Compare using constant-time comparison (`hmac.compare_digest`)
4. Reject if signature doesn't match

### Event Validation

Before processing any webhook event:

1. Verify the event type is in the expected set (see `APPROVAL_EVENTS` in `webhook_handler.py`)
2. Validate entity IDs match expected prefixes (`00n` for bills, `009` for vendors, `stp` for payments)
3. Screen all text fields through Model Armor
4. Only then dispatch to agent handlers

### Idempotency

Webhook events may be delivered more than once. The handler maintains a processed-event cache to ensure idempotent processing. Duplicate events are logged and skipped.

## Error Code Reference

| Code | Meaning | Security Implication |
|------|---------|---------------------|
| 401 | Unauthorized / session expired | Re-authenticate, do not retry with same session |
| 403 | Forbidden | User lacks required role — escalate, do not retry |
| 429 | Rate limited | Backoff, respect Retry-After header |
| `BDC_1205` | Entity not found | May indicate stale data — refresh and retry |
| `BDC_1246` | Bulk rollback | Transactional failure — investigate root cause |
| `BDC_1159` | Cannot overpay | Logic error — verify amounts before payment |

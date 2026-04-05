---
name: bill-com-autonomi
description: >
  BILL.com AP integration for Autonomi — connects agents to tenant BILL.com accounts via
  BILL API (v2 + v3) for invoice approval workflows. Handles bill ingestion, approval chain
  routing, approver assignment (SetApprovers), approval/rejection, status tracking, approval
  policies, webhooks, vendor credits, and bulk operations. Built for NemoClaw sandboxes with
  per-tenant credential isolation. ALWAYS trigger on: BILL.com, Bill.com, bill approval,
  invoice approval, AP approval, SetApprovers, approval chain, approval policy, pending
  approvals, approve bill, reject bill, bill routing, approval status, AP automation with
  BILL, BILL API, bill-com, webhook, vendor credit, bulk bills, bulk payments, or any
  agent workflow involving invoice approval — even if BILL.com isn't explicitly named.
---

# BILL.com Invoice Approval Integration for Autonomi

This skill enables Autonomi agents to manage invoice approval workflows through the BILL.com API. The focus is the approval lifecycle — from the moment a bill lands in BILL.com to the moment it's fully approved and ready for payment. Multiple Autonomi agents (Procurement, Quality, Finance/AP, Settlement) can participate in the approval chain, each with scoped permissions appropriate to their role.

## Why this matters

In food & beverage manufacturing, invoice approvals aren't just bookkeeping — they're a quality and compliance gate. A Procurement Agent confirming a PO match, a QA Agent flagging a COA discrepancy, and an AP Agent giving final sign-off are all part of the same linear chain. Delays in any step cascade into late payments, strained vendor relationships, and potential supply disruptions. This skill gives each agent the ability to do its part in that chain without manual intervention.

## BILL.com Platform Overview

BILL.com is a cloud-based financial operations platform covering three major domains:

- **Accounts Payable (AP)** — Vendors, Bills, Bill approvals, Payments, Vendor credits. Create bills and pay vendors at scale with check, ACH, virtual card, and BILL Pay Faster disbursement methods. Supports bulk bill creation and bulk payments.
- **Accounts Receivable (AR)** — Customers, Invoices, Charge customers, Credit memos, Record payments. Generate and send invoices, charge authorized customers, record payments received outside BILL.
- **Spend & Expense (S&E)** — Budgets, Cards, Transactions, Reimbursements. Card and expense management services with virtual cards, budgets, and custom field tagging.

Additionally, the **BILL Network** connects vendor and customer organizations for electronic payment exchange (ACH, virtual card, or check based on the network vendor's configured payment method), and **Webhooks** provide real-time event notifications for BILL events.

This skill focuses on the **AP workflow** — specifically the bill approval pipeline — but awareness of the full platform is important because vendor credits, payments, and network operations are adjacent to the approval chain.

## BILL.com API Architecture

### Base URLs

The BILL v3 API uses these base URLs:

```
Sandbox API:      https://gateway.stage.bill.com/connect
Production API:   https://gateway.prod.bill.com/connect

Sandbox Webhooks:    https://gateway.stage.bill.com/connect-events
Production Webhooks: https://gateway.prod.bill.com/connect-events
```

### v2 vs v3 — When to Use Which

BILL.com maintains two API versions. The v3 API is the modern REST API — use it for all operations that have v3 endpoints.

**v3 API** — Standard REST with proper HTTP verbs (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`). JSON request/response bodies. Headers: `devKey`, `sessionId`, `content-type: application/json`. Used for: login, vendors, bills, bill approvals, payments, vendor credits, webhooks, bank accounts, and all standard AP/AR operations.

**v2 API** — Legacy API. Uses `POST` for everything with `application/x-www-form-urlencoded` encoding. Still needed for a few operations that don't yet have v3 equivalents (e.g., `SetApprovers` on individual bills outside of policy-based assignment, some reporting endpoints). Base URL: `https://api-sandbox.bill.com/api/v2` (sandbox), `https://api.bill.com/api/v2` (production).

**Rule of thumb**: Always prefer v3. Only fall back to v2 when the specific operation has no v3 equivalent.

### Authentication

Sign in with `POST /v3/login`:

```
POST https://gateway.stage.bill.com/connect/v3/login
Content-Type: application/json
devKey: {developer_key}

{
  "userName": "{username}",
  "password": "{password}",
  "orgId": "{organization_id}"
}
```

The response includes a `sessionId` that must be passed as a header in all subsequent API calls. Sessions expire after inactivity; re-authenticate when you receive a 401.

**MFA-trusted sessions**: Creating payments requires an MFA-trusted API session. The MFA flow uses `POST /v3/mfa/challenge` to initiate and `POST /v3/mfa/challenge/validate` to complete. Once trusted, pass `rememberMeId` and `device` on subsequent logins to skip MFA re-validation.

**Headers for all v3 API calls**:
```
Content-Type: application/json
devKey: {developer_key}
sessionId: {session_id}
```

### Entity ID Prefixes

BILL uses predictable prefixes for entity IDs:

| Entity | Prefix | Example |
|--------|--------|---------|
| Organization | `008` | `00801ABCDEFGHIJ` |
| User | `006` | `00601XYZUSER1234` |
| Vendor | `009` | `00901VENDORID123` |
| Bill | `00n` | `00n01BILLID12345` |
| Bill Line Item | varies | `{billLineItem_id}` |
| Payment | `stp` | `stp01ZZRCUFIQWHP6` |
| Bill Payment | `blp` | `blp01...` |
| Vendor Credit | `vcr` | `vcr01CREDITID123` |
| Bill Approval Policy | `{org_id}-{unique}` | `00801ABC-12345` |

### Credential Setup (Per-Tenant)

Each Autonomi tenant needs four BILL credentials stored in NemoClaw:

| Variable | Description |
|----------|-------------|
| `username` | Email address for BILL developer account |
| `password` | Password for BILL developer account |
| `developer_key` | Developer key generated in BILL Settings > Sync & Integrations |
| `organization_id` | Org ID (begins with `008`), found at bottom of developer key settings page |

For Spend & Expense operations, a separate `api_token` is required (generated in the BILL S&E web app).

## Core Approval Lifecycle

The approval lifecycle has four stages:

### Stage 1: Bill Creation

Bills are created via `POST /v3/bills`. Required fields:

| Field | Description |
|-------|-------------|
| `vendorId` | BILL vendor ID (begins with `009`) |
| `dueDate` | Due date in `yyyy-MM-dd` format |
| `billLineItems` | Array with `amount` and optional `description` per line item |
| `invoiceNumber` | (in `invoice` object) Bill invoice number |
| `invoiceDate` | (in `invoice` object) Invoice sent date in `yyyy-MM-dd` |

Line item amounts can be set directly via `amount`, or calculated from `quantity * price`.

**Bulk creation**: `POST /v3/bills/bulk` creates multiple bills in one request. This is all-or-nothing — if any bill fails, the entire request fails and none are created. Error code `BDC_1246` indicates a rollback due to other failures in the transaction.

A newly created bill has:
- `paymentStatus`: `UNPAID`
- `approvalStatus`: `UNASSIGNED`

**To include approval info in bill responses**, set `billApprovals=true` as a query parameter when creating or retrieving bills with the v3 API.

### Stage 2: Policy Match and Approver Assignment

When a bill is created and an active approval policy matches (based on rules), BILL automatically assigns approvers to the bill.

**Creating approval policies** via `POST /v3/bill-approvals`:

```json
{
  "policyName": "Bills 1000 to 2000",
  "rules": [
    { "key": "BILL_AMOUNT", "op": "gte", "values": ["1000"] },
    { "key": "BILL_AMOUNT", "op": "lt", "values": ["2000"] }
  ],
  "approvers": ["{user_id01}", "{user_id02}"]
}
```

Key details:
- `rules` is an array of objects with `key`, `op`, and `values`. Rules are applied in the specified order.
- Supported rule key: `BILL_AMOUNT`. Supported operators: `gte` (greater than or equal), `lt` (less than).
- `approvers` is a simple string array of user IDs (beginning with `006`). In the response, BILL returns an `approvers` object with `users` (array of `{userId, fullName}`) and `groups` (empty array unless groups are configured via the web app).
- Approval groups cannot be created via the API yet — only through the BILL web app (Settings > Approval policies > Approval groups).
- The response includes a policy `id` in `{organization_id}-{unique_id}` format, and `status: "ACTIVE"`.

**When a bill matches a policy**, the bill response includes:
- `approvalStatus`: changes from `UNASSIGNED` to `ASSIGNED`
- `approvers` array: each entry has `userId`, `status` ("WAITING"), `approverOrder` (0-indexed), and `statusChangedTime`

**The bill cannot be paid until all required approvers have approved it.**

### Stage 3: Approve or Deny

Approvers act on bills via `POST /v3/bill-approvals/actions`:

```json
{
  "billId": "{bill_id}",
  "action": "APPROVE"
}
```

- `action` can be `APPROVE` or `DENY`
- A successful approval returns HTTP 200
- The signed-in user must have the correct permissions (Administrator, Accountant, or Approver roles)
- Only users assigned as approvers for that bill can approve/deny it

**Getting pending approvals**: `GET /v3/bill-approvals/pending-user-approvals` returns bills pending approval by the currently signed-in user:

```json
{
  "bills": [
    {
      "billId": "{bill_id}",
      "vendorId": "{vendor_id}",
      "amount": 1500.00,
      "dueDate": "2026-12-31"
    }
  ]
}
```

### Stage 4: Payment (Post-Approval)

Once fully approved, a bill can be paid via `POST /v3/payments`. This is an MFA-trusted operation.

Required fields:

| Field | Description |
|-------|-------------|
| `billId` | Bill ID (begins with `00n`). Omit if `createBill: true` |
| `processDate` | Payment date in `yyyy-MM-dd`. Required for WALLET type |
| `fundingAccount` | Object with `type` (BANK_ACCOUNT, CARD_ACCOUNT, or WALLET) and `id` |
| `amount` | Payment amount |
| `processingOptions` | Object with `createBill` (boolean) and optional `requestPayFaster` |

Get bank accounts with `GET /v3/funding-accounts/banks`.

Payment response includes: `id` (begins with `stp`), `status` ("SCHEDULED"), `disbursementType` ("ACH" or "CHECK"), `singleStatus`, `transactionNumber`, `confirmationNumber`.

**Bulk payments**: `POST /v3/payments/bulk`. All-or-nothing like bulk bills. Requires `fundingAccount` at the top level and `payments` array with `billId` and `amount` per entry. If vendor has `combinePayments: true`, BILL combines up to 35 bills into one payment. Negative payment amounts are not allowed — apply vendor credits to the bill first, then exclude $0-balance bills from the bulk request.

**BILL Pay Faster**: Set `requestPayFaster: true` in `processingOptions` for expedited payments. Options include Pay Faster ACH (same-day or next-business-day), Pay Faster Check (UPS 1-day, 2-day, 3-day), and Instant Payment (RTP, only for Verified National Vendors).

## Vendor Credits

Vendor credits adjust the amount owed to a vendor. Managed via `/v3/vendor-credits`.

### Create a vendor credit

`POST /v3/vendor-credits`:

```json
{
  "vendorId": "{vendor_id}",
  "referenceNumber": "202602-vendorcredit",
  "creditDate": "2026-12-28",
  "vendorCreditLineItems": [
    { "description": "Item return", "amount": 14.99 },
    { "description": "Pricing correction", "amount": 50.00 }
  ],
  "description": "Vendor Credit 20261228"
}
```

Response includes `id` (begins with `vcr`), `amount`, `appliedAmount` (initially 0), `status` ("NOT_APPLIED").

### Apply vendor credit to a bill

`PATCH /v3/bills/{billId}`:

```json
{
  "vendorCredits": [
    { "id": "{vendor_credit_id}", "amount": 10.00 }
  ]
}
```

After applying: `creditAmount` is set on the bill, `dueAmount` is recalculated (`totalAmount - creditAmount - scheduledAmount - clearedPayment`).

### Apply vendor credit to a payment

Include `vendorCredits` in the `POST /v3/payments` request. The `amount` field in the payment should be the bill amount minus the credit amount.

**Critical**: A vendor credit cannot be unapplied from a payment. It can only be unapplied from a bill (before the bill is paid) by issuing a `PUT /v3/bills/{billId}` with the complete bill details and the `vendorCredits` removed.

### Vendor credit status lifecycle

`NOT_APPLIED` → `PARTIALLY_APPLIED` → `FULLY_APPLIED`

The `usage` array in the vendor credit response lists all bills and payments the credit has been applied to.

## Webhooks

BILL webhooks deliver real-time notifications for events. Subscribe via the webhooks API at the webhooks base URL:

```
Sandbox:    https://gateway.stage.bill.com/connect-events
Production: https://gateway.prod.bill.com/connect-events
```

### Header requirements by event type

| Event Scope | Required Headers |
|-------------|-----------------|
| Org-level AP & AR events | `devKey` + `sessionId` |
| Partner-level AP & AR events | `appKey` + `sessionId` |
| Spend & Expense events | `apiToken` |

### Available webhook events

| Event | Category |
|-------|----------|
| `vendor.created`, `vendor.updated`, `vendor.archived`, `vendor.restored` | Vendor |
| `autopay.failed` | Vendor auto-pay |
| `bill.created`, `bill.updated`, `bill.archived`, `bill.restored` | AP Bill |
| `payment.updated`, `payment.failed` | AP Payment |
| `bank-account.created`, `bank-account.updated` | Bank Account |
| `card-account.created`, `card-account.updated` | Card Account |
| `invoice.created`, `invoice.updated`, `invoice.archived`, `invoice.restored` | AR Invoice |
| `risk-verification.updated` | Risk Verification |
| `spend.transaction.updated` | S&E Transaction |
| `spend.reimbursement.created`, `spend.reimbursement.updated`, `spend.reimbursement.deleted` | S&E Reimbursement |
| `spend.three-ds-challenge.created` | S&E 3D Secure |

### Webhook rules

- Webhook notifications should **not** be the only source of truth. For critical workflows, validate with GET API operations.
- Subscriptions require an `X-Idempotent-Key` header in UUID4 format.
- A `notificationUrl` must be provided where BILL sends event payloads.
- For idempotency, each subscription creation request should use a unique idempotent key.

### Events relevant to approval workflows

For the approval chain, the most relevant events are:
- `bill.created` — Trigger policy evaluation and initial approver assignment
- `bill.updated` — Detect approval status changes (ASSIGNED, APPROVED, DENIED)
- `payment.updated` — Track payment status after approval
- `payment.failed` — Alert Settlement Agent for payment failures

## Vendor Management (Approval-Adjacent)

Vendors are organizations you pay for goods and services. Managed via `/v3/vendors`.

### Create a vendor

`POST /v3/vendors` with name, address, and optionally bank account information. If bank account info is provided, BILL enables electronic payments. Otherwise, BILL sends a check.

### BILL Network

The BILL Network connects vendor and customer organizations for electronic payments. When a vendor is in the network and you send a connection request, BILL automatically connects you. Network vendors can accept ACH, virtual card, or check based on their configured payment method.

Verified National Vendors (large billers like utilities and telecoms) are part of the BILL verified national vendor network and can accept Instant Payment (RTP).

## Agent Integration Patterns

### Linear Approval Chain

The Autonomi approval chain is: **Procurement → Quality → AP** (with Settlement for exceptions).

Each agent maps to a BILL user in the tenant's organization. The approval policy `approvers` array sets the order.

#### Procurement Agent
- Receives `bill.created` webhook or polls for new bills
- Validates PO match (vendor, amounts, line items against ERP data)
- If match: approves via `POST /v3/bill-approvals/actions` with `"action": "APPROVE"`
- If mismatch: denies with `"action": "DENY"` and logs the discrepancy

#### Quality Agent
- Polls `GET /v3/bill-approvals/pending-user-approvals` for bills awaiting its approval
- Cross-references COA data, lot numbers, spec compliance
- Approves or denies based on quality criteria

#### AP/Finance Agent
- Final approver in the chain
- Verifies budget availability, GL coding, payment terms
- On approval, bill becomes eligible for payment
- Can apply vendor credits via `PATCH /v3/bills/{billId}` before payment

#### Settlement Agent (Exception Handler)
- Activated on `payment.failed` webhooks or denial escalations
- Investigates failures (bank account inactive, overpayment, invalid process date)
- Can create vendor credits, void payments, or re-route bills

### Polling vs Webhooks

**Webhooks** (preferred): Subscribe to `bill.created`, `bill.updated`, `payment.updated`, `payment.failed`. Route events to the appropriate agent based on the event type and the bill's current `approvalStatus`.

**Polling** (fallback): Use `GET /v3/bill-approvals/pending-user-approvals` on a schedule (e.g., every 5 minutes). Compare with previous poll results to detect new assignments.

**Hybrid** (recommended): Use webhooks as the primary mechanism, with periodic polling to catch any missed events. The `ApprovalStatusSync` script implements this pattern with persistent state tracking.

### Model Armor Integration

All data ingested from BILL.com (vendor names, bill descriptions, invoice numbers) passes through Model Armor prompt-injection screening before being processed by any agent. This prevents adversarial content in vendor-submitted invoices from manipulating agent behavior.

Screening pipeline:
1. BILL API response received
2. Text fields extracted (description, vendor name, line item descriptions)
3. Model Armor `screenPrompt()` called on each field
4. If injection detected: field quarantined, agent alerted, bill flagged for human review
5. If clean: data passed to agent for normal processing

### LynZ Voice Agent Integration

For voice-driven AP workflows, the LynZ MCP server exposes these tools:

| Tool | Description |
|------|-------------|
| `bill_check_pending` | Get count and summary of bills pending approval |
| `bill_approve` | Approve a bill by ID with voice confirmation |
| `bill_deny` | Deny a bill by ID with reason dictation |
| `bill_status` | Get current approval status of a bill |
| `bill_escalate` | Escalate a bill to the Settlement Agent |

## Common Scenarios

### Scenario 1: Standard Three-Step Approval
1. Bill created → policy matches → approvers assigned (Procurement user, Quality user, AP user)
2. Procurement Agent polls pending approvals, finds bill, validates PO → approves
3. Quality Agent polls, finds bill in its queue, checks COA → approves
4. AP Agent polls, finds bill, verifies budget → approves
5. Bill is now fully approved (`approvalStatus` changes accordingly)
6. Payment created via `POST /v3/payments`

### Scenario 2: Bill with Vendor Credit
1. Bill created for $500
2. Existing vendor credit of $100 (from prior return)
3. AP Agent applies credit: `PATCH /v3/bills/{billId}` with `vendorCredits: [{id, amount: 100}]`
4. Bill `dueAmount` becomes $400
5. Payment created for $400

### Scenario 3: Bulk Bill Ingestion
1. ERP system exports 50 invoices as a batch
2. `POST /v3/bills/bulk` creates all 50 bills (all-or-nothing)
3. If any bill fails validation (e.g., invalid `vendorId`), entire batch fails with `BDC_1205` / `BDC_1246`
4. Fix failed records, retry entire batch
5. On success, each bill gets its own `id` and enters the approval pipeline individually

### Scenario 4: Payment Failure Escalation
1. Bill fully approved, payment submitted
2. `payment.failed` webhook fires
3. Settlement Agent receives alert, checks error (e.g., "Bank account is inactive", "Cannot overpay a bill")
4. Agent resolves: updates vendor bank info, adjusts payment amount, or voids and recreates

### Scenario 5: International Vendor Payment
1. International vendor created (outside US)
2. Bill created — response includes `fundingAmount` (USD), `exchangeRate`, and `amount` (local currency)
3. Exchange rate may change between bill creation and payment time
4. Payment amount is in local currency; funding is withdrawn in USD

## Error Handling

### Common BILL API Error Codes

| Code | Description |
|------|-------------|
| `BDC_1205` | No data found for object with given ID |
| `BDC_1246` | Rollback due to other failures in bulk transaction |
| `BDC_1159` | Cannot overpay a bill |

### HTTP-Level Errors

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Session expired | Re-authenticate with `POST /v3/login` |
| 429 | Rate limited | Exponential backoff, retry after delay |
| 500/503 | Server error | Retry with backoff (max 3 retries) |

### Retry Strategy

```python
RETRY_CODES = {401, 429, 500, 503}
MAX_RETRIES = 3
BACKOFF_BASE = 2  # seconds, exponential

# On 401: refresh session, then retry
# On 429: respect Retry-After header if present, else backoff
# On 500/503: exponential backoff
```

## Reference Files

- `references/bill_api_v3.md` — Complete v3 endpoint reference with request/response schemas
- `references/security.md` — NemoClaw credential isolation, Model Armor rules, permission matrix
- `scripts/bill_session.py` — Session management with auto-refresh and retry logic
- `scripts/approval_chain.py` — Approval workflow operations (get pending, approve, deny, escalate)
- `scripts/approval_status_sync.py` — Polling-based status sync with persistent state
- `scripts/webhook_handler.py` — Webhook receiver with signature verification and agent dispatch

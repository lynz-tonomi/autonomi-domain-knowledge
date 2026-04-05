---
name: qbo-autonomi
description: >
  QuickBooks Online (QBO) integration for Autonomi — connects AI agents to tenant
  QBO accounts via Intuit REST API (v3). Handles AP (bills, bill payments, vendor
  credits), AR (invoices, payments, credit memos, deposits), financial reporting
  (P&L, balance sheet, cash flow, aging, trial balance), inventory & purchasing
  (items, POs, purchases, estimates), chart of accounts, journal entries, tax codes,
  attachments, and webhook/CDC sync. Built for NemoClaw sandboxes with per-tenant
  OAuth 2.0 isolation. ALWAYS trigger on: QuickBooks, QBO, Intuit, qbo, invoicing,
  bill payment, accounts payable, accounts receivable, AP/AR, vendor management,
  customer management, chart of accounts, journal entry, P&L, balance sheet, aging
  report, purchase order, inventory tracking, sales receipt, credit memo, vendor
  credit, QBO sync, QBO webhook, realm ID, SyncToken, or any accounting/bookkeeping
  through QuickBooks — even if not explicitly named.
---

# QuickBooks Online Integration for Autonomi

## Why This Matters

Food and beverage manufacturers run on tight margins where every invoice, bill, and
inventory transaction needs to flow cleanly through the books. QuickBooks Online is
the accounting backbone for many Autonomi tenants — when the Procurement Agent creates
a purchase order, when the AP Agent processes a vendor bill, when the Finance Agent
pulls a P&L report, they all need reliable, auditable access to QBO. This skill
ensures every agent interaction with QBO follows proper authentication, respects rate
limits, handles the SyncToken concurrency model correctly, and screens all external
data through Model Armor before processing.

## Platform Overview

**QuickBooks Online REST API v3**

| Environment | Base URL |
|------------|----------|
| Production | `https://quickbooks.api.intuit.com` |
| Sandbox | `https://sandbox-quickbooks.api.intuit.com` |

All endpoints follow the pattern:
```
{base_url}/v3/company/{realmId}/{entity}?minorversion=75
```

The `realmId` (Company ID) uniquely identifies each tenant's QuickBooks company and
is required in every API call. The `minorversion` parameter should always be set to
**75 or higher** — minor versions 1–74 were phased out August 2025.

**Data format:** JSON (recommended) or XML.
**Authentication:** OAuth 2.0 exclusively — no API keys or basic auth.

---

## Setup & Authentication

QuickBooks uses OAuth 2.0 with a per-tenant authorization flow. Each Autonomi tenant
connects their own QBO company, and the resulting credentials are stored in the
NemoClaw sandbox with strict isolation.

### OAuth 2.0 Flow

Read `references/auth.md` for the complete OAuth 2.0 implementation guide including
endpoints, scopes, token lifecycle, and the per-tenant credential storage pattern.

**Quick reference:**

| Component | Value |
|-----------|-------|
| Authorization endpoint | `https://appcenter.intuit.com/connect/oauth2` |
| Token endpoint | `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer` |
| Primary scope | `com.intuit.quickbooks.accounting` |
| Payment scope | `com.intuit.quickbooks.payment` |
| Access token lifetime | ~1 hour |
| Refresh token lifetime | ~100 days |

**Critical:** The `realmId` is returned only once during the initial authorization
redirect. Capture and store it immediately — there is no API endpoint to retrieve it
later.

### Credential Storage Pattern

```
/sandbox/credentials/tenant_{TENANT_ID}/qbo/
├── oauth_config.json      # client_id, client_secret, redirect_uri
├── token.json             # access_token, refresh_token, realm_id, expiry
└── webhook_verifier.txt   # HMAC-SHA256 verifier token for webhook validation
```

Credentials are encrypted at rest (AES-256-GCM) and scoped so each agent sandbox
can only read its own tenant's credentials. Token refresh is handled automatically
by the `scripts/qbo_auth.py` helper — every API call should go through this helper
to ensure valid tokens.

### Network Policy

Outbound connections restricted to:
- `quickbooks.api.intuit.com`
- `sandbox-quickbooks.api.intuit.com`
- `oauth.platform.intuit.com`
- `appcenter.intuit.com`

---

## Core Operations

### Understanding the SyncToken Model

QBO uses optimistic concurrency via `SyncToken`. Every entity has a SyncToken that
increments on each update. To update an entity, you must include its current
SyncToken — if someone else modified it since your last read, the API returns
error 5010 (Stale Object). The correct response is to re-read the entity, get the
fresh SyncToken, and retry.

This matters because Autonomi agents may be working concurrently. The
`scripts/qbo_request.py` helper handles SyncToken conflicts automatically with
read-retry logic (up to 3 attempts).

### Query Language

QBO provides a SQL-like query language for searching entities:

```
SELECT * FROM Invoice WHERE TxnDate > '2025-01-01' AND Balance > '0'
SELECT * FROM Vendor WHERE DisplayName LIKE '%Acme%'
SELECT * FROM Bill WHERE VendorRef = '42' ORDER BY DueDate
```

**Limitations to keep in mind:**
- Always `SELECT *` — column projections aren't supported
- No `OR` operator, no `JOIN`, no `GROUP BY`
- Only `%` wildcard in `LIKE` clauses
- Escape apostrophes with backslash: `O\'Brien`
- Query string must be URL-encoded

Queries execute via GET:
```
GET /v3/company/{realmId}/query?query={url_encoded_query}&minorversion=75
```

Use `startposition` and `maxresults` for pagination (1-indexed, max 1000 per page).

### Accounts Payable

Read `references/qbo_api_entities.md` (AP section) for full request/response
examples.

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create bill | POST | `/v3/company/{realmId}/bill` |
| Read bill | GET | `/v3/company/{realmId}/bill/{billId}` |
| Update bill | POST | `/v3/company/{realmId}/bill` (include Id + SyncToken) |
| Delete bill | POST | `/v3/company/{realmId}/bill?operation=delete` |
| Query bills | GET | `/v3/company/{realmId}/query?query=SELECT * FROM Bill` |
| Create bill payment | POST | `/v3/company/{realmId}/billpayment` |
| Create vendor credit | POST | `/v3/company/{realmId}/vendorcredit` |
| Manage vendors | POST/GET | `/v3/company/{realmId}/vendor` |

**Bill → BillPayment flow:** Create the Bill first, then when ready to pay, create
a BillPayment that references the Bill via `Line.LinkedTxn`. A BillPayment can
reference multiple bills in a single payment.

### Accounts Receivable

Read `references/qbo_api_entities.md` (AR section) for full request/response
examples.

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create invoice | POST | `/v3/company/{realmId}/invoice` |
| Read invoice | GET | `/v3/company/{realmId}/invoice/{invoiceId}` |
| Send invoice (email) | POST | `/v3/company/{realmId}/invoice/{id}/send` |
| Void invoice | POST | `/v3/company/{realmId}/invoice` (set as voided) |
| Record payment | POST | `/v3/company/{realmId}/payment` |
| Create credit memo | POST | `/v3/company/{realmId}/creditmemo` |
| Create deposit | POST | `/v3/company/{realmId}/deposit` |
| Manage customers | POST/GET | `/v3/company/{realmId}/customer` |

**Invoice → Payment flow:** Create the Invoice, then when payment is received,
create a Payment that references the Invoice. Overpayments automatically create
unapplied credits.

### Financial Reporting

Reports are real-time calculations — not stored snapshots — so they reflect current
data but can be slow for large datasets.

```
GET /v3/company/{realmId}/reports/{ReportName}?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&accounting_method=Accrual
```

| Report | ReportName parameter |
|--------|---------------------|
| Profit & Loss | `ProfitAndLoss` |
| P&L Detail | `ProfitAndLossDetail` |
| Balance Sheet | `BalanceSheet` |
| Cash Flow Statement | `CashFlow` |
| Trial Balance | `TrialBalance` |
| General Ledger | `GeneralLedger` |
| AR Aging Summary | `AgedReceivables` |
| AR Aging Detail | `AgedReceivableDetail` |
| AP Aging Summary | `AgedPayables` |
| AP Aging Detail | `AgedPayableDetail` |
| Transaction List | `TransactionList` |

**Three things to always remember about reports:**

1. **Query Preferences first** to determine the tenant's accounting method (Accrual
   vs Cash) and use that value in every report request's `accounting_method` parameter.
2. **Column limit:** Requesting more than 25 columns risks 504 Gateway Timeout errors.
3. **Cell cap:** Report responses are hard-capped at **400,000 cells**. If a report
   hits this limit, the response is silently truncated — you won't get an error, just
   missing data. For large reports, narrow the date range or use additional filters
   to stay under the cap.

### Inventory & Purchasing

Read `references/qbo_api_entities.md` (Inventory section) for full details.

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Manage items | POST/GET | `/v3/company/{realmId}/item` |
| Create purchase order | POST | `/v3/company/{realmId}/purchaseorder` |
| Record purchase | POST | `/v3/company/{realmId}/purchase` |
| Create estimate | POST | `/v3/company/{realmId}/estimate` |
| Create sales receipt | POST | `/v3/company/{realmId}/salesreceipt` |

**Item types:** Inventory (tracked quantity on hand), NonInventory (purchased but
not tracked), Service (labor/services sold). Purchase orders are non-posting
transactions — they don't hit the books until converted to a bill or item receipt.
Purchase orders require QBO Plus or Advanced subscription.

### Chart of Accounts & Journal Entries

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Manage accounts | POST/GET | `/v3/company/{realmId}/account` |
| Create journal entry | POST | `/v3/company/{realmId}/journalentry` |
| Query journal entries | GET | `/v3/company/{realmId}/query?query=SELECT * FROM JournalEntry` |

Journal entries require at least one debit and one credit line. Lines referencing
AR accounts must include a CustomerRef; lines referencing AP accounts must include
a VendorRef.

### Attachments

Upload supporting documents (COAs, receipts, invoices) to QBO entities:

```
POST /v3/company/{realmId}/upload
Content-Type: multipart/form-data
```

- Max 20 MB per transaction
- File name max 1000 characters
- Link attachments to entities using `AttachableRef`

### Tax Handling

US companies using QBO's Automated Sales Tax (AST) engine don't need manual tax
calculation — create a proxy TaxCode via the API, and QBO swaps it for the correct
AST-determined rate based on source/destination addresses. For non-US locales, read
`references/qbo_api_entities.md` (Tax section).

---

## Agent Integration Patterns

Each Autonomi agent accesses QBO through scoped permissions. The principle here is
least privilege — an agent that only needs to read invoices shouldn't have write
access to journal entries.

### Agent → QBO Operation Mapping

| Agent | QBO Operations | Access Level |
|-------|---------------|-------------|
| Procurement Agent | Purchase orders, vendor management, item queries | Read/Write PO, Vendor, Item |
| AP Agent | Bills, bill payments, vendor credits | Read/Write Bill, BillPayment, VendorCredit |
| AR Agent | Invoices, payments, credit memos, deposits | Read/Write Invoice, Payment, CreditMemo |
| Inventory Agent | Items, purchase orders, stock queries | Read/Write Item, PurchaseOrder |
| Finance Agent | All reports, journal entries, chart of accounts | Read all entities, Write JournalEntry |
| Quality Agent | Vendor queries, attachment uploads (COAs) | Read Vendor, Write Attachable |
| Settlement Agent | Bill payments, deposits, payment reconciliation | Read/Write BillPayment, Deposit, Payment |
| LynZ Voice Agent | Read-only across all entities for voice summaries | Read-only all entities |

### LynZ Voice Agent Pattern

LynZ has broad read access for voice-based financial summaries but cannot modify
any QBO data. All data is screened through Model Armor before text-to-speech output.
Summarize financial data into voice-friendly formats — don't read raw JSON values
aloud. Example: "You have 12 unpaid invoices totaling forty-seven thousand dollars,
with three past due" rather than listing each invoice.

---

## Enterprise Patterns

### Rate Limits

| Limit | Value |
|-------|-------|
| Standard requests | 500/minute per realmId |
| Concurrent requests | 10 max per app+realmId |
| Resource-intensive endpoints | 200/minute |
| Batch operations | 40/minute |
| Sandbox email sends | 40/day per realmId |

When you hit a 429 (Too Many Requests), use exponential backoff starting at 2
seconds. The `scripts/qbo_request.py` helper handles this automatically.

### Idempotency

Include a unique `requestid` parameter on every write operation:

```
POST /v3/company/{realmId}/invoice?requestid={uuid}&minorversion=75
```

If a request fails and you retry with the same `requestid`, QBO returns the
original response rather than creating a duplicate. Generate UUIDs for each
request and log them for replay capability.

### Batch Operations

Bundle up to 30 operations in a single request:

```
POST /v3/company/{realmId}/batch
```

Each item in the batch has a `bId` for correlation. Operations execute serially
but without visibility into previous results within the same batch. Rate-limited
to 40 batch requests per minute.

### Change Data Capture (CDC)

Poll for changes since a timestamp across multiple entity types:

```
GET /v3/company/{realmId}/cdc?entities=Invoice,Bill,Payment&changedSince=2025-03-20T00:00:00Z
```

- Look-back window: 30 days maximum
- Returns up to 1,000 objects per response (full payloads). If a tenant has more
  than 1,000 changes, poll each entity type separately to avoid truncation
- Always use an overlap window (e.g., `changedSince = now - 26 hours` for a daily
  sync) to prevent edge-case misses at the time boundary
- Ideal for daily sync jobs as a safety net behind webhooks

### Webhooks

QBO supports real-time notifications for Create, Update, Delete, Merge, and Void
events across most entity types.

**Two non-negotiable webhook rules:**

1. **HMAC-SHA256 signature validation is mandatory.** Every incoming webhook payload
   includes an `intuit-signature` HTTP header. Compute HMAC-SHA256 of the raw request
   body using the Verifier Token (from your app's webhook config) as the key,
   base64-encode the result, and compare. Reject any payload where the signature
   doesn't match — this prevents spoofed events from triggering agent actions. See
   `references/webhooks_and_sync.md` for the Python validation code.

2. **Respond with HTTP 200 within 3 seconds.** Intuit considers any response slower
   than 3 seconds a delivery failure and retries with exponential backoff. This means
   your webhook handler must return 200 immediately and queue the payload for
   asynchronous processing — never do API lookups, database writes, or agent routing
   in the synchronous request path.

**Recommended pattern:** Webhooks for real-time + daily CDC poll as fallback. This
ensures no events are missed even if a webhook delivery fails.

Read `references/webhooks_and_sync.md` for the full webhook setup, payload format,
HMAC validation code, and the recommended sync architecture.

### Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 5010 | Stale Object (SyncToken conflict) | Re-read entity, get fresh SyncToken, retry |
| 2020 | Required parameter missing | Validate request fields before sending |
| 120 | Authorization failure | Refresh OAuth token, retry once |
| 429 / 003001 | Rate limit exceeded | Exponential backoff (2s, 4s, 8s) |
| 6000 | Validation error | Check field values and types |
| 6140 | Duplicate entity | Query for existing entity, use that instead |
| 6190 | Subscription limitation | Check tenant's QBO subscription tier |
| 500/503 | Server error | Retry with backoff (max 3 attempts) |

Error responses follow this structure:
```json
{
  "Fault": {
    "Error": [{"Message": "...", "Detail": "...", "code": "5010"}],
    "type": "ValidationFault"
  }
}
```

### Model Armor Integration

All data received from QBO APIs is screened through Model Armor before agent
processing. This is especially important for:
- Vendor-submitted bill descriptions and line item memos (potential prompt injection)
- Customer names and addresses from invoices
- Attachment content (uploaded documents)
- Free-text fields in any entity

Model Armor screening is enabled by default in all `scripts/qbo_request.py` calls.

---

## Common Scenarios

### Scenario 1: Procurement Agent Creates a Purchase Order

1. Query existing vendors: `SELECT * FROM Vendor WHERE DisplayName LIKE '%{name}%'`
2. If vendor doesn't exist, create one via POST `/vendor`
3. Query items to get current Item IDs and pricing
4. Create PurchaseOrder with line items referencing vendor and items
5. Webhook fires `PurchaseOrder.created` → AP Agent is notified

### Scenario 2: AP Agent Processes a Vendor Bill

1. Receive notification (webhook or polling) of new bill to process
2. Create Bill via POST `/bill` with VendorRef, line items, and due date
3. If applicable, apply VendorCredit against the bill
4. When approved for payment, create BillPayment linking to the Bill
5. Upload supporting documents (COA, receipt) as attachments

### Scenario 3: Finance Agent Pulls Month-End Reports

1. Query Preferences to get accounting method: `GET /v3/company/{realmId}/preferences`
2. Pull P&L: `GET /reports/ProfitAndLoss?start_date=2025-03-01&end_date=2025-03-31&accounting_method=Accrual`
3. Pull Balance Sheet: `GET /reports/BalanceSheet?...`
4. Pull AP/AR Aging: `GET /reports/AgedPayables?...` and `GET /reports/AgedReceivables?...`
5. Compile into tenant report via document generation scripts

### Scenario 4: Inventory Agent Monitors Stock Levels

1. Query all inventory items: `SELECT * FROM Item WHERE Type = 'Inventory'`
2. Check QtyOnHand against reorder points
3. If below threshold, trigger Procurement Agent to create PurchaseOrder
4. Use CDC to track inventory changes since last sync:
   `GET /cdc?entities=Item&changedSince={last_sync_timestamp}`

### Scenario 5: Daily Sync (CDC + Webhook Fallback)

1. Run daily CDC poll: `GET /cdc?entities=Invoice,Bill,Payment,Item&changedSince={24h_ago}`
2. Compare with webhook-received events to identify any missed notifications
3. Process any gaps
4. Update `last_sync_timestamp` for next run

---

## Reference Files

| File | Contents | When to read |
|------|----------|-------------|
| `references/auth.md` | OAuth 2.0 flow, token management, credential storage | Setting up a new tenant connection |
| `references/qbo_api_entities.md` | Full entity reference with request/response examples | Building or debugging any API call |
| `references/webhooks_and_sync.md` | Webhook setup, HMAC validation, CDC patterns, sync architecture | Implementing event-driven workflows |
| `references/security.md` | NemoClaw isolation, Model Armor rules, permission matrix | Security review or new agent onboarding |

## Bundled Scripts

| Script | Purpose |
|--------|---------|
| `scripts/qbo_auth.py` | OAuth token management with auto-refresh |
| `scripts/qbo_request.py` | HTTP helper with retry, rate limiting, SyncToken handling, Model Armor |
| `scripts/setup_tenant_workspace.py` | Initialize tenant QBO workspace and folder structure |
| `scripts/sync_qbo_data.py` | CDC-based daily sync with webhook reconciliation |
| `scripts/qbo_webhook_processor.py` | Receive and validate QBO webhook events, route to agents |
| `scripts/generate_financial_report.py` | Pull and format financial reports for tenant dashboards |

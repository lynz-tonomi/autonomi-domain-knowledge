# QBO API Integration Patterns for Autonomi Agents

## Overview

QuickBooks Online exposes a REST API (v3) for programmatic access to accounting data. Autonomi AI agents use this API to create transactions, sync inventory, run reports, and automate month-end close. This document covers authentication, key endpoints, query patterns, webhook integration, error handling, and common automation workflows.

---

## 1. OAuth 2.0 Authentication

### Authorization Code Grant Flow

QBO uses OAuth 2.0 with authorization code grant. This is a three-legged flow requiring user consent.

**Step 1 — Authorization Request**
```
GET https://appcenter.intuit.com/connect/oauth2
  ?client_id={CLIENT_ID}
  &redirect_uri={REDIRECT_URI}
  &response_type=code
  &scope=com.intuit.quickbooks.accounting
  &state={CSRF_TOKEN}
```

**Step 2 — Token Exchange**
```
POST https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer
Content-Type: application/x-www-form-urlencoded
Authorization: Basic {base64(CLIENT_ID:CLIENT_SECRET)}

grant_type=authorization_code
&code={AUTH_CODE}
&redirect_uri={REDIRECT_URI}
```

**Step 3 — Response**
```json
{
  "access_token": "eyJhbG...",
  "refresh_token": "Q011...",
  "token_type": "bearer",
  "expires_in": 3600,
  "x_refresh_token_expires_in": 8726400
}
```

### Token Lifecycle Management

| Token | Lifetime | Refresh Strategy |
|-------|----------|-----------------|
| Access token | 60 minutes (3600s) | Refresh proactively at 50 minutes |
| Refresh token | 100 days | Refresh on every use; store new refresh token |

**Critical rules:**
- Store refresh tokens encrypted at rest (AES-256 or equivalent)
- Never log access tokens or refresh tokens
- Implement token refresh retry with exponential backoff (max 3 attempts)
- If refresh token expires (100 days unused), user must re-authorize — alert ops team immediately
- Each realm (company) has its own token pair — multi-entity requires separate token management

### Scopes
| Scope | Access |
|-------|--------|
| `com.intuit.quickbooks.accounting` | Full read/write to accounting data |
| `com.intuit.quickbooks.payment` | Payment processing (separate from accounting) |
| `openid` | User identity information |
| `profile` | User profile data |
| `email` | User email address |

---

## 2. Key API Endpoints

Base URL: `https://quickbooks.api.intuit.com/v3/company/{realmId}`

### Transaction Entities

**Invoice (AR)**
```
POST   /invoice          — Create invoice
GET    /invoice/{id}     — Read invoice
POST   /invoice          — Update invoice (include Id + SyncToken)
POST   /invoice/{id}?operation=delete — Delete (void preferred)
POST   /invoice/{id}/send — Email invoice to customer
GET    /invoice/{id}/pdf  — Get PDF rendition
```

**Bill (AP)**
```
POST   /bill             — Create bill (vendor invoice)
GET    /bill/{id}        — Read bill
POST   /bill             — Update bill
POST   /bill/{id}?operation=delete — Delete
```

**Bill Payment**
```
POST   /billpayment      — Record payment against one or more bills
GET    /billpayment/{id} — Read payment
```

**Payment (AR)**
```
POST   /payment          — Record customer payment against invoices
GET    /payment/{id}     — Read payment
```

**Journal Entry**
```
POST   /journalentry     — Create journal entry
GET    /journalentry/{id} — Read
POST   /journalentry     — Update
```

**Purchase Order**
```
POST   /purchaseorder    — Create PO
GET    /purchaseorder/{id} — Read
POST   /purchaseorder    — Update (change status, add lines)
```

### Reference Entities

**Item (Products/Services)**
```
POST   /item             — Create inventory item, non-inventory item, or service
GET    /item/{id}        — Read item
POST   /item             — Update (adjust QtyOnHand via InventoryAdjustment, not direct update)
```

**Vendor**
```
POST   /vendor           — Create vendor
GET    /vendor/{id}      — Read
POST   /vendor           — Update
```

**Customer**
```
POST   /customer         — Create customer
GET    /customer/{id}    — Read
POST   /customer         — Update
```

**Account**
```
POST   /account          — Create GL account
GET    /account/{id}     — Read
POST   /account          — Update
```

### Reporting Endpoints

```
GET /reports/ProfitAndLoss
    ?start_date=2024-01-01&end_date=2024-12-31
    &summarize_column_by=ProductsAndServices

GET /reports/BalanceSheet
    ?date=2024-12-31
    &accounting_method=Accrual

GET /reports/GeneralLedger
    ?start_date=2024-10-01&end_date=2024-10-31
    &account=5000  (filter by account number)

GET /reports/InventoryValuationSummary
    ?date=2024-12-31

GET /reports/AgedReceivables
    ?date=2024-12-31
    &aging_period=30

GET /reports/AgedPayables
    ?date=2024-12-31

GET /reports/VendorBalanceDetail
    ?start_date=2024-01-01&end_date=2024-12-31

GET /reports/CustomerBalanceDetail
    ?start_date=2024-01-01&end_date=2024-12-31
```

Report parameters:
- `accounting_method`: Accrual or Cash
- `summarize_column_by`: Total, Month, Week, ProductsAndServices, Classes, Locations
- `columns`: Comma-separated column list for custom report layout
- `department`: Class filter (QBO uses "department" for class in API)

---

## 3. Query Syntax

QBO supports a SQL-like query language via the `/query` endpoint.

```
GET /query?query=SELECT * FROM Invoice WHERE TotalAmt > '1000' AND TxnDate >= '2024-10-01' ORDERBY TxnDate DESC MAXRESULTS 100
```

### Query Rules
- String values in single quotes: `WHERE DisplayName = 'Acme Corp'`
- Date format: `YYYY-MM-DD`
- Supported operators: `=`, `<`, `>`, `<=`, `>=`, `IN`, `LIKE`
- LIKE uses `%` wildcard: `WHERE DisplayName LIKE 'Acme%'`
- No JOIN support — query one entity at a time
- MAXRESULTS default: 100, max: 1000
- STARTPOSITION for pagination (1-based): `STARTPOSITION 101 MAXRESULTS 100`
- COUNT queries: `SELECT COUNT(*) FROM Invoice WHERE TxnDate >= '2024-01-01'`

### Common Queries for F&B Operations

**Open invoices (AR aging)**
```sql
SELECT * FROM Invoice WHERE Balance > '0' ORDERBY DueDate ASC MAXRESULTS 500
```

**Unpaid bills (AP aging)**
```sql
SELECT * FROM Bill WHERE Balance > '0' ORDERBY DueDate ASC MAXRESULTS 500
```

**Recent inventory items**
```sql
SELECT * FROM Item WHERE Type = 'Inventory' AND Active = true MAXRESULTS 500
```

**Vendor bills for a specific vendor**
```sql
SELECT * FROM Bill WHERE VendorRef = '142' AND TxnDate >= '2024-10-01' MAXRESULTS 100
```

**Journal entries for production costing**
```sql
SELECT * FROM JournalEntry WHERE TxnDate >= '2024-10-01' AND TxnDate <= '2024-10-31' MAXRESULTS 500
```

**Customer by name (fuzzy)**
```sql
SELECT * FROM Customer WHERE DisplayName LIKE '%Whole Foods%'
```

---

## 4. Webhook Integration

### Setting Up Webhooks
QBO webhooks notify your application of data changes in near real-time.

**Create webhook subscription via Intuit Developer Portal:**
- Endpoint URL: `https://api.autonomi.com/webhooks/qbo`
- Events: Create, Update, Delete, Merge, Void
- Entities: Invoice, Bill, Payment, BillPayment, JournalEntry, Item, Vendor, Customer

### Webhook Payload
```json
{
  "eventNotifications": [
    {
      "realmId": "1234567890",
      "dataChangeEvent": {
        "entities": [
          {
            "name": "Invoice",
            "id": "5678",
            "operation": "Create",
            "lastUpdated": "2024-10-15T14:30:00Z"
          }
        ]
      }
    }
  ]
}
```

### Webhook Verification
- Intuit signs payloads with HMAC-SHA256 using your webhook verifier token
- Verify signature in `intuit-signature` header before processing
- Return 200 OK within 10 seconds or Intuit will retry (up to 4 retries over 6 hours)

### Processing Pattern
1. Receive webhook notification (lightweight — contains entity ID only, not full data)
2. Verify HMAC signature
3. Queue entity ID for processing (do not block the webhook response)
4. Return 200 OK immediately
5. Async worker fetches full entity via GET endpoint
6. Process business logic (sync to warehouse, update dashboard, trigger approval)

---

## 5. Rate Limits and Throttling

| Limit Type | Threshold | Scope |
|-----------|-----------|-------|
| API calls | 500/minute | Per realm (company) |
| Concurrent requests | 10 simultaneous | Per realm |
| Batch operations | 30 entities per batch | Per request |
| Query results | 1,000 max per page | Per query |
| Report generation | Varies by complexity | May timeout for large date ranges |

### Throttling Strategy
- Implement token bucket rate limiter (500 tokens/minute, refill rate ~8.3/second)
- Queue non-urgent operations (report generation, bulk sync) during off-peak hours
- Use exponential backoff on 429 responses: 1s, 2s, 4s, 8s, max 30s
- Batch related operations where possible (create multiple line items in one Invoice, not one per call)
- Cache frequently accessed reference data (accounts, items, vendors, customers) — refresh every 15 minutes

---

## 6. Batch Operations

QBO supports batch requests to execute multiple operations in a single HTTP call.

```
POST /batch

{
  "BatchItemRequest": [
    {
      "bId": "1",
      "operation": "create",
      "Invoice": { ... }
    },
    {
      "bId": "2",
      "operation": "create",
      "Invoice": { ... }
    },
    {
      "bId": "3",
      "operation": "query",
      "Query": "SELECT * FROM Customer WHERE DisplayName = 'Acme Corp'"
    }
  ]
}
```

- Max 30 items per batch
- Each item is independent — one failure does not roll back others
- Response includes individual results keyed by `bId`
- Mix operations: create, update, delete, query in same batch
- Useful for: month-end journal entries, bulk invoice creation, batch inventory adjustments

---

## 7. Common Integration Patterns

### PO-to-Bill Matching
1. Agent creates PurchaseOrder in QBO when procurement approves
2. Warehouse receives goods, agent updates PO status via custom field
3. Vendor invoice arrives in Bill.com, syncs to QBO as Bill
4. Agent matches Bill to PO: compare VendorRef, line items, quantities, prices
5. Variance exceeding threshold triggers exception workflow
6. Matched bills auto-approve for payment

### Auto-Invoice on Shipment
1. Warehouse management system (WMS) confirms shipment with BOL
2. Webhook or polling detects shipment event
3. Agent creates Invoice in QBO with: customer, ship date, PO reference, line items, quantities, prices from sales order
4. Agent emails invoice PDF via `/invoice/{id}/send`
5. Agent updates inventory quantities (QBO adjusts on invoice creation if using inventory items)

### Inventory Level Sync from Warehouse
1. WMS provides real-time inventory levels (by lot, location, status)
2. Agent polls WMS API every 15 minutes (or receives webhook)
3. Agent compares WMS quantities to QBO Item.QtyOnHand
4. Discrepancies recorded via InventoryAdjustment or JournalEntry
5. Adjustments categorized: receiving (increase), shipment (decrease), shrink (decrease + expense), transfer (location change)

### Bank Feed Reconciliation Automation
1. QBO ingests bank transactions via bank feed connection
2. Agent queries unmatched bank transactions
3. Matching rules: exact amount match to open invoice/bill, vendor name fuzzy match, date proximity (±3 days)
4. High-confidence matches (>95%) auto-reconciled
5. Low-confidence matches queued for human review
6. Agent categorizes remaining transactions (bank fees, interest, transfers)

### Trade Spend Deduction Processing
1. Retailer/distributor payment arrives short of invoice amount
2. Agent identifies the deduction (payment amount vs. invoice amount)
3. Agent queries promotion database for matching authorized deductions
4. Match found: create Credit Memo against original invoice, code to trade spend account
5. No match found: create Deduction Dispute, flag for accounts receivable team
6. Agent tracks deduction aging and escalates unresolved items >30 days

---

## 8. Error Handling

### Common Error Responses

**Stale Object Error (HTTP 400)**
```json
{
  "Fault": {
    "Error": [{"Message": "Stale Object Error", "code": "5010"}],
    "type": "ValidationFault"
  }
}
```
Cause: SyncToken in request does not match current version. Another process updated the entity.
Fix: Re-fetch entity, get current SyncToken, retry update.

**Duplicate Detection (HTTP 400)**
```json
{
  "Fault": {
    "Error": [{"Message": "Duplicate Document Number", "code": "6140"}],
    "type": "ValidationFault"
  }
}
```
Cause: DocNumber already exists for this entity type.
Fix: Use idempotency strategy — check for existing entity before creating, or append timestamp suffix.

**Business Validation Error (HTTP 400)**
```json
{
  "Fault": {
    "Error": [{"Message": "Object Not Found", "code": "610"}],
    "type": "ValidationFault"
  }
}
```
Cause: Referenced entity (customer, vendor, account, item) does not exist.
Fix: Verify all reference IDs before creating transaction. Create missing references first.

**Authentication Error (HTTP 401)**
Cause: Access token expired or revoked.
Fix: Refresh access token using refresh token. If refresh fails, re-authenticate.

**Rate Limit (HTTP 429)**
Cause: Exceeded 500 requests/minute.
Fix: Exponential backoff. Queue lower-priority requests.

**Internal Server Error (HTTP 500)**
Cause: Intuit platform issue.
Fix: Retry with exponential backoff. If persistent (>5 minutes), check Intuit status page.

### Idempotency Strategy
QBO does not provide native idempotency keys. Implement application-level idempotency:
1. Generate unique request ID per operation (UUID v4)
2. Before creating entity, query for existing entity with matching criteria (DocNumber, VendorRef + TxnDate, etc.)
3. Store request ID and QBO entity ID in mapping table
4. On retry, check mapping table first — if request ID exists, return stored entity ID
5. For journal entries: use a unique memo field pattern (e.g., `BATCH-2024-0847-COMPLETION`) and query before creating

---

## 9. Sandbox Testing

### Sandbox Environment
- Base URL: `https://sandbox-quickbooks.api.intuit.com/v3/company/{realmId}`
- Sandbox companies are created via Intuit Developer Portal
- Sandbox has same API surface as production
- Pre-populated with sample data (customers, vendors, items, transactions)
- Rate limits are the same as production

### Testing Strategy for Autonomi Agents
1. **Unit tests**: Mock QBO API responses, test business logic in isolation
2. **Integration tests**: Hit sandbox API with real HTTP calls, verify CRUD operations
3. **End-to-end tests**: Full workflow — create PO, receive goods, create bill, match, pay
4. **Regression tests**: After QBO API updates, verify all agent operations still work
5. **Load tests**: Verify rate limiter behavior under sustained 500 req/min

### Sandbox Gotchas
- Sandbox does not support webhooks (use ngrok or similar for local testing)
- Sandbox data resets periodically — do not store sandbox entity IDs long-term
- Some features (bank feeds, payment processing) are limited in sandbox
- Sandbox OAuth tokens have same lifecycle as production

---

## 10. Multi-Entity Consolidation

### Pattern for Multi-Company F&B Operations
Many F&B companies operate multiple QBO realms:
- **Autonomi Brand Co** — brand entity (revenue, marketing, SG&A)
- **Autonomi Manufacturing Co** — manufacturing entity (if owned production)
- **Autonomi Holdings** — parent entity for consolidated reporting

### Consolidation Approach
1. Each entity maintains its own QBO realm with separate OAuth tokens
2. Intercompany transactions use dedicated intercompany accounts (e.g., 1500 Due From/Due To)
3. Agent creates matching intercompany journal entries in both realms
4. Monthly consolidation: agent pulls trial balances from all realms, eliminates intercompany balances
5. Consolidated P&L and Balance Sheet generated in external reporting tool (or QBO Advanced with multi-entity add-on)

### Intercompany Transaction Pattern
```
Brand Co books:
  Dr. 5200 COGS — Co-Pack Toll Fees    $50,000
    Cr. 1510 Due To — Manufacturing Co           $50,000

Manufacturing Co books:
  Dr. 1500 Due From — Brand Co          $50,000
    Cr. 4000 Revenue — Manufacturing             $50,000
```

### Agent Responsibilities
- Ensure intercompany balances net to zero across all entities at month-end
- Flag and investigate any intercompany imbalances >$100
- Generate elimination entries for consolidated reporting
- Track transfer pricing documentation for tax compliance

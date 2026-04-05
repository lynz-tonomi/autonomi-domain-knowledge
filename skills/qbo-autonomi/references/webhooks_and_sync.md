# Webhooks & Data Synchronization

## Table of Contents

1. [Webhook Setup](#webhook-setup)
2. [Webhook Payload Format](#webhook-payload-format)
3. [HMAC-SHA256 Validation](#hmac-sha256-validation)
4. [Processing Architecture](#processing-architecture)
5. [Change Data Capture (CDC)](#change-data-capture-cdc)
6. [Recommended Sync Architecture](#recommended-sync-architecture)

---

## Webhook Setup

### Configuration in Intuit Developer Portal

1. Navigate to your app's Dashboard → Webhooks tab
2. Enter your webhook endpoint URL (must be HTTPS, publicly accessible)
3. Select the entities you want to monitor (Invoice, Bill, Payment, Customer, Vendor, Item, etc.)
4. Note the **Verifier Token** — you need this for HMAC validation
5. Intuit sends a verification request to confirm your endpoint is reachable

### Supported Events

| Operation | Description |
|-----------|-------------|
| Create | New entity created |
| Update | Existing entity modified |
| Delete | Entity deleted |
| Merge | Two entities merged (e.g., duplicate customers) |
| Void | Transaction voided |

### Supported Entities

Most transactional and reference entities support webhooks including: Account,
Bill, BillPayment, Budget, Class, CreditMemo, Currency, Customer, Department,
Deposit, Employee, Estimate, Invoice, Item, JournalEntry, Payment, Purchase,
PurchaseOrder, RefundReceipt, SalesReceipt, TaxAgency, Term, TimeActivity,
Transfer, Vendor, VendorCredit.

---

## Webhook Payload Format

Intuit delivers webhooks as HTTP POST requests with a JSON body:

```json
{
  "eventNotifications": [
    {
      "realmId": "1234567890",
      "dataChangeEvent": {
        "entities": [
          {
            "name": "Invoice",
            "id": "130",
            "operation": "Create",
            "lastUpdated": "2025-03-21T10:15:30.000Z"
          },
          {
            "name": "Payment",
            "id": "201",
            "operation": "Create",
            "lastUpdated": "2025-03-21T10:15:35.000Z"
          }
        ]
      }
    }
  ]
}
```

A single webhook delivery can contain multiple entity changes across multiple
realms (if your app serves multiple companies). The payload tells you WHAT changed
but not the new values — you must query the entity via the API to get updated data.

---

## HMAC-SHA256 Validation

Every webhook must be validated to prevent spoofed payloads. Intuit includes a
signature in the `intuit-signature` HTTP header.

### Validation Algorithm

1. Get the `intuit-signature` header value from the incoming request
2. Compute HMAC-SHA256 of the raw request body using your Verifier Token as the key
3. Base64-encode the result
4. Compare with the header value

### Python Implementation

```python
import hmac
import hashlib
import base64

def validate_webhook(request_body: bytes, signature_header: str, verifier_token: str) -> bool:
    """Validate QBO webhook HMAC-SHA256 signature."""
    computed = hmac.new(
        verifier_token.encode('utf-8'),
        request_body,
        hashlib.sha256
    ).digest()
    computed_b64 = base64.b64encode(computed).decode('utf-8')
    return hmac.compare_digest(computed_b64, signature_header)
```

### Verification Request

When you first configure your webhook URL, Intuit sends a verification payload
with a challenge. Your endpoint must:
1. Validate the HMAC signature
2. Return HTTP 200 with the challenge value in the response body

---

## Processing Architecture

### Critical Rule: Respond First, Process Later

Your webhook endpoint MUST return HTTP 200 within **3 seconds**. If it doesn't,
Intuit marks the delivery as failed and retries. Do not process the payload
synchronously — queue it for async processing.

### Recommended Flow

```
Webhook arrives
    → Validate HMAC signature
    → Return HTTP 200 immediately
    → Queue payload for async processing
    → Worker picks up payload:
        → Parse entity changes
        → For each entity: GET /v3/company/{realmId}/{entity}/{id}
        → Screen through Model Armor
        → Route to appropriate Autonomi agent
        → Update local sync state
```

### Agent Routing

Map entity changes to the responsible Autonomi agent:

| Entity | Agent | Action |
|--------|-------|--------|
| Bill (Create) | AP Agent | Review and process new bill |
| Bill (Update) | AP Agent | Check for approval status changes |
| Invoice (Create) | AR Agent | Track new receivable |
| Payment (Create) | AR Agent / Settlement Agent | Record incoming payment |
| PurchaseOrder (Create) | Procurement Agent | Confirm PO was created |
| Item (Update) | Inventory Agent | Check stock level changes |
| Vendor (Create/Update) | Procurement Agent | Update vendor records |
| Customer (Create/Update) | AR Agent | Update customer records |
| JournalEntry (Create) | Finance Agent | Review manual entries |

### Retry Behavior

If your endpoint returns non-200 or times out, Intuit retries with exponential
backoff. After several failed attempts, Intuit may temporarily disable your
webhook subscription. Monitor your webhook health via the Intuit Developer portal.

---

## Change Data Capture (CDC)

CDC is a polling-based mechanism that returns all entities changed since a given
timestamp. It complements webhooks as a reliability fallback.

### Endpoint

```
GET /v3/company/{realmId}/cdc?entities={comma_separated}&changedSince={ISO_timestamp}&minorversion=75
```

### Example

```
GET /v3/company/1234567890/cdc?entities=Invoice,Bill,Payment,Item,Vendor,Customer&changedSince=2025-03-20T00:00:00Z&minorversion=75
```

### Response Structure

```json
{
  "CDCResponse": [
    {
      "QueryResponse": [
        {
          "Invoice": [
            {"Id": "130", "SyncToken": "4", "TxnDate": "2025-03-20", ...},
            {"Id": "131", "SyncToken": "1", "TxnDate": "2025-03-21", ...}
          ]
        },
        {
          "Bill": [
            {"Id": "145", "SyncToken": "3", "VendorRef": {...}, ...}
          ]
        }
      ]
    }
  ]
}
```

### Constraints

| Constraint | Value |
|-----------|-------|
| Max look-back | 30 days |
| Max entities per response | 1,000 |
| Payload size | Full entity payloads (not just changed fields) |
| Entity limit per request | No documented limit, but keep reasonable (10-15 types) |

### Best Practices

- Poll once per day (e.g., midnight) covering the last 24-48 hours with overlap
- Use a slightly overlapping window (e.g., `changedSince = now - 26 hours`) to
  account for timezone and processing delays
- Store the `changedSince` timestamp after each successful poll
- CDC returns full entity payloads, so you get the latest state directly

---

## Recommended Sync Architecture

The most reliable pattern combines webhooks for real-time responsiveness with
daily CDC polling as a safety net:

```
┌─────────────────────────────────────────────────────┐
│                   QBO Company                        │
│                                                      │
│  Invoice created ──→ Webhook fires immediately       │
│  Bill updated    ──→ Webhook fires immediately       │
│                                                      │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│              Webhook Processor                        │
│                                                      │
│  1. Validate HMAC                                    │
│  2. Return 200 immediately                           │
│  3. Queue for async processing                       │
│  4. Fetch full entity from QBO API                   │
│  5. Screen through Model Armor                       │
│  6. Route to appropriate agent                       │
│  7. Log event with timestamp                         │
│                                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│           Daily CDC Reconciliation                    │
│                                                      │
│  Runs: Once per day (e.g., 2:00 AM tenant timezone)  │
│                                                      │
│  1. Poll CDC for all tracked entities (last 26 hrs)  │
│  2. Compare with webhook event log                   │
│  3. Identify any missed changes                      │
│  4. Process missed changes through same pipeline     │
│  5. Update sync cursor timestamp                     │
│  6. Generate sync health report                      │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Handling Duplicates

Both webhooks and CDC can report the same change. Use entity `Id` + `SyncToken`
as a deduplication key — if you've already processed a change with a given
SyncToken, skip it. This ensures idempotent processing regardless of the event
source.

### Sync State Storage

```json
// /sandbox/state/tenant_{TENANT_ID}/qbo/sync_state.json
{
  "last_cdc_poll": "2025-03-21T02:00:00Z",
  "last_webhook_received": "2025-03-21T14:30:15Z",
  "processed_events": {
    "Invoice:130:4": "2025-03-21T10:15:30Z",
    "Bill:145:3": "2025-03-21T12:20:00Z"
  },
  "missed_events_last_24h": 0,
  "sync_health": "healthy"
}
```

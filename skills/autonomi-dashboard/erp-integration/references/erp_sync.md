# ERP Sync Reference
**Skill:** erp-integration | **Domain:** sync | **Version:** 1.0.0

---

## 1. Integration Architecture Overview

Autonomi uses a hub-and-spoke integration model. Autonomi is the hub; each ERP is a spoke. AGNT-24 (ERP Sync Agent) manages the connection to each ERP. AGNT-25 (Data Pipeline Agent) handles transformation, routing, deduplication, and conflict resolution.

```
                        ┌─────────────────┐
                        │    Autonomi     │
                        │   (Hub Layer)   │
                        │   AGNT-24/25    │
                        └────────┬────────┘
              ┌──────────────────┼──────────────────┐
              ↓                  ↓                  ↓
         ┌─────────┐        ┌──────────┐       ┌──────────┐
         │SAP S/4  │        │NetSuite  │       │QuickBooks│
         │HANA     │        │Mfg       │       │Online    │
         └─────────┘        └──────────┘       └──────────┘
```

---

## 2. Sync Frequency and Method

| Data Entity | Direction | Frequency | Method |
|---|---|---|---|
| Customer orders (sales orders) | ERP → Autonomi | Real-time webhook (if available) or poll every 15 min | REST API pull |
| Production orders | Autonomi → ERP | On creation and every status change | REST API push |
| Purchase orders | Autonomi → ERP | On creation | REST API push |
| Inventory movements | Bidirectional | Every 30 min | Batch delta sync |
| Finished goods receipts | Autonomi → ERP | On QA release | Push |
| Supplier invoices | ERP → Autonomi | On creation in ERP | Webhook or 15-min poll |
| Payments (AP) | Autonomi → ERP | On settlement | Push |
| Payments (AR) | ERP → Autonomi | On receipt in ERP | Webhook or 30-min poll |
| BOM / Recipe master | ERP ← Autonomi master | On change | Push |
| Vendor master | ERP → Autonomi | On change (hourly poll) | Pull |
| Item master / SKUs | ERP → Autonomi | On change (hourly poll) | Pull |
| General ledger | Autonomi → ERP (journal entries) | Daily batch | Batch file |
| Cost center allocations | ERP → Autonomi | Monthly | Batch pull |

---

## 3. SAP S/4HANA Integration

### 3.1 Connection
- **Protocol:** SAP OData REST API (S/4HANA 2022+)
- **Authentication:** OAuth 2.0 (SAP BTP service account)
- **Base URL:** `https://{tenant}.s4hana.cloud.sap/sap/opu/odata4/sap/`

### 3.2 Key SAP Modules Connected

| Module | Purpose | Key APIs Used |
|---|---|---|
| MM (Materials Management) | PO management, GR posting, inventory | `API_PURCHASEORDER_PROCESS_SRV` |
| PP (Production Planning) | Production orders, scheduling, BOM | `API_PRODUCTION_ORDER_SRV` |
| QM (Quality Management) | Inspection lots, usage decisions, COAs | `API_QUALITY_MGMT_SRV` |
| FI/CO (Finance / Controlling) | Invoice posting, payment, cost center | `API_FINANCIALS_SRV` |
| SD (Sales & Distribution) | Customer orders (inbound to Autonomi) | `API_SALES_ORDER_SRV` |

### 3.3 Conflict Resolution — SAP

| Conflict Scenario | Rule |
|---|---|
| Same PO edited in both Autonomi and SAP simultaneously | SAP wins on financial fields (price, terms); Autonomi wins on logistics fields (delivery date, qty) |
| Inventory count discrepancy (Autonomi cycle count ≠ SAP) | If variance < 0.5%: auto-update SAP to match Autonomi; if ≥ 0.5%: flag for human review |
| Production order status mismatch | Autonomi master; push status to SAP |
| Vendor master data conflict | SAP master; pull to Autonomi |

---

## 4. NetSuite Manufacturing Integration

### 4.1 Connection
- **Protocol:** NetSuite REST API (SuiteScript 2.1)
- **Authentication:** TBA OAuth 1.0 or Token-Based Auth
- **Base URL:** `https://{accountId}.suitetalk.api.netsuite.com/services/rest/record/v1/`

### 4.2 Key Record Types Connected

| NetSuite Record | Autonomi Equivalent | Sync Direction |
|---|---|---|
| Work Order | Production Order (AGNT-03) | Bidirectional |
| Purchase Order | PO (AGNT-05) | Autonomi → NetSuite |
| Item Receipt | Goods Receipt | Autonomi → NetSuite |
| Inventory Adjustment | Cycle Count Variance | Autonomi → NetSuite |
| Vendor Bill | Supplier Invoice | NetSuite → Autonomi |
| Bill Payment | USDC Settlement | Autonomi → NetSuite |
| Invoice (customer) | AR Invoice | Autonomi → NetSuite |
| Item (inventory) | SKU / Ingredient Master | NetSuite → Autonomi |
| Assembly Item (BOM) | BOM Record | Autonomi master → push to NS |

### 4.3 Conflict Resolution — NetSuite

| Conflict Scenario | Rule |
|---|---|
| Work Order status conflict | Autonomi master; push to NetSuite |
| Price update (ingredient cost change) | NetSuite FI master; pull to Autonomi for costing |
| Customer order quantity change | NetSuite master; AGNT-01 re-evaluates demand plan |

---

## 5. QuickBooks Online Integration

### 5.1 Connection
- **Protocol:** Intuit QuickBooks REST API v3
- **Authentication:** OAuth 2.0
- **Scope:** `com.intuit.quickbooks.accounting`

### 5.2 Entities Synced

| QBO Entity | Autonomi Entity | Direction |
|---|---|---|
| Bill | Supplier invoice | AGNT-18 → QBO |
| Bill Payment | USDC or ACH payment | AGNT-17 → QBO |
| Purchase Order | PO | AGNT-05 → QBO |
| Vendor | Supplier (vendor master) | QBO ← Autonomi (Autonomi master) |
| Customer | Customer master | QBO → Autonomi |
| Invoice | Customer AR invoice | AGNT-20 → QBO |
| Payment (customer) | AR payment | QBO → Autonomi |
| Item | SKU / Ingredient | QBO → Autonomi (item catalog) |
| Journal Entry | Cost allocations, USDC wallet movements | AGNT-19 → QBO |

### 5.3 USDC Journal Entries to QBO

Every USDC payment generates a journal entry:

**USDC payment to supplier:**
```
DR: Accounts Payable — CitroSource       8,420.00
CR: USDC Operating Wallet                8,420.00
```

**USDC off-ramp (conversion to fiat):**
```
DR: Bank Account (Chase Operating)       50,000.00
DR: USDC Off-Ramp Fee Expense                75.00
CR: USDC Operating Wallet               50,075.00
```

---

## 6. Error Handling and Retry Logic

### 6.1 API Failure Handling

| Error Type | Retry Behavior | Escalation |
|---|---|---|
| HTTP 429 (Rate Limited) | Exponential backoff: 30s, 60s, 120s, 240s | Alert after 3 retries |
| HTTP 500/503 (Server Error) | Retry 3x at 60s intervals | Queue for human review if all fail |
| Authentication failure | Do not retry; alert AGNT-24; alert LynZ | Immediate; check OAuth token refresh |
| Field validation error | Log error with full payload; no retry | Human review: data mapping issue |
| Network timeout | Retry 3x immediately | Queue if all fail |

### 6.2 Dead Letter Queue

Failed sync events are placed in a Dead Letter Queue (DLQ):
- DLQ reviewed by AGNT-24 every 15 minutes
- Items resolved automatically if ERP comes back online
- Items pending > 2 hours: LynZ notification to Weston
- Items pending > 24 hours: Critical alert; manual investigation required

---

## 7. ERP Integration Dashboard

The `erp` page shows:
- Connection status for each ERP (SAP / NetSuite / QBO): green = connected, red = error
- Last successful sync timestamp per entity type
- Pending sync queue count
- Error queue count (with drill-down to individual errors)
- Sync volume (events/hour, events/day)
- Dead letter queue status

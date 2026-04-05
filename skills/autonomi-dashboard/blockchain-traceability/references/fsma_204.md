# FSMA 204 Reference
**Skill:** blockchain-traceability | **Domain:** regulatory-traceability | **Version:** 1.0.0

---

## 1. Overview — FSMA Section 204

FDA's Food Safety Modernization Act (FSMA) Section 204 — Enhanced Traceability Records — requires that food businesses maintain records sufficient to identify immediate previous and subsequent sources of food on the Food Traceability List (FTL). The final rule (21 CFR Part 1 Subpart S) took effect January 20, 2026, for large businesses.

Autonomi's FSMA 204 Recorder Agent (AGNT-13) handles all CTE and KDE recording automatically. Every record is written to the blockchain ledger in real time, creating an immutable, audit-ready traceability chain.

---

## 2. Food Traceability List (FTL) — Products Covered

PurePress Beverages produces the following FTL-covered products:

| BOM | Product | FTL Category | FTL Item |
|---|---|---|---|
| BOM-01 | OJ 500ml | Fresh-cut fruits and vegetables (squeezed juices) | 100% orange juice |
| BOM-03 | Apple 1L | Juices / juice beverages | Apple juice (FTL: fresh cider) |
| BOM-05 | Berry 250ml | Juices | Berry blend (if strawberry > 10%) |
| BOM-07 | Kombucha 355ml | Ready-to-eat foods | Fermented tea with live cultures |
| BOM-08 | Oat Milk 1L | Plant-based beverages | Not currently on FTL — monitored for updates |

---

## 3. Critical Tracking Events (CTEs)

AGNT-13 records a blockchain transaction for every CTE in the supply chain. The required CTEs under 21 CFR 1.1315 are:

### 3.1 CTE Types and Autonomi Automation

| CTE | Trigger Event | AGNT-13 Action | Blockchain TX Type |
|---|---|---|---|
| **Growing/Harvesting** | Supplier COA received with origin data | Extract origin KDEs from COA; write to ledger | `FSMA_CTE_ORIGIN` |
| **Receiving** | Lot received at dock; IoT temp confirmed | Write receipt KDEs; link to supplier lot | `FSMA_CTE_RECEIPT` |
| **Transformation** | Batch production started | Write transformation KDEs; link all input lots | `FSMA_CTE_TRANSFORM` |
| **Creation** | New FTL food created (new SKU, new lot) | Assign new traceability lot code (TLC) | `FSMA_CTE_CREATE` |
| **Shipping** | Outbound dispatch confirmed | Write shipping KDEs; link to customer TLC | `FSMA_CTE_SHIP` |
| **Receiving (subsequent)** | Customer DC confirms receipt | Write receiving KDE at downstream handler | `FSMA_CTE_RECEIVE_DS` |

---

## 4. Key Data Elements (KDEs)

### 4.1 Receiving CTE — Required KDEs

Per 21 CFR 1.1315(a), for each lot of FTL food received, record:

| KDE | Description | Autonomi Source |
|---|---|---|
| Traceability Lot Code (TLC) | Unique identifier for the lot | Auto-generated: `TLC-{SKU}-{YYYYMMDD}-{SEQ}` |
| TLC source | Where/how TLC was assigned | Supplier-assigned or receiving dock |
| Quantity and unit of measure | Weight or count received | Receiving dock scale + scan |
| Product description | Identity of the food | From PO line item |
| Location description (receiving) | Physical address where received | PPB-WH-01 registered facility |
| Date received | ISO 8601 timestamp | IoT dock sensor + system clock |
| Business name and address of source | Supplier identity | From vendor master |
| Reference document type | PO, BOL, or other | PO number from AGNT-05 |
| Reference document number | Document identifier | PO-PPB-{date}-{seq} |

### 4.2 Transformation CTE — Required KDEs

Per 21 CFR 1.1320, for food transformed from one or more FTL ingredients:

| KDE | Description | Autonomi Source |
|---|---|---|
| Input TLC(s) | All input lot TLCs used | From lot picks (AGNT-04) |
| Input quantities | Actual quantities consumed | From BOM actual consumption |
| Input location | Facility where transformation occurred | PPB-WH-01 |
| Output TLC | New TLC assigned to finished good | Auto-generated at batch start |
| Output product description | Finished product identity | From BOM record |
| Output quantity | Finished goods units produced | From production count |
| Transformation date | ISO 8601 range (start to end) | AGNT-03 batch timestamps |

### 4.3 Shipping CTE — Required KDEs

Per 21 CFR 1.1325:

| KDE | Description | Autonomi Source |
|---|---|---|
| TLC of shipped food | Finished good lot TLC | From production batch record |
| Quantity and unit of measure | Cases and units shipped | From shipping order |
| Product description | Finished product identity | BOM description |
| Location where food shipped from | Origin facility | PPB-WH-01 |
| Location where food shipped to | Customer DC or retail | From shipping order |
| Shipping date | ISO 8601 timestamp | AGNT-07 dispatch confirmation |
| Bill of lading number | Carrier document reference | From AGNT-07 tender |
| Receiver business name and address | Customer identity | From customer master |

---

## 5. One-Up One-Down Traceability

FSMA 204 requires that each entity in the supply chain maintain records linking to its immediate supplier (one-up) and immediate customer (one-down).

### 5.1 PurePress Beverages — Traceability Chain

```
SUPPLIER TIER (one-up from PPB)
  CitroSource Inc → LOT-ING-001-20260402-001 (FCOJ concentrate, 48,000 lbs)
  PacificFruit Co → LOT-ING-005-20260401-003 (Tropical blend, 180,000 lbs)
       ↓ CTE: RECEIPT
TRANSFORMATION AT PPB (PPB-WH-01)
  Batch: PPB-L03-20260404-001
  Input TLCs: LOT-ING-001, LOT-ING-005, LOT-ING-009 (citric acid), LOT-ING-010 (stevia)
  Output TLC: TLC-BOM04-20260404-001
  Product: Tropical 350ml, 455,593 units
       ↓ CTE: SHIP
CUSTOMER TIER (one-down from PPB)
  NorCal DC (Sacramento) → 18,400 cases
  Pacific NW DC (Portland) → 9,200 cases
  National 3PL Dallas → 24,600 cases
```

### 5.2 Trace Query Capability

AGNT-13 can answer any traceability query in < 4 seconds:
- "Where did the ingredient in batch PPB-L03-20260404-001 come from?" → CitroSource LOT-ING-001 (origin: Veracruz, Mexico, harvested 2026-03-12)
- "Where did all product from TLC-BOM04-20260404-001 go?" → 3 DCs, 52,200 cases distributed
- "Which customers received product from the NutSource allergen lot?" → Zero (lot blocked at receipt before any production)

---

## 6. FDA Compliance Posture

### 6.1 Record Maintenance Requirements

| Requirement | Standard | Autonomi Status |
|---|---|---|
| Records within 24 hours of a request | 21 CFR 1.1455 | < 4 seconds via blockchain query |
| Records kept for 2 years | 21 CFR 1.1455(b) | Permanent on-chain + 2-year off-chain archive |
| Electronic records acceptable | 21 CFR 1.1455(c) | Yes — blockchain records meet requirements |
| Records must be legible, stored in English | 21 CFR 1.1455(d) | Yes — all records in structured English JSON |

### 6.2 FSMA Dashboard Page (`fsma`)

The FSMA page on the Autonomi dashboard displays:
- Live CTE feed — all traceability events in real time
- Traceability lot code search — enter any TLC to see full chain
- Compliance status: all required KDEs populated (green) or missing (red)
- Recall simulation: enter a lot and trace all downstream customers in seconds
- FDA registration status and next renewal date

---

## 7. Registered Facility Information

PurePress Beverages maintains FDA facility registration as required under 21 CFR Part 1 Subpart H.

| Field | Value |
|---|---|
| Facility Registration Number | FRN-PPB-001 (simulated) |
| Facility name | PurePress Beverages, Inc. |
| Physical address | 1400 Production Blvd, Los Angeles, CA 90021 |
| Operations type | Manufacturing, Processing, Packing, Holding |
| Food categories | Beverages — Juices, Fermented Beverages, Plant-Based Beverages |
| FSMA PCHFrule compliance | 21 CFR Part 117 — confirmed |
| FSMA 204 compliance date | January 20, 2026 |
| Emergency contact | Weston Mitchell / weston@autonomi.llc |

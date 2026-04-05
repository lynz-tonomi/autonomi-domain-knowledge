# Procurement Reference
**Skill:** supply-chain-ops | **Domain:** procurement | **Version:** 1.0.0

---

## 1. Overview

The Autonomi procurement system automates vendor selection, PO generation, COA validation, and payment initiation. The Procurement Agent (AGNT-05) and Supplier Scorer Agent (AGNT-06) work in tandem: AGNT-06 maintains a live composite score for every approved vendor; AGNT-05 routes POs to the highest-scoring qualified supplier that meets lead time and price criteria. All POs above the auto-approve threshold require human confirmation before USDC payment is initiated.

---

## 2. Active Vendor Master

### 2.1 Primary Suppliers — Juice Concentrates & Purees

| Vendor ID | Vendor Name | Category | Score | Lead Time | Payment Terms | USDC Enabled |
|---|---|---|---|---|---|---|
| VND-001 | CitroSource Inc | FCOJ concentrate | 96.4 | 5 days | Net-15 USDC | Yes |
| VND-002 | PacificFruit Co | Tropical / mango purees | 94.1 | 7 days | Net-30 USDC | Yes |
| VND-003 | NutSource (suspended) | Peanut-adjacent oils | Suspended | — | — | — |
| VND-004 | AppleValley Concentrate | Apple juice conc. | 91.8 | 10 days | Net-15 USDC | Yes |
| VND-005 | BerryFarms Cooperative | Berry blend concentrate | 93.2 | 9 days | Net-30 | No (ACH) |
| VND-006 | SunVerde Citrus | Citrus juice NFC | 88.7 | 5 days | Net-15 USDC | Yes |
| VND-007 | GrainBase Oats | Oat base liquid | 90.3 | 3 days | Net-7 USDC | Yes |
| VND-008 | KombuchaCultures Ltd | SCOBY / starter | 87.4 | 14 days | Net-30 | No (ACH) |

### 2.2 Secondary / Backup Suppliers

| Vendor ID | Vendor Name | Category | Activation Trigger |
|---|---|---|---|
| VND-011 | TrapicoBlend | Tropical/mango backup | VND-002 score < 80 or OOS |
| VND-012 | Eastern Berry Co | Berry backup | VND-005 score < 80 or lead > 14 days |
| VND-013 | ClearOat Solutions | Oat base backup | VND-007 score < 80 or OOS |

### 2.3 Ingredients & Additives Suppliers

| Vendor ID | Vendor Name | Materials | Score |
|---|---|---|---|
| VND-020 | IngredChem Corp | Citric acid, malic acid, potassium sorbate | 95.1 |
| VND-021 | PureGum Supply | Xanthan gum, guar gum | 92.6 |
| VND-022 | SweetLeaf Extracts | Stevia RA97, monk fruit | 94.8 |
| VND-023 | OmegaVit Inc | Vitamin C, vitamin D3 | 91.3 |
| VND-024 | PackagePros | PET preforms, HDPE caps | 96.0 |
| VND-025 | LabelWorks | Labels, shrink sleeves | 88.2 |

---

## 3. Supplier Scoring Model

AGNT-06 calculates a composite supplier score (0–100) updated after every delivery event and COA submission.

### 3.1 Score Weights

| Dimension | Weight | Data Source |
|---|---|---|
| On-Time Delivery | 30% | Delivery timestamp vs. PO requested date |
| Quality Conformance | 30% | COA pass rate + rejection rate |
| Fill Rate (order completeness) | 20% | Units delivered / units ordered |
| Responsiveness | 10% | Time to respond to PO, deviation, or escalation |
| Price Stability | 10% | Price variance vs. last-3-order average |

### 3.2 Score Thresholds

| Score Range | Status | Actions Available |
|---|---|---|
| 90–100 | Preferred | Auto-route POs; USDC payment on delivery |
| 80–89 | Approved | Standard routing; human PO approval for > $10K |
| 70–79 | Probationary | Backup-only; require COA pre-receipt |
| 60–69 | Under Review | Escalate to procurement manager; suspend new POs |
| < 60 | Suspended | Block all new POs; initiate re-qualification or replacement |

### 3.3 Score Recovery

A suspended vendor can re-enter the approved list through a formal re-qualification process:
1. Root cause analysis submitted in writing
2. On-site audit or desktop review (depending on risk level)
3. 3-lot probationary delivery period with 100% COA acceptance
4. Score recalculated; if ≥ 80, status restored to Approved

---

## 4. Purchase Order Automation

### 4.1 PO Generation Logic

AGNT-05 generates a draft PO when:
- On-hand quantity drops to the reorder point (see inventory_management.md Section 4.2)
- FEFO timer triggers a fast-consumption requirement
- Production Scheduler confirms a batch within the next 72 hrs without covered ingredients
- Manual override by Weston or operations manager

### 4.2 Auto-Approve Thresholds

| PO Value (USDC / USD equiv.) | Action |
|---|---|
| ≤ $2,500 | Auto-approved by AGNT-05; USDC payment initiated immediately on delivery confirmation |
| $2,501–$10,000 | Auto-generated; requires Weston's 1-click approval in Agentic Wallet |
| $10,001–$25,000 | Generated with recommendation; requires operations manager approval |
| > $25,000 | Generated with full cost analysis; requires CFO-level approval via BILL.com AP workflow |

### 4.3 PO Fields

| Field | Description |
|---|---|
| `po_number` | System-generated: `PO-{SITE}-{YYYYMMDD}-{SEQ}` |
| `vendor_id` | From vendor master |
| `line_items` | Array of {sku, description, qty, unit, unit_price, extended_price} |
| `requested_delivery` | Date required at dock |
| `ship_to` | PPB-WH-01 dock address |
| `payment_method` | USDC (Base L2) or ACH |
| `payment_terms` | From vendor master |
| `smart_contract_trigger` | IoT condition required for auto-payment (e.g., temp ≤ 40°F confirmed, quantity verified) |
| `blockchain_tx_id` | Written on PO issuance and each status update |

---

## 5. COA Validation

### 5.1 Process

Certificate of Analysis (COA) documents are required for every incoming lot of ingredients. AGNT-06 runs automated COA validation:

1. Supplier uploads COA via supplier portal (PDF or structured JSON)
2. AGNT-06 extracts key values via document parsing
3. Values compared against internal spec limits
4. Pass/fail result written to lot record
5. Lot placed on Hold if COA fails; QA Agent (AGNT-08) notified

### 5.2 COA Parameters Checked by Product Category

**Juice Concentrates (Brix, microbiological, heavy metals):**

| Parameter | Spec Limit | Test Method |
|---|---|---|
| Brix (FCOJ) | 65.0–66.0 °Bx | AOAC 932.14 |
| Brix (single-strength NFC) | 11.0–12.5 °Bx | AOAC 932.14 |
| pH | 3.4–4.0 | AOAC 942.15 |
| Total plate count | ≤ 1,000 CFU/mL | FDA BAM |
| Yeast & mold | ≤ 100 CFU/mL | FDA BAM |
| E. coli O157:H7 | Negative / 25g | FDA BAM |
| Patulin (apple products) | ≤ 50 ppb | FDA/AOAC |
| Lead | ≤ 0.01 ppm | ICP-MS |
| Cadmium | ≤ 0.01 ppm | ICP-MS |

**Oat Base:**

| Parameter | Spec Limit |
|---|---|
| Protein | ≥ 1.5% w/v |
| Fat | 0.5–1.5% |
| Total solids | 10.0–13.0% |
| Gluten (ELISA) | ≤ 20 ppm (if gluten-free claim) |
| Total plate count | ≤ 500 CFU/mL |

**Dry Ingredients (Citric Acid, Xanthan, Stevia):**

| Parameter | Spec Limit |
|---|---|
| Assay (citric acid) | ≥ 99.5% anhydrous |
| Viscosity (xanthan, 1% solution) | 1,200–1,600 cP at 25°C |
| Rebaudioside A (stevia) | ≥ 97.0% |
| Moisture (all dry) | ≤ 5.0% |
| Heavy metals (total) | ≤ 10 ppm |

---

## 6. Emergency Procurement Protocol

When a critical ingredient falls below safety stock unexpectedly (stockout risk within 72 hrs):

1. AGNT-05 issues emergency PO to primary supplier (premium freight)
2. If primary supplier ETA > 48 hrs, backup supplier activated simultaneously
3. Production Scheduler alerted to defer affected batches if necessary
4. AGNT-05 escalates to Weston via LynZ voice notification
5. USDC payment pre-authorized for expedited delivery up to $15,000 (emergency override)
6. All emergency procurement events logged to blockchain with escalation chain

---

## 7. Procurement KPIs

| KPI | Target | Current |
|---|---|---|
| PO Cycle Time (from trigger to issuance) | ≤ 4 hrs | 1.8 hrs avg |
| OTIF (Supplier On Time In Full) | ≥ 95% | 96.2% |
| COA Pass Rate (first submission) | ≥ 98% | 97.4% |
| PO Automation Rate (auto-approved) | ≥ 70% | 78.3% |
| Supplier Score (avg, approved vendors) | ≥ 90 | 92.7 |
| Emergency POs (monthly) | ≤ 2 | 1 (last month) |
| Cost Variance vs. Budget | ≤ ±5% | +1.8% |

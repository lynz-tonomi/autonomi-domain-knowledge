# Inventory Management Reference
**Skill:** supply-chain-ops | **Domain:** inventory | **Version:** 1.0.0

---

## 1. Overview

Inventory management on the Autonomi platform enforces FEFO (First Expired, First Out) rotation, maintains safety stock buffers calibrated to lead time variability, and monitors cold chain storage conditions for perishable ingredients. The Inventory Agent (AGNT-04) manages all stock movement logic and surfaces alerts when any SKU drops below its dynamic reorder point. All lot movements are recorded to the blockchain ledger for full FSMA 204 traceability.

---

## 2. Warehouse Layout — PurePress Beverages (Site: PPB-WH-01)

| Zone | Zone ID | Temp Range | Capacity (pallets) | Contents |
|---|---|---|---|---|
| Ambient dry storage | ZONE-A | 60–75°F / 15.5–23.9°C | 480 | Packaging, sweeteners, dry ingredients |
| Refrigerated ingredients | ZONE-R | 34–40°F / 1.1–4.4°C | 120 | Juice concentrates, NFC juice, cultures |
| Frozen concentrate | ZONE-F | -10–0°F / -23.3– -17.8°C | 64 | FCOJ, frozen fruit purees |
| Finished goods cold | ZONE-FG-C | 34–40°F / 1.1–4.4°C | 240 | Cold-fill finished goods, kombucha |
| Finished goods ambient | ZONE-FG-A | 60–75°F / 15.5–23.9°C | 320 | Hot-fill shelf-stable products |
| Quarantine | ZONE-Q | Matches source zone | 24 | Holds, returns, disputed lots |

**Total pallet capacity:** 1,248  
**Current utilization:** 68.4% (855 pallets active)

---

## 3. FEFO Enforcement Rules

### 3.1 Policy
All picking and production consumption follows FEFO, not FIFO. The system issues a **blocking alert** if a pick list would consume a lot with a later expiry date before one with an earlier expiry date.

### 3.2 FEFO Trigger Thresholds

| Shelf Life Remaining | Action |
|---|---|
| > 60 days | Normal — no action |
| 30–60 days | Yellow flag — prioritize in next production run |
| 15–30 days | Orange alert — Production Scheduler promoted to Tier 1 |
| 7–15 days | Red alert — LynZ voice notification + AGNT-04 auto-schedules consumption run |
| < 7 days | Critical — AGNT-04 escalates to human; disposal authorization required if no run feasible |

### 3.3 Shelf Life by Ingredient Category

| Category | Typical Shelf Life | Storage Zone |
|---|---|---|
| FCOJ (frozen) | 24 months | ZONE-F |
| NFC juice (refrigerated) | 21–45 days | ZONE-R |
| Juice concentrate (refrigerated) | 12–18 months | ZONE-R |
| Fruit purees (frozen) | 18–24 months | ZONE-F |
| Citric acid (dry) | 36 months | ZONE-A |
| Malic acid (dry) | 36 months | ZONE-A |
| Potassium sorbate (dry) | 36 months | ZONE-A |
| Xanthan gum (dry) | 24 months | ZONE-A |
| Stevia extract (dry) | 24 months | ZONE-A |
| Oat base (refrigerated) | 30 days | ZONE-R |
| Kombucha culture (live) | 14 days active | ZONE-R |
| PET preforms | 24 months | ZONE-A |
| HDPE caps | 36 months | ZONE-A |
| Labels / shrink sleeves | 24 months | ZONE-A |

---

## 4. Safety Stock Calculation

### 4.1 Formula

Safety Stock = Z × σ_LT × √LT_avg

Where:
- Z = service level factor (1.65 for 95%, 2.05 for 98%, 2.33 for 99%)
- σ_LT = standard deviation of daily demand during lead time
- LT_avg = average lead time in days

**PurePress standard service level:** 98% (Z = 2.05)

### 4.2 Reorder Point

ROP = (Average Daily Demand × Lead Time) + Safety Stock

### 4.3 Active Safety Stock Settings by Key Ingredient

| Ingredient | SKU | Avg Daily Usage (lbs) | σ Daily | Lead Time (days) | Safety Stock (lbs) | ROP (lbs) |
|---|---|---|---|---|---|---|
| FCOJ concentrate | ING-001 | 4,820 | 612 | 7 | 3,328 | 37,068 |
| Apple juice concentrate | ING-002 | 2,140 | 285 | 10 | 1,847 | 23,247 |
| Citrus juice blend | ING-003 | 5,610 | 743 | 5 | 3,408 | 31,458 |
| Mango puree | ING-004 | 3,280 | 488 | 12 | 3,459 | 42,819 |
| Tropical fruit blend | ING-005 | 6,920 | 890 | 8 | 5,157 | 60,517 |
| Berry blend concentrate | ING-006 | 4,110 | 524 | 9 | 3,221 | 40,211 |
| Oat base liquid | ING-007 | 1,840 | 210 | 3 | 729 | 6,249 |
| Kombucha SCOBY / starter | ING-008 | 380 | 62 | 14 | 475 | 5,795 |
| Citric acid | ING-009 | 124 | 18 | 21 | 170 | 2,774 |
| Stevia RA97 | ING-010 | 42 | 8 | 28 | 77 | 1,253 |
| Xanthan gum | ING-011 | 38 | 6 | 21 | 58 | 856 |
| Potassium sorbate | ING-012 | 29 | 5 | 21 | 48 | 657 |

---

## 5. Lot Tracking and Traceability

### 5.1 Lot Record Fields

Every inventory lot carries the following data fields, all written to the blockchain on receipt:

| Field | Description |
|---|---|
| `lot_id` | Internal lot number (format: `LOT-{SKU}-{YYYYMMDD}-{SEQ}`) |
| `supplier_lot` | Supplier's own lot/batch number |
| `supplier_id` | Linked to vendor master |
| `po_number` | Purchase order that generated the receipt |
| `received_date` | ISO 8601 timestamp |
| `quantity_received` | Gross weight (lbs) |
| `quantity_on_hand` | Current balance after consumption |
| `expiry_date` | Best-by or use-by date from COA |
| `coa_hash` | SHA-256 hash of supplier COA PDF |
| `storage_zone` | Assigned warehouse zone |
| `temperature_at_receipt` | Reading from receiving dock IoT sensor |
| `hold_status` | Released / Hold / Quarantine |
| `blockchain_tx_id` | Immutable transaction ID on Hyperledger |

### 5.2 Lot Consumption Recording

When a lot is consumed in production, the following events are recorded:

1. **Lot pick confirmed** — lot_id + quantity_picked + production_batch_id
2. **Consumption posted** — actual quantity used vs. BOM standard
3. **Yield variance** — actual vs. theoretical yield flagged if > ±2%
4. **Remaining balance** — updated in real time; zero-balance lots archived

---

## 6. Cycle Counting Program

### 6.1 Frequency

| ABC Class | Criteria | Count Frequency |
|---|---|---|
| A | Top 20% by value (covers 80% of ingredient spend) | Weekly |
| B | Next 30% by value | Monthly |
| C | Remaining 50% by value | Quarterly |

### 6.2 Variance Thresholds

| Variance Level | Action |
|---|---|
| ≤ 0.5% by weight | Acceptable — adjust system balance |
| 0.5–2.0% | Investigate: check for unreported damage, mis-picks, scale error |
| > 2.0% | Significant — full recount, root cause investigation, CAPA if recurrent |

---

## 7. Cold Chain Compliance

### 7.1 Refrigerated Zone (ZONE-R) Parameters

| Parameter | Spec | Alert Threshold | Critical Threshold |
|---|---|---|---|
| Temperature | 34–40°F (1.1–4.4°C) | > 42°F (5.6°C) | > 45°F (7.2°C) |
| Humidity | 75–85% RH | > 90% RH | > 95% RH |
| Door open time | < 3 min per event | > 5 min | > 10 min |
| Monitoring interval | Every 5 min | — | — |

### 7.2 Frozen Zone (ZONE-F) Parameters

| Parameter | Spec | Alert Threshold | Critical Threshold |
|---|---|---|---|
| Temperature | -10–0°F (-23.3– -17.8°C) | > 5°F (-15°C) | > 15°F (-9.4°C) |
| Defrost cycles | 2x per day max | — | > 3x/day triggers investigation |
| Monitoring interval | Every 5 min | — | — |

### 7.3 Cold Chain Excursion Protocol

1. IoT sensor triggers alert → AGNT-19 fires to LynZ
2. LynZ notifies Weston via voice + dashboard toast
3. AGNT-04 places affected lots on Hold status
4. QA Agent (AGNT-08) initiates temperature excursion review
5. Lot disposition: Release / Rework / Dispose — requires human sign-off
6. All actions recorded to blockchain with timestamps

---

## 8. Dashboard Inventory KPIs

| KPI | Target | Current |
|---|---|---|
| Inventory Turn Rate | ≥ 12x annually | 13.4x |
| Days of Supply (A-class ingredients) | 14–21 days | 17.2 days |
| FEFO Compliance Rate | 100% | 99.8% |
| Cycle Count Accuracy (A-class) | ≥ 99.5% | 99.6% |
| Stockout Events (monthly) | 0 | 0 (last 4 months) |
| Excess Stock (> 90 days supply) | < 5% of SKUs | 3.1% |
| Cold Chain Excursions (monthly) | 0 | 1 (minor, resolved) |

---

## 9. Agent Decision Rules

**AGNT-04 auto-approves:**
- FEFO rotation assignments (no threshold)
- Cycle count adjustments ≤ 0.5% variance
- Hold placement on excursion lots pending QA review

**AGNT-04 escalates to human:**
- Variance > 2% on any A-class ingredient
- Cold chain excursion on a lot with confirmed customer order
- Lot disposal recommendation > $5,000 value
- Any Hold removal on a previously flagged lot

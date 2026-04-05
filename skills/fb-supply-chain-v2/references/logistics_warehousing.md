# Logistics & Warehousing — Deep Reference

## 6.1 Data Schema

| Field | Type | Unit | Typical Range |
|-------|------|------|---------------|
| `shipment_id` | string | — | — |
| `carrier` | string | — | — |
| `mode` | enum | — | TL, LTL, intermodal, parcel |
| `origin` | string | — | Warehouse/plant ID |
| `destination` | string | — | Customer DC or store |
| `ship_date` | date | — | — |
| `delivery_date` | date | — | — |
| `pallets` | int | — | 1–22 per truck |
| `weight_lbs` | float | lbs | Max 44,000 for standard TL |
| `temperature_required` | enum | — | ambient, refrigerated, frozen |
| `otif_status` | enum | — | on_time_in_full, late, short, both |
| `freight_cost` | float | $ | — |
| `cost_per_case` | float | $/case | — |

## 6.2 Cold Chain Requirements

```
REFRIGERATED (target ≤38°F / 3.3°C):
  Log temperature: every 15 min during transit
  FLAG if temp > 40°F for > 30 consecutive minutes
  REJECT LOAD if temp > 45°F at any single reading

FROZEN (target ≤0°F / -18°C):
  Log temperature: every 15 min during transit
  FLAG if temp > 5°F for > 30 consecutive minutes
  REJECT LOAD if temp > 10°F at any single reading
  Evidence of thaw/refreeze (ice crystals, wet cases) = REJECT

AMBIENT:
  No active monitoring required
  Do not transport in direct sun or with incompatible goods
  Max trailer temp should not exceed 90°F

COLD CHAIN BREAK POINTS (most common failures):
  1. Loading dock — product sitting on warm dock waiting for trailer
  2. Driver stops — engine off may shut down reefer on some units
  3. Cross-dock facilities — product exposed during transfer
  4. Last mile — DTC delivery without insulated packaging
```

### Reefer Pre-cool Requirements

```
BEFORE LOADING:
  Reefer trailer must be pre-cooled to within 5°F of target temp
  Verify with probe thermometer, not just reefer display
  Document pre-cool temp on BOL

LOADING RULES:
  Do not block airflow between pallets (2" minimum gap)
  Do not stack above red line in trailer
  Load heaviest pallets first (near cab), lightest near doors
  For mixed-temp loads: use bulkhead partition (rare — avoid if possible)
```

## 6.3 OTIF Metrics

```
ON-TIME:
  Delivered within ±1 day of requested delivery date (general trade)
  Retail customers (Walmart, Kroger, etc.): ±0 days — MUST HIT exact window

IN-FULL:
  Shipped quantity ≥ 95% of ordered quantity (general trade)
  Retail customers: 100% — shorts = chargeback

OTIF = (on_time_shipments ∩ in_full_shipments) / total_shipments × 100

TARGETS:
  Industry average: 85–90%
  Retail requirement: 95–98%
  Target: ≥95%

CHARGEBACK REFERENCE:
  Walmart OTIF fine: ~3% of COGS per violation
  Kroger: variable, typically $500–$2,000 per incident
  Amazon: variable, deducted from payment
  Target (retailer): similar structure to Walmart
```

### OTIF Root Cause Analysis

```
IF otif_status != 'on_time_in_full':
  CATEGORIZE root cause:
    LATE causes:
      - Carrier missed pickup window
      - Production delay (batch not ready)
      - Carrier transit delay (weather, mechanical)
      - Appointment not available at consignee
    SHORT causes:
      - Insufficient inventory at ship point
      - Pick/pack error
      - Damaged product during loading
      - Order entry error
  LOG root cause for trend analysis
  FLAG if same root cause occurs 3+ times in 30 days
```

## 6.4 Freight Cost Benchmarks

| Mode | Cost Range | Typical Use |
|------|-----------|-------------|
| Full truckload (TL, dry) | $2.50–$4.50/mile | ≥20 pallets, 300+ miles |
| Full truckload (TL, reefer) | $3.50–$6.00/mile | Refrigerated/frozen |
| LTL (dry) | $15–$40/cwt | 1–10 pallets |
| LTL (reefer) | $25–$60/cwt | 1–6 pallets, temp-controlled |
| Intermodal | $1.50–$3.00/mile | ≥1,000 miles, non-urgent, shelf-stable |
| Parcel (DTC) | $8–$25/package | Direct-to-consumer |

```
FREIGHT COST PER CASE:
  freight_per_case = total_freight_cost / total_cases_shipped

TARGET: freight_per_case < 5% of wholesale case price
FLAG if > 8%

FTL vs LTL BREAK-EVEN:
  Calculate cost per case for FTL vs LTL at various volumes
  Break-even typically at 8,000–12,000 lbs (varies by lane)
  IF shipment_weight > break_even_lbs: use FTL
  IF shipment_weight < break_even_lbs: use LTL or consolidate
```

## 6.5 Warehouse Slotting

```
SLOTTING PRIORITY:
  A movers (top 20% by velocity):    Ground-level pick slots, closest to dock
  B movers (next 30%):               Second-tier pick, moderate distance
  C movers (bottom 50%):             Upper rack, farthest from dock

TEMPERATURE ZONE ASSIGNMENT:
  ambient_items      → dry warehouse (60–80°F)
  refrigerated_items → cooler (34–38°F)
  frozen_items       → freezer (-10°F to 0°F)

ALLERGEN SEGREGATION IN WAREHOUSE:
  Top 9 allergens: store in dedicated zones where possible
  If shared zone: allergen items stored BELOW non-allergen items (spill containment)
  Peanut and tree nut ingredients: separate locked cage or dedicated area
  Maintain allergen zone map — update when products are added/removed
```

### Pallet Configuration Reference

| Format | Cases/Pallet (std 48×40) | Lbs/Pallet (approx) |
|--------|------------------------|---------------------|
| 12oz cans (24-pack) | 84–100 | 1,800–2,200 |
| 16oz bottles (12-pack) | 72–84 | 1,400–1,700 |
| 32oz / 1L bottles (12-pack) | 48–60 | 1,200–1,500 |
| 500ml bottles (24-pack) | 60–72 | 1,600–1,900 |
| Gallon jugs (4-pack) | 36–48 | 1,200–1,600 |

```
TRUCK CAPACITY:
  Standard 53ft trailer: 20–22 pallets
  Cases per truck: ~1,500–2,200 (varies by format)
  Weight limit: 44,000 lbs (including pallets)

CONSTRAINT CHECK:
  IF total_weight > 44,000 lbs:
    CUBE-OUT — reduce pallets to meet weight limit
  IF total_pallets > 22:
    WEIGHT-OUT — split shipment or use larger trailer
  → Always check which constrains first: cube or weight
```

## 6.6 3PL Management

### 3PL Cost Structure

| Charge Type | Typical Range | Notes |
|------------|--------------|-------|
| Storage (ambient) | $8–$15/pallet/month | — |
| Storage (refrigerated) | $15–$25/pallet/month | — |
| Storage (frozen) | $20–$35/pallet/month | — |
| Handling in | $0.15–$0.50/case | Receiving and putaway |
| Handling out | $0.15–$0.50/case | Pick and load |
| Order pick | $2–$5/order + $0.30–$0.75/line | Per-order + per-line |
| Value-added services | Per unit or per hour | Labeling, kitting, display building |
| Accessorials | Variable | Detention, lumper, pallet exchange |

### 3PL SLA Metrics

```
3PL SCORECARD:
  Inventory accuracy: >99.5%
  Order accuracy (right product, right quantity): >99.5%
  On-time shipping: >98%
  FEFO compliance: >99%
  Receiving turnaround: <24 hrs from arrival to putaway
  Temperature compliance: 100% (no excursions)

REVIEW: Monthly with 3PL operations team
FLAG: Any metric below threshold for 2 consecutive months
```

## 6.7 Failure Modes

| Failure | Detection | Action |
|---------|-----------|--------|
| Cold chain break in transit | Temperature logger alarm at delivery | Quarantine load, quality assessment, file carrier claim |
| OTIF miss on key account | Delivery confirmation vs PO | Root cause analysis, corrective action, customer notification |
| Freight cost > 8% of case price | Cost analysis | Review mode selection, consolidation opportunities, carrier negotiation |
| 3PL inventory discrepancy | Cycle count vs system | Joint investigation, adjust inventory, implement controls |
| Damaged product at delivery | Receiving inspection at customer | File carrier claim, replace product, investigate packaging adequacy |
| Detention charges recurring | Invoice analysis | Improve appointment scheduling, staging, dock procedures |

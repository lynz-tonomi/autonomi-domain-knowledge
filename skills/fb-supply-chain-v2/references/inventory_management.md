# Inventory Management — Deep Reference

## 4.1 Data Schema

| Field | Type | Unit | Typical Range |
|-------|------|------|---------------|
| `item_id` | string | — | RM/PM/FG prefix |
| `item_type` | enum | — | raw_material, packaging, finished_good, WIP |
| `lot_number` | string | — | Supplier lot or internal lot |
| `received_date` | date | — | — |
| `expiration_date` | date | — | — |
| `manufacture_date` | date | — | — |
| `quantity_on_hand` | float | lbs/units/cases | — |
| `quantity_allocated` | float | lbs/units/cases | Committed to open work orders |
| `quantity_available` | float | lbs/units/cases | on_hand − allocated |
| `location` | string | — | Warehouse zone + bin |
| `temperature_zone` | enum | — | ambient, refrigerated, frozen |
| `hold_status` | enum | — | available, qa_hold, supplier_hold, recall_hold |
| `days_of_supply` | float | days | Calculated field |

## 4.2 FEFO / FIFO Logic

```
FEFO (First Expired, First Out) — DEFAULT for all F&B:
  SELECT lot WHERE item_id = X AND hold_status = 'available'
  ORDER BY expiration_date ASC, received_date ASC
  → Always consume nearest-expiry lot first

FIFO (First In, First Out) — fallback when no expiration (e.g., packaging):
  SELECT lot WHERE item_id = X AND hold_status = 'available'
  ORDER BY received_date ASC
```

### Expiry Flagging Rules

```
IF days_until_expiry < 30:  FLAG 'EXPIRING_SOON'
IF days_until_expiry < 7:   FLAG 'CRITICAL_EXPIRY'
IF days_until_expiry < 0:   FLAG 'EXPIRED' — do not allocate, quarantine immediately
IF quantity_available < safety_stock: FLAG 'BELOW_SAFETY_STOCK'
IF quantity_available < 0:   FLAG 'NEGATIVE_INVENTORY' — cycle count required
```

### Retailer Minimum Shelf Life Requirements

```
remaining_shelf_life_pct = days_until_expiry / total_shelf_life_days × 100

Retailer minimums:
  Most grocery: 60–75% remaining at delivery
  Club stores (Costco, Sam's): 75%+
  Convenience: 50% (smaller packs, faster turns)
  Amazon: 90 days minimum remaining (varies by category)

SHIPPABLE CHECK:
  IF remaining_shelf_life_pct < retailer_minimum_pct:
    DO NOT SHIP to that retailer
    → Redirect to DTC, foodservice, discount, or donate
```

## 4.3 Safety Stock & Reorder Points

```
SAFETY STOCK (standard):
  safety_stock = z_score × std_dev_demand × sqrt(lead_time_days)

z_score by service level:
  90% = 1.28
  95% = 1.65
  97% = 1.88
  99% = 2.33

SAFETY STOCK (with lead time variability):
  safety_stock = sqrt(
    (z × std_dev_demand × sqrt(avg_lead_time))² +
    (z × avg_demand × std_dev_lead_time)²
  )

REORDER POINT:
  reorder_point = (avg_daily_usage × lead_time_days) + safety_stock

DAYS OF SUPPLY:
  days_of_supply = quantity_available / avg_daily_usage
```

### F&B-Specific Safety Stock Caps

```
MAX USEFUL SAFETY STOCK:
  max_safety_stock = daily_demand × (shelf_life_days − retailer_min_dte − production_lead_time_days)

ACTUAL SAFETY STOCK:
  actual_safety_stock = min(calculated_safety_stock, max_useful_safety_stock)

→ Safety stock that would expire before use is waste, not safety.
```

### Reorder Decision

```
IF days_of_supply < lead_time_days + safety_stock_days:
  GENERATE PO (see Procurement reference)

IF days_of_supply < lead_time_days:
  FLAG 'STOCKOUT_RISK' — expedite or find alternate supplier

IF days_of_supply < 0:
  FLAG 'STOCKOUT' — production at risk, escalate immediately
```

## 4.4 Shelf Life Reference

| Category | Typical Shelf Life | Storage Temp | Notes |
|----------|-------------------|-------------|-------|
| Juice (hot-fill, pasteurized) | 9–18 months | Ambient | Vitamin degradation over time |
| Juice (HPP) | 30–90 days | Refrigerated (≤38°F) | Short shelf life, premium price |
| Kombucha (raw) | 60–120 days | Refrigerated (≤38°F) | Active fermentation continues |
| Oat milk (aseptic) | 9–12 months | Ambient (until opened) | Separation expected — shake well |
| Oat milk (refrigerated) | 7–14 days | Refrigerated | Ultra-short, perishable |
| Cold brew coffee | 90–180 days | Refrigerated | Nitrogen-flushed extends life |
| Functional / energy drinks | 12–24 months | Ambient | Vitamin C degrades ~10%/year |
| Concentrates (frozen) | 12–24 months | Frozen (≤0°F) | Thaw before use — plan lead time |
| Raw ingredients (dry) | 6–24 months | Ambient, dry | Varies widely by ingredient |
| Raw ingredients (refrigerated) | 7–90 days | Refrigerated | Dairy cultures, fresh fruit purees |

### Days-to-Expiry Classification

```
Green zone  (>60% remaining): Full value, ship to any channel
Yellow zone (30–60% remaining): May not meet retailer minimums;
  prioritize for DTC, foodservice, or discount channels
Red zone    (10–30% remaining): Markdown, donate, or use as ingredient in other products
Expired     (<0 DTE): Dispose. Calculate write-off cost.
```

## 4.5 Cycle Counting

```
CYCLE COUNT FREQUENCY (ABC-based):
  A items (top 20% by value):    Count weekly
  B items (next 30% by value):   Count monthly
  C items (bottom 50% by value): Count quarterly

TOLERANCE THRESHOLDS:
  Raw materials (by weight): ±2%
  Packaging (by count):      ±1%
  Finished goods (by case):  ±0.5%

IF variance > tolerance:
  FLAG 'COUNT_VARIANCE'
  Investigate: receiving errors, unreported scrap, theft, misallocation
  Adjust inventory ONLY after root cause documented and approved
```

### Inventory Accuracy KPI

```
inventory_accuracy = (locations_where_system_matches_physical / total_locations_counted) × 100
TARGET: >99%
FLAG if < 97%
```

## 4.6 ABC/XYZ Classification

### ABC (Value-based)

- **A items** (top 80% of revenue, ~20% of SKUs): Highest service level, tightest controls.
- **B items** (next 15% of revenue): Moderate controls.
- **C items** (bottom 5% of revenue): Simplest controls, candidates for SKU rationalization.

### XYZ (Demand variability, by coefficient of variation)

- **X** (CV < 0.5): Stable demand, easy to forecast, lean inventory.
- **Y** (0.5 ≤ CV < 1.0): Moderate variability, moderate safety stock.
- **Z** (CV ≥ 1.0): Highly variable/sporadic, make-to-order if possible.

### Combined Decision Matrix

| | X (Stable) | Y (Variable) | Z (Erratic) |
|---|-----------|-------------|-------------|
| **A** (High value) | Lean flow, low safety stock, JIT | Moderate buffer, forecast closely | High value + unpredictable = strategic buffer or MTO |
| **B** (Medium value) | Standard replenishment | Standard + safety stock | Review: worth carrying? |
| **C** (Low value) | Auto-replenish, minimal effort | Minimal safety stock | Strongest candidates for discontinuation |

## 4.7 Lot Tracking Requirements

Every inventory transaction must record:

| Field | Required |
|-------|----------|
| Lot / batch number | Yes |
| Quantity | Yes |
| Location (warehouse, zone, bin) | Yes |
| Date/time of transaction | Yes |
| Transaction type | Yes (receipt, pick, ship, adjust, dispose, transfer) |
| Reason code (for adjustments) | Yes |
| Operator / user ID | Yes |

This data powers recall readiness. Mock recall target: trace a finished product lot to all ingredient lots (and vice versa) within 4 hours.

## 4.8 Temperature Zone Management

```
Zone utilization = current_pallet_positions / zone_capacity_pallet_positions × 100

Cost multipliers (vs ambient):
  Refrigerated: 2–3× more expensive per pallet position
  Frozen: 3–4× more expensive per pallet position

ALERT:
  IF zone_utilization > 90%: FLAG 'ZONE_NEAR_CAPACITY'
  IF zone_utilization > 95%: FLAG 'ZONE_CRITICAL' — arrange overflow
```

## 4.9 Failure Modes

| Failure | Detection | Action |
|---------|-----------|--------|
| FEFO violation | Shipment contains lot with later expiry when earlier-expiry lot was available | Investigate WMS pick logic, retrain warehouse staff |
| Expired product shipped | `expiration_date < ship_date` | Customer notification, potential recall, root cause in WMS |
| Negative inventory | `quantity_on_hand < 0` | Immediate cycle count, transaction audit |
| Below safety stock for A-item | `days_of_supply < safety_stock_days` for A-class item | Expedite PO or transfer from another location |
| Temperature excursion in storage | Temperature logger alarm | Quarantine affected product, quality assessment |
| Allergen cross-contact in warehouse | Physical inspection or incident report | Quarantine both products, assess contamination scope |

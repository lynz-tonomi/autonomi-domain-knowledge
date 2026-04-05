# Cost Management — Deep Reference

## 10.1 Data Schema

| Field | Type | Unit | Typical Range |
|-------|------|------|---------------|
| `sku_id` | string | — | — |
| `ingredient_cost_per_unit` | float | $/unit | Sum of all ingredient costs |
| `packaging_cost_per_unit` | float | $/unit | Bottle + cap + label + case + shrink |
| `labor_cost_per_unit` | float | $/unit | Direct labor allocated |
| `overhead_cost_per_unit` | float | $/unit | Facility, utilities, depreciation |
| `freight_cost_per_unit` | float | $/unit | Outbound freight allocated |
| `cogs_per_unit` | float | $/unit | Sum of all above |
| `wholesale_price` | float | $/unit | — |
| `gross_margin_pct` | float | % | — |

## 10.2 COGS Buildup

```
INGREDIENT COST PER UNIT:
  For each ingredient in BOM:
    ingredient_cost_i = (formula_pct_i / 100) × density_lb_per_gal × (fill_size_oz / 128) × price_per_lb_i
  total_ingredient_cost = Σ ingredient_cost_i

PACKAGING COST PER UNIT:
  packaging_cost = bottle_cost + cap_cost + label_cost
                 + (case_cost / units_per_case)
                 + (shrink_cost / units_per_case)
                 + (pallet_cost / units_per_pallet)

LABOR COST PER UNIT:
  labor_cost = direct_labor_rate_per_hr / line_speed_units_per_hr
  → Include all direct operators: mixer, filler, palletizer, QC

OVERHEAD COST PER UNIT:
  overhead_cost = facility_overhead_per_hr / line_speed_units_per_hr
  → Includes: utilities, depreciation, maintenance, insurance, QA lab

CO-PACK FEE (if applicable):
  copack_cost = per_unit_fee + (per_run_fee / units_per_run)

COGS PER UNIT:
  cogs = ingredient_cost + packaging_cost + labor_cost + overhead_cost + copack_cost
```

### Typical COGS Breakdown for Beverages

| Component | % of COGS (typical range) |
|-----------|--------------------------|
| Ingredients | 30–50% |
| Packaging | 25–40% |
| Direct labor | 5–15% |
| Overhead | 10–20% |
| Co-pack fee (if applicable) | replaces labor + overhead |

## 10.3 Margin Analysis

```
GROSS MARGIN:
  gross_margin_pct = ((wholesale_price - cogs_per_unit) / wholesale_price) × 100

TARGETS:
  Branded beverages: > 40%
  Co-pack / private label: > 25%
  DTC: > 50% (but higher marketing + fulfillment costs)
  FLAG if < 20% on any SKU

CONTRIBUTION MARGIN:
  contribution_margin = wholesale_price - cogs - freight_per_unit - trade_spend_per_unit
  → Must be positive for every SKU
  → Negative contribution margin = unprofitable even at full volume
  → FLAG any SKU with negative contribution margin

NET MARGIN (fully loaded):
  net_margin = contribution_margin - allocated_marketing - allocated_SG&A
  → Used for SKU rationalization decisions
```

### Margin Sensitivity Analysis

```
FOR EACH KEY INGREDIENT:
  impact_per_1pct_increase = ingredient_cost_per_unit × 0.01
  margin_impact = impact_per_1pct_increase / wholesale_price × 100

EXAMPLE (12oz juice at $1.50 wholesale):
  Orange concentrate = $0.35/unit
  1% price increase = $0.0035/unit
  Margin impact = 0.23 percentage points per 1% ingredient increase

  → A 20% spike in OJ concentrate costs reduces margin by 4.7 points
  → This is the kind of calculation the agent should run proactively
     when commodity prices change
```

## 10.4 Yield Loss Costing

```
YIELD LOSS COST:
  loss_units = theoretical_yield - actual_yield
  loss_cost = loss_units × cogs_per_unit

YIELD LOSS ALLOCATION:
  Category 1: Line waste (filler, CIP, start/stop) → production overhead
  Category 2: QC rejects (out-of-spec, damage) → quality cost
  Category 3: Ingredient loss (tank heels, transfer) → material cost
  Category 4: Rework (blend-back, reprocess) → partial recovery, net against loss

SCRAP RATE:
  scrap_rate = loss_units / theoretical_yield × 100
  TARGET: < 3%
  FLAG if > 5%
  → Scrap rate > 5% triggers root cause investigation

ANNUAL WASTE COST:
  annual_waste_cost = Σ (monthly_loss_units × cogs_per_unit)
  → Track by line, product, and loss category
  → Use for capital justification (e.g., new filler to reduce waste)
```

## 10.5 Landed Cost (for Imports)

```
LANDED COST:
  landed_cost_per_unit = purchase_price
    + international_freight / units_in_shipment
    + customs_duty (% of declared value)
    + customs_broker_fee / units_in_shipment
    + import_taxes
    + domestic_freight_to_warehouse / units_in_shipment
    + insurance
    + inspection_fees (FSVP, FDA prior notice) / units_in_shipment
```

### Typical Import Cost Adders

| Cost Component | Typical Range | Notes |
|---------------|--------------|-------|
| Ocean freight (40ft container) | $3,000–$8,000 | Varies by lane and season |
| Customs duty | 0–20% of declared value | Check HTS code for specific rate |
| Customs broker | $150–$400 per entry | Per customs entry, not per container |
| FSVP compliance | $500–$2,000/supplier/year | Foreign Supplier Verification Program |
| Cold storage at port | $50–$200/pallet/week | If waiting for clearance |
| Demurrage/detention | $150–$350/day | If container returned late to port |
| Fumigation (if required) | $500–$1,500/container | For certain agricultural products |
| Lab testing (import) | $200–$1,000/lot | If FDA or CBP requires testing |

```
LANDED COST COMPARISON:
  domestic_total_cost = domestic_price + domestic_freight
  import_total_cost = landed_cost (all components)

  → Import is justified only if:
    import_total_cost < domestic_total_cost × 0.90
    (10% buffer for risk, longer lead time, and working capital)
  → Also factor: supply chain risk, lead time variability, quality consistency
```

## 10.6 Freight Cost Allocation

```
FREIGHT ALLOCATION METHODS:

METHOD 1: PER CASE (simplest)
  freight_per_case = total_freight / total_cases_in_shipment

METHOD 2: PER WEIGHT (fairer for mixed loads)
  freight_per_case = total_freight × (case_weight / total_shipment_weight)

METHOD 3: PER CUBE (for cube-constrained shipments)
  freight_per_case = total_freight × (case_volume / total_shipment_volume)

→ Use per-weight for heavy products (glass bottles, gallon jugs)
→ Use per-cube for light/bulky products (snack bags, large PET bottles)
→ Use per-case as default when difference is negligible

TARGET: freight_per_case < 5% of wholesale case price
FLAG if > 8%
```

## 10.7 Trade Spend & Deductions

### Trade Spend Categories

| Category | Description | Typical Range |
|----------|-------------|--------------|
| Off-invoice | Discount at time of invoicing | 5–15% of gross |
| Billback | Retailer invoices after promo | Variable |
| Scan-based | Payment based on POS data | Variable |
| Slotting | One-time new item placement fee | $5,000–$50,000/SKU/chain |
| MDF / co-op | Marketing development funds | 2–5% of gross |
| Display allowance | Payment for display placement | $5–$15/case during promo |

```
TRADE SPEND AS % OF GROSS REVENUE:
  Industry average: 15–25%
  TARGET: < 20%
  FLAG if > 25% — margin erosion

TRADE SPEND ROI:
  trade_roi = incremental_gross_profit / trade_spend_investment
  TARGET: trade_roi > 1.0 (every $1 spent returns > $1 profit)
  FLAG if < 0.5 — promo destroying value
```

### Deduction Management

```
DEDUCTION VALIDATION:
  FOR EACH retailer deduction:
    1. Match to promo agreement (promo ID, dates, rates, eligible SKUs)
    2. IF no matching agreement: DISPUTE within 60 days
    3. IF agreement matches but amount differs > 5%: DISPUTE
    4. IF agreement matches and amount within 5%: APPROVE

AGING:
  0–30 days: normal processing
  31–60 days: follow up with retailer
  61–90 days: escalate internally
  > 90 days: escalate to sales VP, consider write-off

TARGET: dispute resolution < 45 days
TARGET: invalid deduction recovery rate > 60%
```

## 10.8 SKU Profitability Analysis

```
SKU RATIONALIZATION DECISION:
  FOR EACH SKU, calculate:
    1. Gross margin %
    2. Contribution margin $ (absolute)
    3. Annual volume (cases)
    4. Revenue rank (% of total revenue)
    5. Growth trend (YoY %)
    6. Complexity cost (unique ingredients, packaging, setup time)

  KEEP: gross_margin > target AND volume growing or stable
  REVIEW: gross_margin > target BUT volume declining
  IMPROVE: gross_margin < target BUT volume growing (reformulate or reprice)
  DISCONTINUE CANDIDATES:
    gross_margin < target AND volume declining AND revenue < 2% of total
    → Verify no strategic reason to keep (retailer relationship, portfolio fill)
    → Plan exit: sell through inventory, notify customers, sunset SKU
```

## 10.9 Failure Modes

| Failure | Detection | Action |
|---------|-----------|--------|
| COGS increase > 5% vs prior quarter | Quarterly cost analysis | Identify driver: ingredient, packaging, yield. Negotiate or reformulate |
| Gross margin < 20% on any SKU | Monthly P&L review | Price increase, cost reduction, or discontinue |
| Trade spend > 25% of gross revenue | Trade spend analysis | Review promo effectiveness, reduce unprofitable promos |
| Freight > 8% of case price | Freight cost analysis | Consolidate shipments, renegotiate carrier rates, review mode selection |
| Deductions unresolved > 90 days | Deduction aging report | Escalate, write off if unrecoverable, fix process to prevent recurrence |
| Yield loss cost > $X/month threshold | Monthly waste report | Root cause top 3 sources, invest in prevention |

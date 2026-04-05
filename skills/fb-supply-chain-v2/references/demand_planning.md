# Demand Planning — Deep Reference

## 7.1 Data Schema

| Field | Type | Unit | Typical Range |
|-------|------|------|---------------|
| `sku_id` | string | — | — |
| `customer_id` | string | — | — |
| `period` | date | month | — |
| `forecast_qty` | float | cases | — |
| `actual_qty` | float | cases | — |
| `forecast_error` | float | cases | forecast − actual |
| `promo_flag` | bool | — | Promotional period |
| `promo_lift_pct` | float | % | 20–300% |
| `seasonality_index` | float | — | 0.5–2.0 (1.0 = average) |

## 7.2 Forecast Accuracy Metrics

```
MAPE (Mean Absolute Percentage Error):
  MAPE = (1/n) × Σ |actual - forecast| / actual × 100
  TARGET: MAPE < 25% at SKU-month level
  GOOD:   MAPE < 20%
  FLAG if > 35%

  Limitation: MAPE is undefined when actual = 0. Exclude zero-demand
  periods or use WMAPE instead.

WMAPE (Weighted MAPE — better for SKU mix):
  WMAPE = Σ |actual - forecast| / Σ actual × 100
  → Weights accuracy by volume. High-volume SKUs dominate the metric.

BIAS:
  bias = Σ (forecast - actual) / Σ actual × 100
  TARGET: bias between -5% and +5%
  POSITIVE bias = over-forecasting → excess inventory risk
  NEGATIVE bias = under-forecasting → stockout risk
  FLAG if |bias| > 10%

TRACKING SIGNAL:
  tracking_signal = Σ (forecast - actual) / MAD
  where MAD = (1/n) × Σ |forecast - actual|
  FLAG if |tracking_signal| > 4 → systematic bias, model needs recalibration

FORECAST VALUE ADDED (FVA):
  FVA = naive_forecast_error - adjusted_forecast_error
  → If FVA < 0, the human/model adjustment made the forecast worse.
  → Measure FVA for each adjustment layer (statistical → demand planner → sales input)
```

## 7.3 Promotional Lift Modeling

```
PROMO LIFT CALCULATION:
  baseline_qty = avg non-promo qty for same period (last 12 months, exclude promos)
  promo_qty = actual qty during promo
  lift_pct = ((promo_qty - baseline_qty) / baseline_qty) × 100
```

### Typical Lift Ranges by Promo Type

| Promo Mechanism | Typical Lift | Notes |
|----------------|-------------|-------|
| TPR (temporary price reduction) | 20–60% | Most common, moderate lift |
| BOGO / multi-buy | 40–100% | High lift but high cost |
| Display + TPR | 80–200% | Display is the multiplier |
| Feature (flyer/ad) + display + TPR | 150–300% | Maximum lift, rare |
| Sampling / demo | 30–80% | Short-term, brand-building |
| Coupon (digital/paper) | 10–30% | Lower redemption rates |

### Promo Planning Rules

```
POST-PROMO DIP:
  Expect 10–30% volume decline in 2–4 weeks post-promo
  Factor dip into demand plan to avoid overproduction

CANNIBALIZATION:
  If promoting SKU A, expect 5–15% decline in related SKUs (B, C)
  Must net out cannibalization to get true incremental lift

FORWARD BUY (retailer):
  Retailers may buy 4–8 weeks of supply during promo at deal price
  This creates a demand spike during promo + demand trough post-promo
  Scan-based promotions reduce forward buying (pay for what sells)

PROMO FORECAST OVERRIDE:
  IF promo_flag == true:
    forecast_qty = baseline_qty × (1 + estimated_lift_pct / 100)
    → Use historical lift for same promo type/retailer if available
    → For new promo types, use category average lift
```

## 7.4 S&OP Cadence

```
MONTHLY S&OP CYCLE:

  Week 1: DEMAND REVIEW
    - Statistical forecast updated with latest actuals
    - Market intelligence: new distribution, lost accounts, competitor activity
    - Promo calendar updated
    - Output: unconstrained demand plan (what we would sell if no constraints)

  Week 2: SUPPLY REVIEW
    - Capacity assessment: can we make what demand wants?
    - Material availability: are ingredients available?
    - Identify constraints and gaps
    - Output: constrained supply plan + gap list

  Week 3: PRE-S&OP
    - Reconcile demand vs supply gaps
    - Propose scenarios: add shifts, outsource, prioritize SKUs, adjust promos
    - Financial impact of each scenario
    - Output: recommended plan with trade-offs documented

  Week 4: EXECUTIVE S&OP
    - Decisions on production plan, inventory targets, capital requests
    - Approve consensus plan
    - Output: authorized operating plan for next 1–3 months

KEY OUTPUTS:
  Consensus demand plan (units by SKU by month, 3–18 month horizon)
  Production plan (aligned to demand, constrained by capacity)
  Inventory projection:
    projected_inventory = on_hand + on_order + planned_production - forecast_demand
  Financial reconciliation (revenue plan vs operational plan)
```

## 7.5 Seasonality

### Beverage Seasonality (Northern Hemisphere)

| Season | Months | Index Range | Notes |
|--------|--------|-------------|-------|
| Peak | May–Sep | 1.3–1.8 | Summer, highest volume |
| Trough | Nov–Feb | 0.6–0.8 | Winter, lowest volume |
| Shoulder | Mar–Apr, Oct | 0.9–1.1 | Transition periods |

### Category-Specific Seasonality

| Category | Seasonal Pattern | Index Swing |
|----------|-----------------|-------------|
| Juice | High seasonality, summer peak | ±40% |
| Kombucha | Less seasonal, health-driven | ±15% |
| Functional/energy | Moderate seasonality | ±20% |
| Oat milk | Inverted — peaks fall/winter (coffee season) | +20% in Oct–Feb |
| Cold brew coffee | Summer peak, moderate winter (hot coffee substitution) | ±30% |
| Sparkling water | Strong summer peak | ±50% |

### Seasonal Ingredient Availability

| Ingredient | Availability Window | Planning Action |
|-----------|-------------------|-----------------|
| Orange juice concentrate | Florida Oct–Jun, Brazil year-round | Contract during FL season |
| Berry concentrates | Pacific NW Jul–Sep, frozen year-round | Buy annual need at harvest |
| Apple juice concentrate | Sep–Nov harvest, stored year-round | Contract at harvest |
| Mango puree | Apr–Jul (India), year-round (Mexico) | Secure frozen or aseptic early |
| Cranberry concentrate | Sep–Nov | Annual contract at harvest |

```
SEASONALITY INDEX CALCULATION:
  For each month m:
    seasonality_index_m = avg_demand_month_m / avg_demand_all_months

  Apply to baseline forecast:
    seasonal_forecast_m = annual_forecast / 12 × seasonality_index_m
```

## 7.6 New Product Forecasting

```
NEW PRODUCT FORECAST (no history):
  Method 1: ANALOGUE — use sales history of most similar existing SKU
    adjusted for: distribution breadth, price point, category growth rate
  Method 2: BUILD-UP — estimate by account:
    Σ (stores_per_account × velocity_per_store_per_week × weeks)
  Method 3: TOP-DOWN — category size × expected market share

  All three methods should be triangulated.
  Bias toward conservative (Method 3 tends to be optimistic).

NEW PRODUCT VELOCITY BENCHMARKS (US grocery):
  Successful launch: 1–3 units/store/week in first 12 weeks
  Strong performer: 3–5 units/store/week
  Category leader: 5+ units/store/week
  → Below 1 unit/store/week at week 12: risk of discontinuation
```

## 7.7 Failure Modes

| Failure | Detection | Action |
|---------|-----------|--------|
| MAPE > 35% for 3+ months | Forecast accuracy tracking | Recalibrate model, review demand signals, check data quality |
| Bias > +10% (chronic over-forecast) | Bias metric | Reduce forecast, investigate source of optimism (sales input?) |
| Bias < -10% (chronic under-forecast) | Bias metric | Increase forecast, check for untracked demand (new accounts, e-comm) |
| Promo lift misestimated by >50% | Post-promo analysis | Update lift assumptions for this promo type/retailer |
| Seasonal pattern shifted | Year-over-year comparison | Adjust seasonality indices, check for structural demand change |
| New product below velocity threshold | Week 8–12 scan data | Evaluate: increase marketing, adjust price, or plan exit |

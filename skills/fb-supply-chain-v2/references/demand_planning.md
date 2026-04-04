# Demand Planning & Forecasting — F&B Beverage Manufacturing

## Overview

Demand planning in food and beverage is uniquely challenging because of perishability constraints, promotional volatility, seasonal consumption patterns, and the rapid pace of new product introductions. Unlike durable goods where excess inventory sits indefinitely, a forecast miss in fresh beverages means either out-of-stocks (lost sales, retailer penalties) or product dumped at end of shelf life (margin destruction). Effective demand planning is the backbone of profitable beverage operations.

---

## 1. Seasonal Patterns in Beverage Consumption

### Category-Level Seasonality

| Category | Peak Season | Index vs Annual Average | Trough Season | Index vs Average |
|---|---|---|---|---|
| Juice (refrigerated) | June-August | 115-130 | January-February | 75-85 |
| Juice (shelf-stable) | June-August | 110-120 | January-February | 85-90 |
| Kombucha | May-September | 120-140 | November-February | 65-80 |
| Cold-brew coffee | May-August | 130-150 | December-February | 60-75 |
| Hot-fill tea (RTD) | June-August | 125-145 | December-February | 70-80 |
| Functional water/electrolyte | June-September | 140-170 | November-February | 55-70 |
| Oat/nut milk | Relatively flat | 95-105 year-round | Slight summer dip | 90-95 |
| Holiday specialty (eggnog, cider) | October-December | 300-500 (3-5 month window) | N/A | Zero outside window |

**Planning implication**: Production scheduling must ramp 4-8 weeks ahead of consumption peak. Co-manufacturer capacity is tightest in March-May (everyone building for summer simultaneously). Book summer production capacity by Q4 of the prior year.

### Weather Sensitivity

Beverage consumption is highly correlated with temperature. A heat wave can spike demand 20-40% above forecast within a week. A cool, rainy summer can depress seasonal categories 10-20% below plan. Incorporate weather forecasts (10-day outlook) into near-term demand sensing.

---

## 2. New Product Launch Forecasting

Forecasting new products with no sales history is inherently uncertain. Standard methodologies:

### Analogous Product Method

1. Identify 2-3 existing products with similar attributes (category, price point, channel, target consumer)
2. Pull first-year velocity curves from those analogues
3. Adjust for: distribution build differences, marketing spend differences, competitive landscape, price positioning
4. Apply a confidence range: optimistic (120% of analogue), base (100%), conservative (70%)

| Factor | Upward Adjustment | Downward Adjustment |
|---|---|---|
| Stronger marketing spend vs analogue | +10-20% | |
| More competitive category today | | -10-20% |
| Higher price point vs analogue | | -5-15% |
| Trending ingredient/category | +10-30% | |
| Weaker brand awareness | | -15-25% |
| Better channel fit | +5-15% | |

### Test Market Extrapolation

1. Launch in 200-500 stores in representative markets (e.g., Northern California natural channel as proxy for national natural)
2. Track 12-16 weeks of POS sell-through data
3. Calculate weekly velocity per point of distribution (units/store/week)
4. Apply distribution build curve for national rollout
5. Adjust for regional consumption differences (e.g., NorCal natural over-indexes for kombucha vs national average)

### Distribution Build Curve (Typical for New SKU at Major Retailer)

| Week | % of Total Authorized Stores Stocking | Cumulative ACV Equivalent |
|---|---|---|
| Week 1-2 | 20-30% | Early-ship DCs fulfill first orders |
| Week 3-6 | 50-70% | DC-to-store distribution builds |
| Week 7-10 | 80-90% | Laggard stores fill in; off-shelf placement stabilizes |
| Week 11-16 | 90-95% | Full distribution; includes re-orders |
| Steady state (Week 16+) | 85-95% | Normal voids begin (OOS, discontinued in underperforming stores) |

---

## 3. Promotion Lift Modeling

### Promotion Types and Expected Lifts

| Promotion Type | Abbreviation | Typical Lift (vs baseline) | Duration | Funding |
|---|---|---|---|---|
| Temporary Price Reduction | TPR | 2-3x | 1-2 weeks | Trade spend; off-invoice or scan-back |
| Buy One Get One | BOGO | 3-5x | 1-2 weeks | Trade spend; brand-funded |
| In-store display (feature + display) | F&D | 3-6x | 1-2 weeks | Display allowance + feature ad fee |
| Digital coupon | DCpn | 1.5-2x | 2-4 weeks | Coupon face value + retailer platform fee |
| Shipper display (floor stand) | SHP | 2-4x | 2-4 weeks | Brand-funded shipper + fill; retailer placement fee |
| End cap placement | EC | 2-4x (category dependent) | 2-4 weeks | Premium placement fee |
| Sampling / demo | Demo | 1.3-2x (trailing lift) | Weekend | Demo agency fee + product cost |

### Promotion Forecasting Process

1. **Event calendar**: Build a 52-week promotional calendar by retailer, by SKU. Input from sales team on confirmed and tentative events.
2. **Baseline forecast**: Statistical forecast of what would sell with zero promotional activity. Methods: exponential smoothing, ARIMA, or regression with trend and seasonality.
3. **Lift application**: Overlay promotional lifts onto baseline. Use historical lift data from the same retailer-SKU-promo type when available. If no history, use the category averages above.
4. **Cannibalization adjustment**: Promotional volume may cannibalize baseline weeks before/after the event (pantry loading effect, particularly for shelf-stable). Deduct 10-20% from adjacent baseline weeks.
5. **Halo effect**: Promoted SKU may lift other SKUs in the brand portfolio by 5-15%. Capture this in the portfolio-level forecast.

### Trade Spend ROI Analysis

| Metric | Calculation | Target |
|---|---|---|
| Incremental volume | Promo volume - baseline volume during promo period | Positive; breakeven at minimum |
| Cost per incremental case | Total trade spend / incremental cases | <$5-8/case for emerging brands |
| Incremental revenue | Incremental volume x net price per case | Must exceed trade spend + COGS |
| Post-promotion dip | Baseline drop in 2 weeks following promo vs normal baseline | <15% dip acceptable |
| Retailer ROI | (Incremental gross margin for retailer) / (retailer's promotional cost) | Retailer expects >1.0x |

---

## 4. Retailer POS Data Integration

### Syndicated Data Sources

| Provider | Coverage | Granularity | Cost | Best For |
|---|---|---|---|---|
| Circana (formerly IRI) | 95%+ of US grocery, mass, drug, convenience | Weekly; UPC x market x channel | $50K-500K/year depending on categories | Category trends, competitive share, market sizing |
| NielsenIQ | 90%+ of US measured channels | Weekly; UPC x market x channel | $50K-500K/year | Same as above; some retailers prefer NIQ |
| SPINS | Natural/specialty channel dominant | Weekly; UPC x retailer-group | $15K-80K/year | Natural channel brands; organic/non-GMO analytics |

### Retailer Portal Data

| Retailer | Portal/Platform | Data Available | Latency |
|---|---|---|---|
| Walmart | Retail Link / Luminate | Store-level POS, inventory, on-hand, forecast | 1-2 days |
| Kroger | 84.51° / KPM (Kroger Precision Marketing) | Store-level POS, shopper loyalty data | 1-3 days |
| Target | Partners Online (POL) | DC-level inventory, POS by store cluster | 1-2 days |
| Whole Foods / Amazon | Vendor Central | POS, inventory, forecasting, replenishment | 1-2 days |
| Costco | Retail portal | Warehouse-level POS | 3-5 days |
| Albertsons/Safeway | Vendor portal | DC and store POS | 2-4 days |
| Sprouts | Vendor portal | Store-level POS | 3-5 days |

**Data integration best practice**: Automate weekly POS data pulls into a central demand planning system. Compare POS sell-through to shipments (sell-in) to detect inventory pipeline fills vs true consumption. A large sell-in without corresponding sell-through indicates retail pipeline fill — not consumer demand.

---

## 5. Safety Stock for Perishable Goods

### Standard Safety Stock Formula (Modified for Shelf Life)

Base safety stock: `SS = Z x sigma_d x sqrt(LT + RP)`

Where:
- Z = service level factor (1.65 for 95%, 1.96 for 97.5%, 2.33 for 99%)
- sigma_d = standard deviation of daily demand
- LT = replenishment lead time (days)
- RP = review period (days)

**Perishable modification**: Safety stock cannot exceed `(Remaining shelf life at delivery - Retailer minimum code date requirement) x Average daily demand`. Otherwise, safety stock itself becomes waste.

### Practical Safety Stock Targets by Product Type

| Product Type | Target Days of Cover (SS) | Max Days of Cover (total inv) | Rationale |
|---|---|---|---|
| Fresh juice (45-day shelf) | 5-7 days | 14-18 days | Tight shelf life; code date pressure |
| Kombucha (90-day shelf) | 7-10 days | 21-30 days | Moderate shelf life; live culture sensitive |
| Shelf-stable beverage (12-mo) | 14-21 days | 45-60 days | Long shelf life allows more buffer |
| Frozen concentrate (18-mo) | 21-30 days | 60-90 days | Long shelf life; seasonal procurement |

### Dynamic Safety Stock Triggers

- **Increase SS** when: entering peak season, launching promotional events, supplier reliability declining, new product launch period, severe weather threatening supply
- **Decrease SS** when: entering off-season, supplier performance stable, approaching seasonal product EOL, excess inventory building

---

## 6. ABC/XYZ Inventory Classification

### ABC Classification (by revenue or volume contribution)

| Class | % of SKUs | % of Revenue | Planning Treatment |
|---|---|---|---|
| A | 10-20% | 70-80% | Weekly forecast review; high service level (98%+); priority allocation |
| B | 20-30% | 15-20% | Bi-weekly review; standard service level (95%); normal allocation |
| C | 50-70% | 5-10% | Monthly review; lower service level (90%); candidate for rationalization |

### XYZ Classification (by demand variability)

| Class | Coefficient of Variation (CV) | Demand Pattern | Planning Method |
|---|---|---|---|
| X | CV < 0.5 | Stable, predictable | Statistical forecast reliable; lean safety stock |
| Y | 0.5 < CV < 1.0 | Variable, some pattern | Statistical forecast + judgment; moderate safety stock |
| Z | CV > 1.0 | Erratic, lumpy | Difficult to forecast; make-to-order or high safety stock with risk acceptance |

### Combined Matrix (Strategic Action)

| | X (Stable) | Y (Variable) | Z (Erratic) |
|---|---|---|---|
| **A (High value)** | Lean flow; automated replenishment | Active management; frequent forecast updates | Executive attention; demand sensing; flexible supply |
| **B (Medium value)** | Standard planning | Standard planning with promotional overlays | Review for simplification or discontinuation |
| **C (Low value)** | Automate; minimal attention | Consider discontinuation | Discontinue or make-to-order only |

---

## 7. Production Scheduling Integration (MPS)

### Forecast-to-Production Flow

```
Demand Forecast (SKU-week)
    |
    v
Finished Goods Netting (forecast - on-hand - in-transit - scheduled production)
    |
    v
Master Production Schedule (MPS) — what to produce, when, how much
    |
    v
Material Requirements Planning (MRP) — ingredient and packaging needs by date
    |
    v
Purchase Orders / Releases to Suppliers
    |
    v
Co-Manufacturer Scheduling — booking production windows
```

### Co-Manufacturer Constraints

| Constraint | Typical Range | Planning Impact |
|---|---|---|
| Minimum run size | 500-2,000 cases (varies by line speed and format) | Cannot produce less; excess goes to inventory |
| Scheduling lead time | 4-8 weeks for planned runs; 8-12 weeks for peak season | Forecast frozen period must cover this window |
| Changeover time | 2-8 hours (flavor/format dependent) | Batching similar flavors reduces lost production time |
| Line allocation | Shared line with other brands | Availability limited; may only get 1-2 windows per month |
| Ingredient lead time | 2-6 weeks for domestic; 8-20 weeks for import | Longest-lead ingredient sets planning horizon |
| Packaging lead time | 4-12 weeks for printed materials | Must release PO well ahead of production date |

### Production Scheduling Rules of Thumb

1. **Flavor sequencing**: Light to dark, mild to strong — reduces changeover time and cross-contamination risk (e.g., run lemon before grapefruit before berry)
2. **Allergen sequencing**: Non-allergen products first; allergen-containing products last; full CIP/sanitation between allergen transitions
3. **Minimum campaign length**: Target 1 full shift (8-10 hours) per SKU to maximize line efficiency (OEE)
4. **Co-man communication**: Provide 8-week rolling production forecast; firm 4 weeks out; adjustable 5-8 weeks out

---

## 8. S&OP Process for Emerging Brands

### Monthly S&OP Cadence

| Week | Meeting | Participants | Outputs |
|---|---|---|---|
| Week 1 | **Demand Review** | Sales, marketing, demand planner | Updated demand forecast by SKU-month; promotional calendar; new item forecasts |
| Week 2 | **Supply Review** | Supply chain, procurement, co-man liaison | Production plan; material availability gaps; capacity constraints; alternate sourcing |
| Week 3 | **Pre-S&OP / Financial Reconciliation** | Finance, demand planner, supply chain lead | Demand-supply gap resolution proposals; financial impact of scenarios; inventory projections |
| Week 4 | **Executive S&OP** | CEO/GM, VP Sales, VP Ops, VP Finance | Decisions on gaps; resource allocation; risk acceptance; approved plan of record |

### S&OP at Different Company Stages

| Revenue Stage | S&OP Maturity | Tools | Key Focus |
|---|---|---|---|
| $1-5M | Informal; spreadsheet-based | Excel, Google Sheets | Cash management; avoid stockouts on hero SKUs |
| $5-20M | Structured monthly cadence | Excel + light planning software (Inventory Planner, Flieber) | Demand-supply alignment; co-man booking; working capital |
| $20-50M | Formal S&OP with cross-functional ownership | Planning software (Anaplan, Logility, NetSuite Demand Planning) | SKU rationalization; trade spend ROI; service level by customer |
| $50-200M | Integrated Business Planning (IBP) | Enterprise planning (Kinaxis, o9, SAP IBP) | Portfolio management; scenario planning; integrated financial planning |

### Common S&OP Failures in Emerging Brands

1. **Sales team overrides forecast with "gut feel"**: Leads to bullwhip effect. Require data-based justification for large forecast adjustments.
2. **No frozen period**: Changing production plan inside 2-week window wastes ingredients and co-man capacity.
3. **Ignoring cannibalization**: Launching a new flavor without reducing forecast for existing flavors overstates total demand.
4. **Promotional volume treated as baseline**: One-time BOGO inflates baseline forecast for future periods. Strip promotional lift before baseline calculation.
5. **No SKU sunset process**: Tail SKUs accumulate inventory and eat working capital. Quarterly SKU rationalization review should be part of S&OP.

---

## 9. Forecast Accuracy Metrics

### Primary Metrics

| Metric | Formula | Target (SKU-Month) | Interpretation |
|---|---|---|---|
| **MAPE** | Mean of abs(actual - forecast) / actual x 100 | <25% for A items; <35% for B; <50% for C | Lower is better; does not detect bias |
| **Bias** | Sum(forecast - actual) / sum(actual) x 100 | -5% to +5% | Positive = over-forecasting; negative = under-forecasting |
| **Tracking signal** | Running sum of forecast errors / MAD | -6 to +6 | Outside range indicates systematic bias; action required |
| **Weighted MAPE** | MAPE weighted by volume or revenue | <20% at total portfolio level | Better reflection of business impact vs simple MAPE |
| **Forecast Value Added (FVA)** | Compare each step's accuracy vs naive forecast | Positive FVA | If a forecast step does not improve accuracy, eliminate it |

### Measurement Cadence

| Level | Frequency | Granularity | Audience |
|---|---|---|---|
| SKU-week | Weekly | By SKU, by ship-to location | Demand planner (operational) |
| SKU-month | Monthly | By SKU, by channel | S&OP team (tactical) |
| Category-quarter | Quarterly | By product line, by customer tier | Executive team (strategic) |

---

## 10. Managing Promotional vs Baseline Demand

### Demand Decomposition

Total demand = Baseline demand + Incremental promotional demand + New distribution pipeline + Seasonality index

**Baseline isolation**: Use 52-week history, exclude weeks with promotional activity (flagged via trade spend records or POS causal data), apply exponential smoothing or regression to non-promoted weeks only.

**Promotional overlay**: Layer confirmed promotional events onto baseline. Each event has: start date, end date, promotion type, expected lift multiplier, and store count.

**Pipeline fills**: New distribution authorizations create a one-time pipeline fill (typically 2-4 weeks of expected sell-through). This is not recurring demand — capture it as a one-time planning event.

---

## 11. Co-Manufacturer Capacity Booking

### Capacity Booking Timeline

| Horizon | Action | Commitment Level |
|---|---|---|
| 12 months out | Annual volume commitment discussion; rough capacity reservation | Indicative; non-binding |
| 6 months out | Confirm quarterly production windows; lock key material orders | Soft commitment; cancellation fees may apply |
| 8 weeks out | Submit firm production schedule (flavors, quantities, dates) | Firm; changes incur fees |
| 4 weeks out | Final material and packaging confirmation; no changes to schedule | Frozen; no changes without penalty |
| 2 weeks out | Pre-production ingredient and packaging delivery | Operational; deviations risk missed run |
| Run day | Production execution; QA inline and end-of-line | Brand QA should be on-site for new products |

### Co-Man Capacity Considerations

- **Shared lines**: Your brand competes for line time with other brands. During peak season (March-August for beverages), booking priority goes to largest-volume brands.
- **Line speed by format**: Hot-fill PET may run 200-400 BPM; aseptic Tetra Pak 100-200 units/min; HPP post-fill processing adds 24-48 hours to cycle.
- **Minimum efficient run**: Below minimum run size, the cost per case increases sharply due to fixed changeover and sanitation costs. For hot-fill: typically 500-1,000 cases minimum. For aseptic: 1,000-2,000 cases.
- **Scheduling flexibility**: Some co-mans offer "flex windows" — unscheduled capacity you can fill on 2-week notice — at a premium rate. Useful for unexpected demand.

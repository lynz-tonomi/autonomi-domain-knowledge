# Procurement — Deep Reference

## 5.1 Data Schema

| Field | Type | Unit | Typical Range |
|-------|------|------|---------------|
| `po_number` | string | — | PO-YYYYMMDD-SEQ |
| `supplier_id` | string | — | — |
| `item_id` | string | — | — |
| `order_qty` | float | lbs/units | Including overage |
| `unit_price` | float | $/lb or $/unit | — |
| `lead_time_days` | int | days | 3–90 depending on item |
| `moq` | float | lbs/units | Minimum order quantity |
| `order_multiple` | float | lbs/units | Must order in multiples of |
| `delivery_date_requested` | date | — | — |
| `delivery_date_confirmed` | date | — | — |
| `incoterms` | string | — | FOB, CIF, DDP, EXW |
| `payment_terms` | string | — | Net 30, Net 45, 2/10 Net 30 |
| `coa_required` | bool | — | Always true for ingredients |
| `coa_received` | bool | — | Must be true before lot release |

## 5.2 PO Generation Logic

```
PO GENERATION TRIGGER:
  IF days_of_supply < lead_time_days + safety_stock_days:

    order_qty = MAX(
      (avg_daily_usage × order_cover_days) − quantity_available,
      moq
    )
    → Round UP to nearest order_multiple
    → Apply overage factor (see BOM reference)
    → Check supplier price breaks (volume discounts)

ORDER COVER DAYS:
  Standard: lead_time_days + safety_stock_days + review_period_days
  Seasonal items: extend to cover expected unavailability window
  Promotional periods: add promotional lift volume

SPLIT ORDER RULES:
  IF order_qty > single_truck_capacity (typically 42,000 lbs):
    Split into multiple deliveries
    Stagger by 1–2 weeks to manage warehouse space
  IF supplier has capacity constraints:
    Split across approved alternate suppliers (maintain dual-source ratio)
```

### Payment Terms Reference

| Terms | Meaning | Cash Flow Impact |
|-------|---------|-----------------|
| Net 30 | Pay within 30 days of invoice | Standard |
| Net 45 | Pay within 45 days | Better cash flow |
| Net 60 | Pay within 60 days | Best cash flow, may limit supplier pool |
| 2/10 Net 30 | 2% discount if paid within 10 days, else Net 30 | 2% discount = 36.7% annualized return — almost always take it |
| COD | Cash on delivery | Worst cash flow, used for new/small suppliers |
| Prepaid | Pay before shipment | Required for some imports |

## 5.3 Lead Time Reference

| Category | Domestic Lead Time | Import Lead Time | Notes |
|----------|-------------------|-----------------|-------|
| Juice concentrates | 7–14 days | 30–60 days (ocean) | Brazil/Mexico origin common |
| Organic sweeteners | 10–21 days | 45–90 days | Limited organic supply chain |
| Natural flavors | 14–28 days | — | Custom blends take longer |
| Vitamins / minerals | 7–14 days | 30–60 days | China origin, verify COAs carefully |
| PET bottles | 7–14 days | — | Domestic blow-mold usually |
| Caps / closures | 7–21 days | 30–45 days | Custom colors take longer |
| Labels | 10–21 days | — | Print plate setup for new SKUs: add 5–10 days |
| Corrugated cases | 7–14 days | — | — |
| Shrink film | 7–14 days | — | — |
| Oat base / oat flour | 7–21 days | 30–45 days | Gluten-free certified oats have longer lead times |
| Coffee (green) | 14–30 days | 45–90 days | Seasonal harvest, single-origin longer |
| SCOBY / kombucha cultures | 7–14 days | — | Domestic only, maintain backup culture |

### Seasonal Procurement Considerations

| Ingredient | Harvest Window | Price Behavior | Planning Action |
|-----------|---------------|----------------|-----------------|
| Orange juice | FL: Oct–Jun, Brazil: year-round | Peaks after freeze events | Forward contract 60–80% of annual need |
| Berry concentrates | Pacific NW: Jul–Sep | Lowest at harvest, +20–40% off-season | Buy annual need during harvest for frozen storage |
| Apple juice concentrate | Sep–Nov | Lowest at harvest | Contract during harvest |
| Vanilla | Mar–Jul (curing adds months) | Extremely volatile ($200–$600/kg range) | Lock price via forward contract |
| Coconut water/cream | Year-round (tropical) | Moderate fluctuation | 3-month rolling contracts |

## 5.4 Supplier Qualification Requirements

```
NEW SUPPLIER CHECKLIST:
  [ ] GFSI-certified (SQF, BRC, FSSC 22000, or equivalent)
  [ ] OR: successful on-site audit (if no GFSI cert — document scope and findings)
  [ ] Allergen management program documented
  [ ] Product specifications agreed and signed
  [ ] COA template reviewed — must include:
        lot, manufacture date, expiry date, micro results,
        allergen statement, all spec parameters
  [ ] Food defense / FSVP documentation (for imports)
  [ ] Certificate of insurance on file
  [ ] W-9 / tax documentation
  [ ] Payment terms agreed
  [ ] Quality agreement signed:
        response time for complaints, recall protocols,
        notification of formulation/facility changes
  [ ] Approved for relevant certifications:
        organic (NOP cert), kosher (certificate), non-GMO (if claimed)

ONGOING MONITORING:
  Supplier scorecard: quarterly review
  GFSI cert renewal: verify annually
  COA trending: flag if any spec parameter drifts toward limit
  Corrective actions: track open CARs and resolution time
```

### Supplier Scorecard Dimensions

| Dimension | Weight | Metrics |
|-----------|--------|---------|
| Quality | 30–40% | Lot acceptance rate, COA accuracy, audit score, incident count |
| Delivery | 25–30% | On-time rate, lead time consistency (std dev), fill rate, ASN accuracy |
| Cost | 20–25% | Price competitiveness, PPV, total cost of ownership |
| Responsiveness | 10–15% | Communication speed, rush order flexibility, issue resolution time |

```
SCORECARD CLASSIFICATION:
  Strategic:    >85 composite score
  Preferred:    70–85
  Approved:     55–70
  Probationary: <55 — improvement plan required, dual-source immediately
```

## 5.5 COA Requirements

```
COA REVIEW DECISION:

IF coa_received == false AND item_type == 'raw_material':
  HOLD LOT — do not release for production
  Notify procurement to request from supplier
  IF COA not received within 48 hrs: ESCALATE

IF coa_received == true:
  VERIFY all spec parameters within range
  IF any parameter out of spec:
    HOLD LOT — notify quality alert
    Initiate supplier NCR (non-conformance report)
    Assess: reject lot, return to supplier, or use-as-is with deviation approval
  IF all parameters pass:
    RELEASE LOT for production allocation

SKIP LOT PROGRAM (reduced inspection):
  IF supplier has: GFSI cert + 10 consecutive lots pass + scorecard > 90:
    Inspect 1 in 3 lots (visual + COA only, no lab testing)
    Revert to full inspection after any failure
```

### COA Required Parameters by Ingredient Type

| Ingredient Type | Required COA Parameters |
|----------------|----------------------|
| Juice concentrate | Brix, pH, TA, color, micro (APC, Y&M, coliforms), allergens, pesticide statement |
| Sweeteners | Purity/assay, moisture, color, micro, heavy metals (if organic) |
| Flavors | Specific gravity, refractive index, flash point, allergen statement |
| Vitamins | Assay/potency, moisture, heavy metals, micro |
| Oat base | Moisture, protein, fat, gluten (<20 ppm if GF claim), micro |
| Packaging | Dimensional specs, FDA compliance statement (21 CFR 174-186), functional test results |

## 5.6 Failure Modes

| Failure | Detection | Action |
|---------|-----------|--------|
| Supplier late delivery | `delivery_date_actual > delivery_date_confirmed` | Assess production impact, expedite or source from alternate |
| COA parameter out of spec | COA review flags deviation | Hold lot, NCR, evaluate reject/use-as-is |
| Price increase > 5% without notice | PO price vs contract price | Dispute, review contract terms, evaluate alternates |
| Supplier loses GFSI cert | Annual verification check | Elevate to probationary, schedule audit or find alternate |
| MOQ exceeds consumption before expiry | `moq / daily_usage > shelf_life_days` | Negotiate lower MOQ, find alternate supplier, or consortium buy |
| Single-source ingredient at risk | Only 1 approved supplier for critical item | Qualify second source immediately |

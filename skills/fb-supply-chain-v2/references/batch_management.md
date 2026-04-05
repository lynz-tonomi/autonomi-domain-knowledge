# Batch Management — Deep Reference

## 2.1 Data Schema

| Field | Type | Unit | Typical Range |
|-------|------|------|---------------|
| `batch_id` | string | — | YYMMDD-LINE-SEQ |
| `batch_size_gal` | float | gallons | 500–50,000 |
| `actual_yield_gal` | float | gallons | — |
| `yield_pct` | float | % | 92–99% (target >96%) |
| `batch_status` | enum | — | mixing, processing, filling, hold, released, rejected |
| `brix` | float | °Brix | 4–65 depending on product |
| `ph` | float | — | 2.5–7.0 |
| `titratable_acidity` | float | % | 0.1–2.0 |
| `temperature_f` | float | °F | 33–275 depending on process |
| `fill_weight_oz` | float | oz | ±1% of target |
| `headspace_in` | float | inches | 0.125–0.375 |
| `dissolved_o2_ppb` | float | ppb | <50 for juice, <100 for water |
| `co2_volumes` | float | volumes | 2.5–4.0 for carbonated |
| `lot_codes` | array | — | All ingredient lots consumed |

## 2.2 Yield Calculations

```
BATCH YIELD (units):
  batch_yield_units = (batch_size_gal × 128) / fill_size_oz

BATCH YIELD (weight):
  batch_yield_lbs = batch_size_gal × density_lb_per_gal

YIELD PERCENTAGE:
  yield_pct = (actual_output_units / theoretical_yield_units) × 100

INGREDIENT USAGE:
  lbs_per_batch = batch_size_gal × density_lb_per_gal × formula_pct
  lbs_per_unit  = (formula_pct × density_lb_per_gal × fill_size_oz) / 128
  unit_cost     = price_per_lb × lbs_per_unit
  run_cost      = lbs_per_batch × price_per_lb
```

### Yield Thresholds by Product Type

| Product Type | Expected Yield | Flag Below | Investigate Below |
|-------------|---------------|------------|-------------------|
| Juice (hot-fill) | 96–98% | 94% | 90% |
| Kombucha | 94–97% | 92% | 88% |
| Oat milk | 95–98% | 93% | 89% |
| Carbonated | 93–96% | 91% | 87% |
| Cold brew (extraction) | 60–75% | 55% | 50% |

### Yield Loss Categories

- **Line loss** (filler waste, start/stop purges): 1–3%
- **QC samples and lab retention**: 0.2–0.5%
- **Out-of-spec product** (underfill, overfill, cap defects): 0.5–2%
- **Tank heels and transfer losses**: 0.5–1.5%
- **Rework input** (blending back off-spec product): reduces apparent loss

## 2.3 Rework / Reprocess Rules

```
REWORK DECISION TREE:

IF batch_status == 'hold' AND deviation_type == 'out_of_spec':

  IF parameter == 'brix':
    IF actual_brix > target_brix:
      ACTION: DILUTE (add water, recalculate formula)
    IF actual_brix < target_brix:
      ACTION: CONCENTRATE (add concentrate, recalculate)
    → Retest after adjustment. Max 2 rework attempts before reject.

  IF parameter == 'ph':
    IF actual_ph > target_ph:
      ACTION: ADD ACID (citric or malic, recalculate)
    IF actual_ph < target_ph:
      ACTION: DILUTE or BLEND with higher-pH batch
    → CRITICAL: If pH adjustment moves product from acidified to
      low-acid (pH > 4.6): STOP. Requires process authority review.
      Cannot proceed without filed scheduled process for low-acid.

  IF parameter == 'fill_weight':
    Rework not possible on filled product. Segregate and repack or destroy.

  IF parameter == 'micro' (positive pathogen or APC > spec):
    NO REWORK ALLOWED. Reject batch. Initiate CAPA.

  IF parameter == 'co2_volumes':
    IF actual_volumes < target:
      ACTION: Re-carbonate in tank (if product not yet filled)
    IF actual_volumes > target:
      ACTION: Degas by agitation or transfer (difficult — usually accept if within ±0.3)

  IF parameter == 'dissolved_o2':
    IF DO2 > spec:
      ACTION: Nitrogen sparge to strip oxygen (must be done before filling)
    → If already filled, product shelf life is compromised. Evaluate for short-code release.
```

### Rework Limits

- Maximum rework blend-back: 10% of next batch volume unless quality approves higher.
- Reworked product must be retested against full finished product spec before release.
- All rework events are logged with traceability to both source and destination batch IDs.
- Reworked product carries the lot codes of BOTH the original and destination batches.

## 2.4 Batch Release Criteria

```
RELEASE CHECKLIST (all must pass):
  [ ] Brix within ±0.3 of target
  [ ] pH within ±0.1 of target (and ≤4.6 for acidified products)
  [ ] Fill weight within ±1% of declared
  [ ] Headspace within spec (critical for retort — affects thermal process)
  [ ] Cap torque within range:
        8–18 in-lbs for 38mm closure
        12–24 in-lbs for 43mm closure
        Custom ranges for other formats — check spec
  [ ] Visual inspection pass (no foreign material, label correct, code date legible)
  [ ] Metal detection pass:
        Ferrous: ≤1.5 mm
        Non-ferrous: ≤2.0 mm
        Stainless steel: ≤2.5 mm
  [ ] Micro hold time met (if applicable):
        Yeast/mold: 24–72 hrs incubation
        APC: 24–48 hrs
        Pathogens: 24–48 hrs (PCR) or 5–7 days (culture)
  [ ] COA for all incoming ingredients on file
  [ ] Retort/aseptic process records reviewed and signed (if applicable)
  [ ] Allergen verification complete (label matches production sequence)
  [ ] Net contents verified (NIST Handbook 133 compliance)
```

### Batch Record Contents

Every production batch must capture:

| Field | Description |
|-------|-------------|
| `batch_id` | Unique identifier linking to all records |
| `product` / `sku_id` | SKU produced |
| `start_time` / `end_time` | Production window |
| `line_id` | Which line was used |
| `ingredient_lots` | Every ingredient lot number and quantity used |
| `process_parameters` | Temperature, time, pressure, speed, Brix, pH |
| `qc_results` | In-process and finished product test results |
| `operator_id` | Who ran the batch |
| `yield_pct` | Actual output vs theoretical |
| `deviations` | Anything that went wrong and how it was resolved |
| `rework_events` | Any blend-back or reprocess actions |
| `release_decision` | Released / held / rejected, by whom, when |

## 2.5 Batch Sizing

```
Max Batch Size = min(
  Equipment Capacity (tank_size_gal),
  Expected Demand Before Expiry (daily_demand × shelf_life_days),
  Available Ingredient Inventory (constrained by shortest-supply ingredient)
)

Optimal Batch Size balances:
  Setup/changeover cost     → favors larger batches
  Inventory carrying cost   → favors smaller batches
  Shelf-life constraint     → caps batch size
  Equipment capacity        → physical upper limit
```

## 2.6 Failure Modes

| Failure | Detection | Action |
|---------|-----------|--------|
| Yield < 90% | `yield_pct < 90` | Investigate immediately: line waste, ingredient measurement, equipment malfunction |
| Micro positive | Lab result positive for pathogen | Reject batch, initiate CAPA, trace-forward all ingredient lots |
| pH drift above 4.6 | In-process pH check | STOP FILLING. Re-acidify and verify. If already filled, hold entire batch for process authority review |
| Brix drift > ±0.5 from target | In-process Brix check | Hold current tank, recalibrate refractometer, re-sample, adjust blend |
| Fill weight out of spec | Statistical process control (5-unit check) | Adjust filler, hold product since last passing check |
| Metal detector reject | Metal detector alarm | Isolate unit, increase check frequency, inspect upstream equipment for wear |
| Code date error | Visual check or camera system | STOP line, correct coder, quarantine all units with wrong code |

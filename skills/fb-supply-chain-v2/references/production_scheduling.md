# Production Scheduling — Deep Reference

## 1.1 Data Schema

| Field | Type | Unit | Typical Range |
|-------|------|------|---------------|
| `run_id` | string | — | UUID or sequential |
| `sku_id` | string | — | Internal SKU code |
| `batch_size_gal` | float | gallons | 500–50,000 |
| `fill_size_oz` | float | oz | 8–64 |
| `line_id` | string | — | Line identifier |
| `line_speed_upm` | int | units/min | 100–1,200 |
| `scheduled_start` | datetime | UTC | — |
| `scheduled_end` | datetime | UTC | — |
| `changeover_min` | int | minutes | 15–480 |
| `campaign_group` | string | — | Allergen/flavor family |
| `priority` | int | — | 1 (highest) – 5 |
| `status` | enum | — | scheduled, running, complete, held |

## 1.2 Run Sequencing Rules

### Allergen Sequencing — Light-to-Dark, Simple-to-Complex

Always schedule in this order within a production day:

```
SEQUENCE PRIORITY (run in this order):
1. Water / unflavored bases
2. Citrus (no Top 9 allergens)
3. Tropical fruit (no Top 9 allergens)
4. Berry (no Top 9 allergens)
5. Oat milk / plant-based (contains GLUTEN if oat-based — Top 9)
6. Kombucha (may contain trace soy from SCOBY nutrient)
7. Protein / functional (may contain MILK, SOY, TREE NUTS)
8. Any product with PEANUT or SESAME
```

If allergen sequencing is violated: Flag as `ALLERGEN_SEQUENCE_VIOLATION`. Require full wet CIP + allergen swab verification (ATP < 10 RLU + allergen-specific ELISA < 10 ppm) before running the next SKU.

### Changeover Time Estimation

```
changeover_min = base_changeover
  + (flavor_change ? flavor_flush_min : 0)
  + (allergen_change ? full_cip_min : 0)
  + (size_change ? mechanical_changeover_min : 0)
  + (process_change ? thermal_requalification_min : 0)

Typical values:
  base_changeover:              15–30 min
  flavor_flush_min:             20–45 min (rinse + recirculate)
  full_cip_min:                 60–120 min (caustic + acid + sanitize + rinse + swab)
  mechanical_changeover_min:    30–90 min (filler heads, cap type, labeler)
  thermal_requalification_min:  45–120 min (retort or aseptic requalification)
```

### Campaign Run Optimization

Group identical or similar SKUs to minimize changeovers. A campaign is 2+ consecutive runs of the same product family. Target campaign length: 4–8 hours minimum to amortize changeover cost.

```
campaign_efficiency = total_production_time / (total_production_time + total_changeover_time)
TARGET: campaign_efficiency > 0.80
FLAG if < 0.65
```

## 1.3 Process-Specific Scheduling

### Retort Canning

- Retort cycle time: 30–90 min depending on can size and product pH.
- Low-acid (pH > 4.6): requires scheduled process filing with FDA (21 CFR 113).
- Acidified (pH ≤ 4.6 by added acid): requires scheduled process + 21 CFR 114.
- Retort deviation = any failure to meet time/temperature → full batch hold + process authority review.
- Schedule retort runs in blocks to minimize heat-up/cool-down cycles.
- Retort capacity is measured in cans per cycle × cycles per shift. A typical still retort holds 2,000–6,000 cans; a continuous retort processes 300–1,000 cans/min.

### Aseptic Bottling

- Sterilization hold time for filler: 30–45 min at 250°F+ before production starts.
- Line must maintain sterility — any break in aseptic zone = re-sterilize (45–60 min lost).
- Schedule aseptic runs as long campaigns (8–16 hrs) to minimize sterilization overhead.
- Typical aseptic filler speeds: 200–600 bottles/min depending on format.
- Aseptic lines require a sterility test kit result (negative) before releasing product.

### Cold Brew Extraction

- Extraction time: 12–24 hours at 35–45°F.
- Must schedule extraction start 12–24 hrs before batch tank availability.
- Extraction vessels are the bottleneck — schedule extraction starts in rolling waves.
- Yield varies by grind size, water ratio, and steep time — expect 60–75% extraction efficiency.
- Typical water-to-coffee ratio: 4:1 to 8:1 by weight. Lower ratio = stronger concentrate.
- Filtration after extraction adds 1–3 hours (coarse → fine → optional sterile filter).

### Hot-Fill Process

- Product must reach ≥185°F at the filler. Fill, cap, invert bottle for 15–30 sec to sterilize cap interior.
- Cool to <100°F within 30 min post-inversion to prevent thermal degradation.
- Line speed is constrained by cooling tunnel capacity, not filler speed.
- Schedule hot-fill after aseptic (if sharing a line) to avoid contaminating the aseptic zone.

### Co-Packing

- Co-packer scheduling requires 2–4 week lead time minimum.
- Minimum run quantities: typically 5,000–25,000 cases per SKU.
- Co-packer changeover costs are passed through — $500–$2,500 per changeover.
- Schedule co-pack runs to fill full truckloads (20–22 pallets) to optimize freight.
- Ingredient shipping to co-packer must arrive 3–5 days before scheduled run for receiving/QC.

## 1.4 OEE (Overall Equipment Effectiveness)

```
Availability = (Planned Time − Downtime) / Planned Time
Performance  = (Units Produced × Ideal Cycle Time) / Available Time
Quality      = Good Units / Total Units Produced
OEE          = Availability × Performance × Quality
```

| OEE Component | Target | Flag Below |
|---------------|--------|------------|
| Availability | >90% | 85% |
| Performance | >95% | 90% |
| Quality | >99% | 97% |
| OEE (composite) | >85% | 65% |

Track OEE by line, shift, AND product. Aggregate OEE hides problems. A line might run at 85% OEE on Product A and 55% on Product B.

### The Six Big Losses (F&B-adapted)

1. **Breakdowns**: Filler jams, pump failures, seal failures.
2. **Setup/Changeovers**: Product switches, flavor changes, size changes, CIP time.
3. **Small stops**: Label misfeeds, cap jams, sensor trips.
4. **Reduced speed**: Running below rated speed due to viscosity, foaming, or temperature.
5. **Process defects**: Underfill, wrong Brix, contamination.
6. **Startup rejects**: Product lost during startup until stable quality achieved.

## 1.5 Capacity Planning

```
Gross Capacity = Hours/shift × Shifts/day × Days/week × Line speed (units/hr)
Net Capacity   = Gross Capacity × OEE
Available      = Net Capacity − Planned Maintenance − Planned CIP
```

| Utilization | Interpretation |
|-------------|----------------|
| <70% | Underutilized. High fixed cost per unit. Seek additional volume. |
| 70–85% | Healthy. Room for demand spikes and maintenance. |
| 85–95% | Tight. Limited flexibility. Plan peak season carefully. |
| >95% | Maxed. Any disruption = missed orders. Add capacity or outsource. |

## 1.6 Failure Modes

| Failure | Detection | Action |
|---------|-----------|--------|
| Allergen sequence break | `campaign_group` order violates hierarchy | Hold line, require full CIP + allergen swab |
| Retort deviation | Time or temp below scheduled process | Full batch hold, notify process authority |
| Aseptic zone breach | Sterility break detected by sensor or operator | Re-sterilize filler, hold all product since last confirmed sterile point |
| Changeover exceeds estimate by >50% | `actual_changeover > changeover_min × 1.5` | Flag for root cause — mechanical issue or SOP gap |
| Line downtime >30 min unplanned | `downtime_min > 30 AND reason != 'scheduled'` | Flag for maintenance predictor, update OEE |
| Hot-fill temp drop below 185°F | Filler temperature sensor | Hold all units filled since last confirmed ≥185°F reading |
| Cold brew extraction <55% yield | `extraction_yield < 0.55` | Check grind size, water temp, steep time; adjust parameters |

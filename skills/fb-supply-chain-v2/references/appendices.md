# Appendices — Beverage Specs, Conversions, Alerting Thresholds

## Appendix A: Common Beverage Specifications

| Parameter | Juice (Hot-Fill) | Kombucha | Oat Milk | Cold Brew | Functional |
|-----------|-----------------|----------|----------|-----------|------------|
| Brix | 10–14 | 3–8 | 8–12 | 2–5 | 8–14 |
| pH | 3.2–4.0 | 2.8–3.5 | 6.5–7.2 | 4.8–5.5 | 3.0–4.2 |
| TA (%) | 0.4–1.2 | 0.3–0.8 | N/A | 0.8–1.5 | 0.3–1.0 |
| Fill temp (°F) | 185–195 | 34–38 | 34–42 | 34–38 | Varies |
| Process | Hot-fill/hold/invert | None (raw) | HTST or UHT | Cold-fill, N2 flush | Hot-fill or aseptic |
| Shelf life | 12–18 mo | 60–120 days | 7–365 days* | 90–180 days | 12–24 mo |
| Storage | Ambient | Refrigerated | Both* | Refrigerated | Ambient |
| CO2 | No | Yes (natural, 1.5–3.0 vol) | No | Optional (nitro) | Optional |
| DO2 target | <50 ppb | N/A | <100 ppb | <50 ppb | <50 ppb |
| Typical batch (gal) | 2,000–10,000 | 500–5,000 | 2,000–15,000 | 500–3,000 | 2,000–10,000 |
| Fill sizes (oz) | 10, 12, 15.2, 32, 64 | 12, 15.2, 16 | 32, 52, 64 | 10, 12, 32 | 8, 12, 16 |

*Oat milk: refrigerated HTST = 7–14 days; aseptic UHT = 9–12 months.

### Carbonation Levels by Product Type

| Product | CO2 Volumes | Pressure (PSI at 38°F) |
|---------|------------|----------------------|
| Still water | 0 | N/A |
| Light sparkling | 1.5–2.5 | 10–18 |
| Kombucha (natural) | 1.5–3.0 | 10–22 |
| Standard carbonated | 2.5–3.5 | 18–28 |
| Highly carbonated (energy) | 3.5–4.5 | 28–38 |
| Beer reference | 2.4–2.8 | 12–16 |

### Process Temperature Reference

| Process | Temperature | Duration | Application |
|---------|-------------|----------|-------------|
| HTST pasteurization | 161°F / 72°C | 15 seconds | Juice, dairy, oat milk |
| HTST (extended) | 175–185°F / 80–85°C | 15–30 seconds | High-pulp juice, viscous products |
| UHT | 280°F / 138°C | 2–4 seconds | Aseptic oat milk, shelf-stable dairy |
| Hot-fill | 185–195°F / 85–91°C | Fill + hold + invert | Acidic beverages (pH ≤ 4.6) |
| Tunnel pasteurization | 140–160°F / 60–71°C | 10–30 minutes | Carbonated beverages post-fill |
| Retort | 240–260°F / 116–127°C | 20–90 minutes | Low-acid canned foods |
| Cold brew extraction | 35–45°F / 2–7°C | 12–24 hours | Cold brew coffee |
| Carbonation | 34–38°F / 1–3°C | Continuous | CO2 injection |
| Nitrogen dosing | 34–38°F / 1–3°C | Continuous | Nitro cold brew, headspace purge |

## Appendix B: Unit Conversion Reference

### Volume

```
1 gallon     = 128 fluid ounces
1 gallon     = 3.785 liters
1 liter      = 33.814 fluid ounces
1 barrel (bev) = 31 gallons
1 drum       = 55 gallons
1 tote (IBC) = 275 gallons (typical)
1 tanker     = 5,000–6,500 gallons
```

### Weight

```
1 pound      = 16 ounces (avoirdupois)
1 pound      = 453.592 grams
1 kilogram   = 2.20462 pounds
1 metric ton = 2,204.62 pounds
1 short ton  = 2,000 pounds
```

### Temperature

```
°F = (°C × 9/5) + 32
°C = (°F - 32) × 5/9

Key reference points:
  Water freezes:    32°F / 0°C
  Refrigeration:    34–38°F / 1–3°C
  HTST pasteurize:  161°F / 72°C
  Hot-fill:         185°F / 85°C
  UHT:              280°F / 138°C
  Retort:           250°F / 121°C
```

### Pressure

```
1 PSI = 6.895 kPa
1 bar = 14.504 PSI

Key reference points:
  Aseptic filler backpressure:  5–15 PSI
  Retort operating pressure:    15–25 PSI
  CO2 carbonation pressure:     25–45 PSI (varies by target volumes and temp)
  Nitrogen dosing:              30–50 PSI
  HPP (high pressure processing): 43,500–87,000 PSI (300–600 MPa)
```

### Packaging: Cases per Pallet (standard 48×40)

| Format | Cases/Pallet | Lbs/Pallet (approx) |
|--------|-------------|---------------------|
| 12oz cans (24-pack) | 84–100 | 1,800–2,200 |
| 16oz bottles (12-pack) | 72–84 | 1,400–1,700 |
| 32oz / 1L bottles (12-pack) | 48–60 | 1,200–1,500 |
| 500ml bottles (24-pack) | 60–72 | 1,600–1,900 |
| Gallon jugs (4-pack) | 36–48 | 1,200–1,600 |

### Truck Capacity

```
Standard 53ft trailer:
  Pallets: 20–22 (double-stacked if height allows)
  Cases: ~1,500–2,200 (varies by format)
  Weight limit: 44,000 lbs (including pallets)

  → Check which constrains first: CUBE or WEIGHT
  → Heavy products (glass, gallons): often weight-constrained
  → Light products (large PET, snacks): often cube-constrained
```

## Appendix C: Critical Alerting Thresholds

### Immediate Escalation (notify quality + operations within 15 min)

```
- Pathogen positive (Salmonella, Listeria monocytogenes, E. coli O157:H7)
- Retort deviation (time or temp below scheduled process)
- Aseptic zone sterility breach
- Allergen cross-contact confirmed
- Foreign material found in product
- Cold chain break: > 45°F for refrigerated product
- pH of acidified product > 4.6 (food safety critical limit)
- Customer illness complaint linked to product
```

### Same-Day Escalation (notify within 4 hours)

```
- Batch yield < 90%
- In-process check failure (3+ consecutive out of spec)
- Supplier COA parameter out of spec
- Customer complaint: foreign material (non-illness)
- OTIF miss on key account shipment
- Inventory negative or count variance > tolerance
- Metal detector rejecting > 3 units per hour
- Unplanned line downtime > 2 hours
- Hot-fill temperature drop below 185°F
```

### Weekly Review (include in S&OP or quality review)

```
- Yield trending down (3+ batches below target)
- Supplier scorecard decline (dropped below 80)
- Forecast bias > ±10% for 2+ consecutive months
- COGS per unit increase > 5% vs prior quarter
- Scrap rate > 3% for any product line
- Days of supply < safety stock for any A-item
- OEE < 65% for any line (weekly average)
- Trade spend ROI < 0.5 for any active promotion
- Cold storage utilization > 90%
- Open holds aging > 7 days without disposition
```

### Monthly Review (include in executive S&OP)

```
- Gross margin < 20% on any SKU
- MAPE > 35% at portfolio level
- OTIF < 90% (rolling 30-day)
- Supplier on-time delivery < 90% (any strategic supplier)
- Total trade spend > 25% of gross revenue
- New product velocity < 1 unit/store/week at week 12
- Inventory turns below segment benchmark
- Freight cost > 8% of wholesale case price (any lane)
```

## Appendix D: Regulatory Quick Reference

| Regulation | Applies To | Key Requirement |
|-----------|-----------|-----------------|
| 21 CFR 113 | Low-acid canned foods (pH > 4.6, aw > 0.85) | Scheduled process filing, retort records |
| 21 CFR 114 | Acidified foods | Scheduled process filing, pH monitoring |
| 21 CFR 117 | All human food facilities | Preventive Controls (cGMP + HARPC) |
| FSMA 204 | Foods on FDA Traceability List | CTEs/KDEs, sortable electronic records |
| FSMA PCHF | All food manufacturers | Hazard analysis, preventive controls, supply chain program |
| FSMA FSVP | Importers of food | Foreign supplier verification |
| NIST Handbook 133 | All packaged foods | Net contents accuracy (fill weight) |
| FALCPA + FASTER Act | All packaged foods | Top 9 allergen declaration |
| FDA Nutrition Labeling (21 CFR 101.9) | Most packaged foods | Nutrition Facts panel format and rounding |
| Fair Packaging and Labeling Act | All consumer commodities | Label format, net quantity statement |
| FD&C Act Section 403 | All food | Misbranding provisions |

## Appendix E: KPI Summary Dashboard

| Domain | KPI | Formula | Target | Flag |
|--------|-----|---------|--------|------|
| Production | OEE | Availability × Performance × Quality | >85% | <65% |
| Production | Campaign efficiency | Production time / (production + changeover) | >80% | <65% |
| Batch | Yield % | Actual / theoretical × 100 | >96% | <90% |
| Batch | Scrap rate | Loss units / theoretical × 100 | <3% | >5% |
| Inventory | Days of supply | Qty available / avg daily usage | Varies | < lead time |
| Inventory | FEFO compliance | FEFO shipments / total shipments × 100 | >99% | <97% |
| Inventory | Waste rate | (Expired + damaged) / throughput × 100 | <2% | >3% |
| Procurement | Supplier OTD | On-time POs / total POs × 100 | >95% | <90% |
| Procurement | Supplier quality | Accepted lots / total lots × 100 | >98% | <95% |
| Logistics | OTIF | On-time ∩ in-full / total shipments × 100 | >95% | <90% |
| Logistics | Freight/case | Total freight / cases shipped | <5% of price | >8% |
| Demand | MAPE | Mean |actual-forecast|/actual × 100 | <25% | >35% |
| Demand | Bias | Σ(forecast-actual)/Σ actual × 100 | ±5% | >±10% |
| Cost | Gross margin | (Price - COGS) / price × 100 | >40% branded | <20% |
| Cost | Trade spend % | Trade spend / gross revenue × 100 | <20% | >25% |
| Quality | Incoming acceptance | Accepted lots / total lots × 100 | >98% | <95% |
| Quality | Hold aging | Holds > 7 days | 0 | Any |

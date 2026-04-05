# BOM & Formulation — Deep Reference

## 3.1 Data Schema

| Field | Type | Unit | Typical Range |
|-------|------|------|---------------|
| `bom_id` | string | — | BOM-001 through BOM-NNN |
| `ingredient_id` | string | — | RM-XXXXX |
| `ingredient_name` | string | — | — |
| `formula_pct` | float | % | 0.01–99.0 |
| `density_lb_per_gal` | float | lb/gal | 8.3–9.5 (most beverages) |
| `batch_size_gal` | float | gallons | 500–50,000 |
| `fill_size_oz` | float | oz | 8–64 |
| `price_per_lb` | float | $/lb | 0.01–25.00 |
| `overage_pct` | float | % | 1–5 |
| `allergen_flags` | array | — | Top 9 allergen codes |
| `organic_certified` | bool | — | — |
| `kosher_certified` | bool | — | — |

## 3.2 Density Reference

| Product Type | Typical Density (lb/gal) | Notes |
|-------------|-------------------------|-------|
| Water | 8.34 | Reference baseline |
| Juice (10–12 °Brix) | 8.55–8.75 | Increases with sugar content |
| Juice concentrate (42 °Brix) | 9.6–10.2 | Significantly denser |
| Kombucha (4–8 °Brix) | 8.40–8.55 | Lower sugar = closer to water |
| Oat milk | 8.55–8.70 | Varies with oat solids content |
| Carbonated beverage | 8.40–8.60 | CO2 reduces apparent density slightly |
| Simple syrup (65 °Brix) | 10.8–11.2 | Very dense |
| Citric acid solution (50%) | 9.8–10.0 | — |
| Honey | 11.8–12.2 | Extremely dense |
| Coconut cream | 8.5–8.8 | Varies by fat content |

### Brix-to-Density Approximation

```
density_lb_per_gal ≈ 8.34 × (1 + 0.004 × brix)
  Accurate to ±1% for Brix 0–40.
  For Brix > 40 (concentrates), use refractometer-specific tables.
```

## 3.3 Recipe Scaling Formulas

```
SCALE FROM BATCH A TO BATCH B:
  scale_factor = batch_b_gal / batch_a_gal
  ingredient_lbs_b = ingredient_lbs_a × scale_factor

CONVERT FORMULA % TO WEIGHT:
  ingredient_lbs = batch_gal × density_lb_per_gal × (formula_pct / 100)

CONVERT WEIGHT TO VOLUME (liquid ingredients):
  ingredient_gal = ingredient_lbs / ingredient_density_lb_per_gal

BRIX BLENDING (two-stream):
  target_brix = (stream_a_gal × brix_a + stream_b_gal × brix_b)
                / (stream_a_gal + stream_b_gal)
  → Solve for stream_a_gal or stream_b_gal given target

PEARSON SQUARE (quick blending):
  parts_of_a = |target_brix - brix_b|
  parts_of_b = |target_brix - brix_a|
  ratio = parts_of_a : parts_of_b
```

### Non-Linear Scaling Notes

Recipe scaling is NOT always linear. Common non-linearities in beverages:

1. **Heat transfer**: Surface-to-volume ratio changes at scale. Hot-fill hold times may need adjustment at larger batch volumes.
2. **Mixing dynamics**: Emulsions and suspensions behave differently. Oat milk requires higher shear at scale to maintain homogeneity.
3. **Flavor perception**: At larger volumes, subtle flavors may get lost. Flavor dosing often needs 5–15% increase at full production scale vs bench-top.
4. **Acidification**: pH changes may not be linear with volume due to buffering effects. Always verify pH after scaling.
5. **Carbonation**: CO2 absorption rates depend on temperature, pressure, and surface area — all change with tank size.

Best practice: Scale in steps (bench → pilot → production). Document scaling factors for each product.

## 3.4 Overage Factors

Apply overage to account for line losses, tank heels, and QC samples:

| Component | Standard Overage | Notes |
|-----------|-----------------|-------|
| Concentrate / juice | 2–3% | Higher for viscous products |
| Water | 1–2% | Lower loss rate |
| Flavors | 3–5% | Small volumes, high loss in transfer |
| Vitamins / minerals | 3–5% | Must account for degradation over shelf life |
| Cultures (kombucha) | 5–10% | Viability loss during processing |
| Packaging (bottles) | 1–2% | Breakage, rejects |
| Packaging (caps) | 1–2% | Misfeeds, cross-threading |
| Labels | 2–3% | Misregistration, splice waste |

```
order_qty = theoretical_qty × (1 + overage_pct / 100)
```

### Vitamin Overage Specifics

Vitamins degrade over shelf life. Overage at formulation must compensate:

| Vitamin | Typical Overage at Formulation | Notes |
|---------|-------------------------------|-------|
| Vitamin C (ascorbic acid) | 15–25% | Degrades ~10–15%/year in liquid, more with heat/light/oxygen |
| B vitamins (B6, B12, niacin) | 10–20% | Moderate stability in acidic beverages |
| Vitamin D | 5–10% | Relatively stable in fortified beverages |
| Vitamin A | 10–15% | Light-sensitive, fat-soluble |
| Zinc, Iron | 5–10% | Mineral forms are generally stable |

Overage must ensure label claim is met at END of shelf life, not just at production.

## 3.5 Ingredient Substitution Rules

```
SUBSTITUTION DECISION TREE:

IF primary_ingredient unavailable:
  CHECK substitution_table for approved alternates
  IF approved_alternate exists:
    VERIFY: allergen profile matches (no new allergens introduced)
    VERIFY: organic/kosher/halal status matches if product requires
    VERIFY: price delta < 15% (flag if higher for cost approval)
    VERIFY: functionality equivalent (Brix contribution, pH effect, viscosity)
    → Substitution requires quality approval + updated batch record
  IF no approved_alternate:
    ESCALATE to R&D. Do not substitute unapproved ingredients.
```

### Common Beverage Substitutions

| Primary | Approved Substitute | Adjustment Required |
|---------|-------------------|-------------------|
| Citric acid | Malic acid | Malic is ~90% as strong — increase dose by ~10% |
| Cane sugar | Beet sugar | Functionally identical; check organic cert |
| Ascorbic acid (source A) | Ascorbic acid (source B) | Match by active content, not by weight |
| Lemon juice concentrate | Lemon juice NFC | Adjust for Brix difference (concentrate ~42°Bx vs NFC ~8°Bx) |
| Oat fiber (source A) | Oat fiber (source B) | Verify particle size and water absorption; affects mouthfeel |

### Never Substitute Without R&D Approval

- **Natural flavors**: Flavor profiles are not interchangeable even within the same flavor family.
- **Cultures / probiotics**: Strain-specific efficacy and regulatory claims.
- **Gums / stabilizers**: Xanthan, gellan, pectin have different functionality at different concentrations and pH ranges.
- **Preservatives**: Sorbate, benzoate, natamycin have different efficacy spectra and regulatory limits.

## 3.6 Allergen Matrix Management

### The Top 9 (US — FALCPA + FASTER Act)

1. Milk
2. Eggs
3. Fish
4. Crustacean shellfish
5. Tree nuts
6. Peanuts
7. Wheat
8. Soybeans
9. Sesame

### Cross-Contact Classification

| Level | Definition | Label Implication |
|-------|-----------|-------------------|
| **Contains** | Allergen intentionally added as ingredient | "Contains: [allergen]" required |
| **May contain (shared line)** | Same line processes allergen-containing products | Advisory "may contain" statement (voluntary but recommended) |
| **May contain (shared facility)** | Same facility, different lines | Advisory based on risk assessment |
| **Free from** | No allergens in facility or validated controls | Can make "free from" claim if validated |

### Allergen Change Management

If an ingredient supplier changes their formulation or facility and introduces a new allergen:
1. Flag as `ALLERGEN_CHANGE` in supplier management system.
2. Hold all existing inventory of that ingredient.
3. Review all finished products using that ingredient for label accuracy.
4. If new allergen present: update label, notify customers, assess recall need for shipped product.

## 3.7 BOM Multi-Level Explosion

```
EXAMPLE: 12oz Organic Lemonade

Level 0: Finished Product (12oz Bottle Organic Lemonade)
├── Level 1: Lemonade Blend (liquid)
│   ├── Level 2: Simple Syrup (15% of blend)
│   │   ├── Level 3: Organic Cane Sugar (67% of syrup)
│   │   └── Level 3: Purified Water (33% of syrup)
│   ├── Level 2: Organic Lemon Juice Concentrate (8% of blend)
│   ├── Level 2: Citric Acid (0.3% of blend)
│   └── Level 2: Purified Water (76.7% of blend)
├── Level 1: 12oz PET Bottle
├── Level 1: 38mm Cap
├── Level 1: Shrink Sleeve Label
└── Level 1: 24-count Tray
    ├── Level 2: Corrugated Case
    └── Level 2: Divider Insert

BOM EXPLOSION for 10,000 bottles:
  Total blend needed: (10,000 × 12 oz) / 128 oz/gal = 937.5 gal
  Simple Syrup: 937.5 × 0.15 = 140.6 gal
    Sugar: 140.6 × 0.67 × 10.9 lb/gal = 1,025.6 lbs
    Water: 140.6 × 0.33 = 46.4 gal
  Lemon concentrate: 937.5 × 0.08 = 75.0 gal
  Citric acid: 937.5 × 0.003 × 8.34 = 23.5 lbs
  Water: 937.5 × 0.767 = 719.1 gal
  Bottles: 10,000 × 1.02 overage = 10,200
  Caps: 10,200
  Labels: 10,000 × 1.03 = 10,300
  Trays: ceil(10,000 / 24) × 1.02 = 426
```

Apply yield factors at each level to get gross requirement.

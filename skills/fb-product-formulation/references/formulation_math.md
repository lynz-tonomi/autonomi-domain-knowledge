# Food Formulation Mathematics: Technical Reference

A practical calculation reference for daily formulator workflows. All examples use real-world data and common units.

## Table of Contents

1. [Brix, Specific Gravity, Density](#brix-specific-gravity-density)
2. [Dilution & Blending](#dilution--blending)
3. [pH & Titratable Acidity](#ph--titratable-acidity)
4. [Batch Scaling](#batch-scaling)
5. [Nutritional Calculations](#nutritional-calculations)
6. [Yield Calculations](#yield-calculations)
7. [Water Activity & Moisture](#water-activity--moisture)
8. [Cost Modeling](#cost-modeling)

---

## Brix, Specific Gravity, Density

### What is Brix?

**Brix (°Bx)** = % sucrose by weight in a solution, measured via refractometer.

- Pure water = 0°Bx
- 10% sucrose solution = 10°Bx
- Orange juice concentrate ≈ 65°Bx

Brix is **concentration independent of temperature** once set, but refractometer readings *vary slightly* with temperature (typically ±0.1°Bx per 10°C).

### Corrected Brix for Non-Sugar Solids

Real juice and beverages contain acids, pigments, proteins, and alcohol—not just sucrose. These dissolved solids inflate apparent Brix slightly.

**Corrected Brix** accounts for the refractive index contributions of other solids:

```
Corrected Brix ≈ Measured Brix - (Acid correction + Alcohol correction + Other solids)
```

**Common corrections:**

| Substance | Correction Factor |
|-----------|-------------------|
| Citric acid (1% TA) | −0.15 to −0.25°Bx |
| Malic acid (1% TA) | −0.15 to −0.25°Bx |
| Ethanol (1% ABV) | −0.06°Bx |
| Pectin (0.1%) | −0.02°Bx |

**Example:** Orange juice with measured Brix of 12.5°Bx, 0.8% TA (citric acid), 0.5% ethanol:

```
Corrected Brix = 12.5 - (0.8 × 0.20) - (0.5 × 0.06)
               = 12.5 - 0.16 - 0.03
               = 12.31°Bx
```

For production, always **report corrected Brix** in specifications.

### Density from Brix (Quick Estimation)

**Linear approximation:**

```
Density (g/mL) ≈ 1.000 + (Brix × 0.004)
```

**Example:** 12°Bx orange juice:

```
Density ≈ 1.000 + (12 × 0.004) = 1.048 g/mL
```

This is accurate within ±0.002 g/mL for Brix 0–70 and solutions dominated by sucrose.

**More precise:** Use USDA sugar-density tables or:

```
Density (g/mL) = 0.99823 + (0.01839 × Brix) + (0.00056 × Brix²)
```

For Brix > 50 or non-sugar solutions, measure density directly via hydrometer or pycnometer.

### Specific Gravity

**Specific Gravity (SG)** = density of solution / density of pure water at same temperature.

```
SG = ρ_solution / ρ_water
```

At 20°C, density of water ≈ 0.9982 g/mL.

**Example:** 12°Bx orange juice at density 1.048 g/mL:

```
SG = 1.048 / 0.9982 = 1.049
```

**Why it matters:**
- Recipe scaling: ingredient volumes change with density. A gallon of 12°Bx juice weighs more than a gallon of 4°Bx juice.
- Tank calibration: tank volumes are marked by volume, but you fill by weight. Weight = volume × density.
- Gravity compensation in dosing systems.

---

## Dilution & Blending

### Dilution: C₁V₁ = C₂V₂

Diluting a concentrate to target concentration:

```
C₁V₁ = C₂V₂

Where:
C₁ = initial concentration (°Bx, % TA, ppm, etc.)
V₁ = initial volume
C₂ = target concentration
V₂ = final volume
```

**Example:** Dilute 100 L of 65°Bx orange juice concentrate to 12°Bx:

```
65 × 100 = 12 × V₂
V₂ = 6500 / 12 = 541.7 L

Water to add = 541.7 - 100 = 441.7 L
```

**Sanity check:** We're diluting 65× to 12×, so we expect roughly 5.4× volume increase. ✓

**Important:** This formula assumes:
- Complete mixing (no stratification).
- Additive volumes (especially valid for dilute aqueous solutions; concentrated syrups may show slight non-additivity).
- No chemical reactions (e.g., acid + base neutralization).

For weight-based dilution (more accurate):

```
M₁ × C₁ = M₂ × C₂

Where M = mass (kg or lb)
```

**Example (weight-based):** 100 kg of 65°Bx concentrate to 12°Bx:

```
100 × 65 = M₂ × 12
M₂ = 6500 / 12 = 541.7 kg

Water to add = 541.7 - 100 = 441.7 kg (assuming water density ≈ 1 kg/L)
```

### Pearson's Square for Two-Component Blending

Blend two ingredients at different concentrations to hit a target concentration **with minimal waste**.

**Setup:** Arrange in a square:

```
          ┌─────────────────────┐
          │     C₁    |  (C₂−Ct)│
          │           |         │
          │    Ct ────┼─────    │
          │           |         │
          │     C₂    |  (Ct−C₁)│
          └─────────────────────┘

C₁ = concentration of first ingredient
C₂ = concentration of second ingredient
Ct = target concentration
```

**Parts of first ingredient** : **Parts of second ingredient** = (C₂ − Ct) : (Ct − C₁)

**Example:** Blend 65°Bx orange concentrate (C₁) with water (C₂ = 0°Bx) to reach 12°Bx (Ct):

```
Parts concentrate : Parts water = (0 - 12) : (12 - 65)
                                = (-12) : (-53)
                                = 12 : 53
```

To make 1000 L of 12°Bx juice:

```
Total parts = 12 + 53 = 65

Concentrate needed = (12/65) × 1000 = 184.6 L
Water needed = (53/65) × 1000 = 815.4 L

Check: (184.6 × 65) + (815.4 × 0) = 12000
       12000 / 1000 = 12°Bx ✓
```

**Why Pearson's Square matters:** It minimizes total volume (no overthinking ratios). For three or more components, use **mass balance** (see Multi-Component Blending below).

### Multi-Component Blending: Mass Balance

For recipes with 3+ ingredients at different concentrations:

```
Σ(Mass_i × Concentration_i) = Mass_final × Concentration_final

Or: Σ(Solute_i) = Solute_final
```

**Example:** Make 1000 kg of 12°Bx beverage from:
- 65°Bx orange concentrate
- 20°Bx apple concentrate
- Water (0°Bx)
- Target: 12°Bx

Let x = kg orange concentrate, y = kg apple concentrate, z = kg water.

**Constraint 1 (mass balance):**
```
x + y + z = 1000
```

**Constraint 2 (solute balance):**
```
65x + 20y + 0z = 12 × 1000
65x + 20y = 12000
```

Assume a ratio—say 80% orange, 20% apple (by solute contribution):

```
65x = 0.8 × 12000 = 9600  →  x = 147.7 kg
20y = 0.2 × 12000 = 2400  →  y = 120 kg
z = 1000 - 147.7 - 120 = 732.3 kg
```

**Verification:**
```
(147.7 × 65) + (120 × 20) + (732.3 × 0) = 9600 + 2400 = 12000 ✓
12000 / 1000 = 12°Bx ✓
Total mass = 147.7 + 120 + 732.3 = 1000 kg ✓
```

---

## pH & Titratable Acidity

### pH Fundamentals

```
pH = −log₁₀[H⁺]

Where [H⁺] = molar concentration of hydrogen ions
```

pH is **logarithmic**: each step = 10× change in acidity.

| pH | [H⁺] (mol/L) | Perceived Acidity | Examples |
|----|--------------|--------------------|----------|
| 2  | 0.01         | Very sour          | Vinegar  |
| 3  | 0.001        | Sour               | Lemon juice, orange juice |
| 4  | 0.0001       | Tart               | Tomato juice, apple juice |
| 5  | 0.00001      | Mildly tart        | Coffee  |
| 7  | 10⁻⁷         | Neutral            | Pure water |

**Key for beverages:** pH 3.0 is **10× more acidic** than pH 4.0 (even though the difference looks small).

### Titratable Acidity (TA)

**Titratable Acidity** = grams of acid per 100 mL, expressed as the predominant acid.

**Method:** Titrate with 0.1 M NaOH to pH 8.3 (phenolphthalein endpoint), measure mL NaOH used.

```
TA (%) = (mL NaOH × 0.1 M × MW_acid / 1000) / (Sample mL) × 100

Where MW_acid = molecular weight of predominant acid
```

**Common acids & molecular weights:**

| Acid | MW (g/mol) | Typical in |
|------|-----------|-----------|
| Citric (C₆H₈O₇) | 192 | Juice, citrus drinks |
| Malic (C₄H₆O₅) | 134 | Apple juice, stone fruits |
| Tartaric (C₄H₆O₆) | 150 | Wine, grape juice |
| Acetic (CH₃COOH) | 60 | Vinegar |
| Lactic (C₃H₆O₃) | 90 | Fermented beverages |

**Example:** 10 mL orange juice requires 8.5 mL of 0.1 M NaOH to reach pH 8.3. Predominant acid = citric (MW 192):

```
TA (%) = (8.5 × 0.1 × 192 / 1000) / 10 × 100
       = (0.1632) / 10 × 100
       = 1.632% (or 1.63% as citric acid)
```

### Buffer Capacity

**Buffer capacity (β)** = amount of acid or base needed to change pH by 1 unit.

```
β = dn/dpH

Where n = moles of acid or base added
```

**Practical:** Measure buffer capacity empirically:

1. Measure pH of 100 mL sample.
2. Add 1 mL of 0.1 M HCl, stir 1 min, measure pH.
3. Buffer capacity ≈ 0.1 mmol / ΔpH.

**Typical examples:**

| Product | Buffer Capacity | Example |
|---------|-----------------|---------|
| Orange juice (1% TA) | ≈ 0.08 | ΔpH ≈ 1.25 with 0.1 M HCl |
| Water + citric acid (0.1% TA) | ≈ 0.008 | ΔpH ≈ 12.5 with 0.1 M HCl |
| Flavored water (low TA) | ≈ 0.005 | Very pH-sensitive |

**Why it matters:** High buffer capacity = pH stable during fermentation or storage. Low buffer capacity = risk of pH drift (especially in low-acid drinks).

### Brix/Acid Ratio

**Brix/Acid Ratio** (or **BRIX:TA ratio**) predicts perceived sweetness balance.

```
Brix/Acid Ratio = °Bx / TA(%)
```

**Targets by product type:**

| Product | Target Ratio | Example |
|---------|--------------|---------|
| Orange juice | 12–16 | 12°Bx / 0.8% TA = 15 |
| Apple juice | 15–22 | 13°Bx / 0.65% TA = 20 |
| Lemonade | 8–12 | 10°Bx / 1.2% TA = 8.3 |
| Cranberry juice | 10–15 | 11°Bx / 1.1% TA = 10 |
| Tropical fruit blend | 12–18 | 14°Bx / 0.9% TA = 15.6 |

**Example:** You're formulating a new apple-mango blend.

Target Brix = 13°Bx. Industry benchmark for apple-mango = 14:1 ratio.

```
Required TA = 13 / 14 = 0.93%
```

Measure apple concentrate: 0.6% TA. Mango: 0.35% TA. Water = 0% TA.

Use mass balance to hit 0.93% TA at 13°Bx (same as multi-component blending above).

---

## Batch Scaling

### Weight-Based Formulations (Not Volume)

**Critical rule:** Scale recipes by **weight**, never by volume.

**Why:** Density varies with Brix, temperature, and ingredient type. One liter of concentrate ≠ one liter of water.

**Example of failure:**

```
Recipe (incorrect, volume-based):
- 1 L orange concentrate (65°Bx)
- 4 L water
= 5 L total

Scaled to 500 L batch:
- 100 L concentrate
- 400 L water
= 500 L... but this is wrong.

Density concentrate ≈ 1.27 g/mL → 100 L = 127 kg
Density water ≈ 1.00 g/mL → 400 L = 400 kg
Total mass = 527 kg, not 500 kg.
Final Brix = (127 × 65) / 527 = 15.65°Bx (target was 12°Bx) ✗
```

**Correct approach (weight-based):**

```
Recipe (correct):
- 200 kg @ 65°Bx orange concentrate
- 1033 kg @ 0°Bx water
= 1233 kg total batch

Solute check: (200 × 65) + (1033 × 0) = 13000 ÷ 1233 = 10.55°Bx ✓
```

### Scale Factor Calculation

```
Scale Factor (SF) = Target Batch Size (kg) / Formula Batch Size (kg)

Then: Ingredient Mass_scaled = Ingredient Mass_formula × SF
```

**Example:** Formula batch is 100 kg (orange juice concentrate 15 kg, water 85 kg). Scale to 1000 kg production batch:

```
SF = 1000 / 100 = 10

Concentrate needed = 15 × 10 = 150 kg
Water needed = 85 × 10 = 850 kg

Total = 1000 kg ✓
```

### Account for Process Losses

Always add a **loss factor** to ingredient amounts:

```
Ingredient Mass (including losses) = (Ingredient Mass × SF) / (1 - Loss Factor)

Loss Factor = Evaporation + Trim + Dead Volume + Overfill
```

**Common losses by process:**

| Loss Type | Typical % |
|-----------|-----------|
| Evaporation (pasteurization, 85–95°C) | 1–3% |
| Trim (start-up/shutdown waste) | 0.5–1% |
| Dead volume (pump, lines, valve) | 0.2–0.5% |
| Overfill (safety margin, ±2%) | 1–2% |
| **Total** | **3–6%** |

**Example:** Batch 1000 kg juice, expect 4% total loss:

```
Concentrate needed = (150 kg) / (1 - 0.04) = 150 / 0.96 = 156.25 kg
Water needed = (850 kg) / (1 - 0.04) = 850 / 0.96 = 885.42 kg

Total input = 156.25 + 885.42 = 1041.67 kg
Expected net output = 1041.67 × 0.96 = 1000 kg ✓
```

### Bill of Materials (BOM)

**BOM** sums ingredient costs per unit of finished product.

```
BOM ($/unit) = Σ(Ingredient Mass per Unit × Cost per kg)
```

**Example:** One 240 mL (8 fl oz) serving of orange juice costs:

```
Ingredients per serving (240 mL = 0.24 L @ 1.048 g/mL = 251.5 g):
- Orange concentrate: 38.6 g @ $3.50/kg = $0.135
- Water: 212.9 g @ $0.001/kg = $0.000
- Vitamin C: 0.35 g @ $15/kg = $0.005
- Citric acid: 2.5 g @ $1.20/kg = $0.003
- Potassium sorbate: 0.08 g @ $8/kg = $0.001

BOM = $0.144 per 240 mL serving
```

**To calculate packaging + overhead BOM:**

```
Total Cost per Unit = BOM + Packaging Cost + Allocated Labor + Allocated Utilities
```

---

## Nutritional Calculations

### Energy (Calories)

```
Energy (kcal) = (Protein g × 4) + (Total Carb g × 4) + (Fat g × 9) + (Alcohol g × 7)
```

**Example:** 240 mL orange juice:

| Component | g | kcal |
|-----------|---|------|
| Protein | 1.7 | 6.8 |
| Carbohydrate | 26.8 | 107.2 |
| Fat | 0.5 | 4.5 |
| Alcohol | 0 | 0 |
| **Total** | | **118.5 kcal** |

(Actual OJ ≈ 110 kcal per 240 mL; variation due to Brix and fiber.)

### Sugar Calculation

**Total Sugar** = sum of monosaccharides + disaccharides only.

Does **NOT** include:
- Sugar alcohols (sorbitol, xylitol, erythritol)
- Fiber (soluble or insoluble)
- Organic acids

**Example:** 240 mL orange juice, assuming typical composition:

| Sugar | g |
|-------|---|
| Fructose | 12.4 |
| Glucose | 9.2 |
| Sucrose | 5.2 |
| **Total Sugar** | **26.8 g** |

### Added Sugars (FDA Definition)

**Added Sugars** = sugars added during manufacturing or preparation, **excluding** sugars naturally present.

**Includes:**
- Cane sugar, high-fructose corn syrup (HFCS), honey, maple syrup added to recipe.
- Sugars from juice concentrate added beyond replacing natural juice loss.

**Does NOT include:**
- Sugars naturally in fruit, vegetable, or dairy ingredients.

**Example:** "Orange Juice Blend" with 50% juice + 50% added apple concentrate (to boost Brix):

```
Natural juice sugars (50% of content) = naturally occurring
Added concentrate sugars (50% of content) = added sugars (if it exceeds what's needed to replace natural loss)
```

If juice lost 3% solids during processing, adding > 3% concentrate = added sugar.

### Reference Amount Customarily Consumed (RACC)

FDA 21 CFR 101.12 sets serving sizes based on **Reference Amount Customarily Consumed**.

**Beverage RACCs:**

| Product | RACC (mL) | RACC (fl oz) |
|---------|-----------|-------------|
| 100% fruit/vegetable juice | 240 | 8 |
| Other beverages (flavored water, etc.) | 240 | 8 |
| Carbonated soft drinks | 360 | 12 |
| Water (plain) | 240 | 8 |

Nutrition facts must be reported **per serving**, where 1 serving = RACC.

**Example:** 240 mL orange juice with 26.8 g sugars:

```
Per RACC (240 mL): 26.8 g sugar
Percent Daily Value (%DV) = (26.8 / 50) × 100 = 53.6%
(50 g/day is daily recommended value for reference 2000 kcal diet)
```

---

## Yield Calculations

### Batch Yield (Units)

```
Batch Yield (units) = (Batch Volume × Fill Efficiency) / Fill Volume per Unit

Or: Batch Yield (units) = (Batch Mass × Fill Efficiency) / (Fill Mass per Unit)
```

**Example:** Producing 240 mL servings from 1000 L batch:

```
Fill efficiency = 98% (2% foaming, drain loss, startup waste)
Effective volume = 1000 L × 0.98 = 980 L

Batch Yield = 980 L / 0.24 L per unit = 4083 units
```

### Fill Efficiency

**Fill Efficiency (%)** = (actual net volume) / (nominal fill × units). Accounts for:

- Foaming during fill (especially carbonated).
- Drain loss in lines and equipment.
- Startup/shutdown waste.
- Temperature-induced volume change post-fill.

**Typical values:**

| Process | Fill Efficiency |
|---------|-----------------|
| Still beverages, gravity fill | 98–99% |
| Carbonated drinks, counter-pressure fill | 97–98% |
| Aseptic fill, post-cooling | 97–98% |
| Hot fill (shrinkage on cool-down) | 96–97% |

### Overfill Strategy

**Declared fill volume** ≈ target ± tolerance.

**Actual fill** = declared + safety overfill (typically +1 to +2%).

```
Actual Fill = Declared Fill × (1 + Overfill %)
```

**Example:** Declared 240 mL, +1.5% overfill:

```
Actual fill target = 240 × 1.015 = 243.6 mL per unit

For 1000 L batch (1,000,000 mL):
Units = 1,000,000 / 243.6 ≈ 4104 units (vs. 4167 at exact 240 mL)

Cost per unit increases by ~1.5% (overfill material cost).
But avoids underfill violations and customer complaints.
```

---

## Water Activity & Moisture

### Water Activity (aₓ) Definition

```
aₓ = P / P₀

Where:
P = partial vapor pressure of water in the food
P₀ = vapor pressure of pure water at same temperature
```

Range: 0 (completely dry) to 1.0 (pure water).

**Why it matters:** Microbial growth, oxidative stability, texture change, and shelf life depend almost entirely on aₓ, **not** absolute moisture content.

### Raoult's Law (Simple Solutions)

For solutions with one dominant solute (e.g., sugar solution):

```
aₓ = 1 - (mole fraction of solute)

Or: aₓ ≈ 1 - (w / (w + W))

Where:
w = moles of solute
W = moles of solvent (water)
```

**Example:** 50% w/w sucrose solution:

```
Moles sucrose per 100 g: 50 g / 342 g/mol = 0.146 mol
Moles water per 100 g: 50 g / 18 g/mol = 2.78 mol

aₓ ≈ 1 - (0.146 / (0.146 + 2.78)) = 1 - 0.050 = 0.95
```

**Sucrose impact on aₓ:** A practical table:

| Sucrose (% w/w) | Estimated aₓ |
|-----------------|--------------|
| 0% (water) | 1.00 |
| 20% | 0.98 |
| 40% | 0.94 |
| 50% | 0.93 |
| 60% | 0.91 |
| 70% | 0.87 |

### Ross Equation (Multi-Solute)

For products with multiple dissolved solids (juice, jam, etc.):

```
aₓ(total) ≈ aₓ₁ × aₓ₂ × aₓ₃ × ... × aₓₙ

Where aₓᵢ = water activity contribution of each solute
```

**Example:** Jam with:
- 60% sucrose (aₓ ≈ 0.91)
- 5% glucose (aₓ ≈ 0.96 at this concentration)
- 35% water

```
aₓ(total) ≈ 0.91 × 0.96 = 0.875
```

(Actual jam aₓ measured ≈ 0.80–0.85; Ross underestimates slightly for very concentrated foods.)

### Critical aₓ Thresholds

| aₓ Range | Microbial Growth | Stability | Notes |
|----------|-----------------|-----------|-------|
| > 0.98 | All organisms | Aqueous solution (short shelf life) | OJ, juice, beverages |
| 0.93–0.98 | Most bacteria, fungi | Stable 6–12 mo. | Juice with added sugar, flavored water |
| 0.85–0.93 | Most bacteria inhibited | Stable 12–24 mo. | Jams, honey, syrups |
| 0.80–0.85 | Most molds inhibited | Stable 24+ mo. | High-solids preserves, dried fruit |
| 0.60–0.80 | No microbial growth | Very stable | Dry goods, cereal, cracker |
| < 0.60 | No microbial growth | Indefinite | Spices, powders, shelf-stable |

**Practical:** Most beverages target aₓ > 0.97 (rely on pH or preservatives for safety). Most shelf-stable fruit spreads target aₓ < 0.85.

### Moisture Isotherm Curves

Moisture content vs. aₓ at constant temperature (e.g., 25°C).

```
Isotherm = graph of equilibrium moisture (% w/w) at each aₓ
```

**Why important:** In multi-layer products (fruit filling + cookie crumb), moisture migrates from high-aₓ to low-aₓ regions. An isotherm curve predicts final equilibrium after weeks/months of storage.

**Example:** Granola bar with dried cranberries (low aₓ) + granola (high aₓ) + yogurt coating (high aₓ):

- Initially: cranberries aₓ ≈ 0.60, granola aₓ ≈ 0.50, yogurt aₓ ≈ 0.95.
- Over time: moisture diffuses from yogurt → cranberries → granola.
- **Result:** Cranberries soften, yogurt hardens, product texture degrades.

**Mitigation:** Use moisture barriers (wax coating, foil), or equilibrate all components to similar aₓ before assembly.

---

## Cost Modeling

### COGS (Cost of Goods Sold) per Unit

```
COGS per Unit = Raw Materials + Packaging + Direct Labor + Utilities + Waste Allowance
```

### Raw Material Cost

```
Raw Material Cost per Unit = Σ(Ingredient Mass per Unit × Delivered Cost per Unit Mass)
```

**Example:** 240 mL orange juice:

| Ingredient | Mass (g) | Cost/kg | Cost/Unit |
|-----------|----------|---------|-----------|
| Orange concentrate | 38.6 | $3.50 | $0.1351 |
| Water | 212.9 | $0.0008 | $0.0002 |
| Vitamin C (ascorbic acid) | 0.35 | $15.00 | $0.0053 |
| Citric acid | 2.5 | $1.20 | $0.0030 |
| Potassium sorbate | 0.08 | $8.00 | $0.0006 |
| **Total** | | | **$0.1442/unit** |

**Delivered cost** includes:
- FOB ingredient cost + freight + tariffs (if imported) + storage.

### Total COGS Calculation

```
Total COGS/Unit = Raw Material + Packaging + Overhead
```

**Example:** 240 mL OJ in aseptic Tetra Pak:

| Cost Component | $/Unit |
|---|---|
| Raw material (above) | $0.1442 |
| Aseptic Tetra Pak + straw | $0.0850 |
| Secondary packaging (case) | $0.0120 |
| Case labor + handling | $0.0180 |
| Utilities (fill plant) | $0.0090 |
| Waste allowance (2%) | $0.0040 |
| **Total COGS** | **$0.2722/unit** |

### Target Cost by Channel

```
Target COGS/Unit = Wholesale Price / Target Margin %
```

**Typical margin targets (COGS as % of wholesale):**

| Channel | Target COGS % | Notes |
|---------|--------------|-------|
| RTD beverage, mass retail | 25–35% | High volume, thin margin |
| Premium juice, specialty | 35–45% | Smaller volume, command premium |
| Co-pack (customer-owned product) | 20–30% | Customer absorbs other costs |
| Private label (retailer-owned) | 28–38% | Competitive with RTD |

**Example:** Wholesale price $1.50 per 240 mL OJ, target 30% COGS:

```
Target COGS = $1.50 × 0.30 = $0.45/unit

Current COGS (above) = $0.2722/unit ✓ (within budget)
```

### Reformulation for Cost Targets

**Ingredient substitution matrix:** Map which ingredients can swap at what ratios, with tradeoffs:

| Ingredient | Replacement | Ratio | Cost $/kg | Impact |
|-----------|-------------|-------|-----------|--------|
| Orange concentrate ($3.50/kg) | Apple concentrate ($2.00/kg) | 1:0.95 | Save $0.50/kg | Flavor shift, higher TA |
| Citric acid ($1.20/kg) | Malic acid ($0.90/kg) | 1:1.1 | Save $0.30/kg | Different taste, less astringency |
| Aseptic Tetra Pak ($0.085) | HDPE bottle + label ($0.052) | — | Save $0.033 | Shelf life reduced; requires preservative increase |
| Vitamin C ($15/kg) | Omit | 1:0 | Save $0.005 | Loss of marketing claim, may darken in storage |

**Example:** Target COGS $0.35/unit (vs. current $0.27):

```
Reduce concentrate from 38.6 g to 35 g orange + 2.5 g apple:
- Orange: 35 × $3.50 / 1000 = $0.1225
- Apple: 2.5 × $2.00 / 1000 = $0.0050
- Subtotal = $0.1275 (vs. $0.1351, save $0.0076/unit)

Switch packaging from Tetra Pak to HDPE bottle:
- Save $0.033/unit

New total COGS ≈ $0.2722 - $0.0076 - $0.033 = $0.2316/unit
```

**Tradeoff check:**
- Taste: Slightly more apple tang (customer testing required).
- Shelf life: HDPE allows light/oxygen ingress; increase potassium sorbate 0.1% → 0.15%.
- Perceived value: Less premium image.

---

## Summary: Formulator's Workflow Checklist

1. **Determine target Brix & TA** → Check Brix/Acid Ratio against product category.
2. **Source ingredients** → Note delivered costs, density, and measured Brix/TA.
3. **Design recipe (weight-based)** → Use mass balance for multi-component blending.
4. **Scale batch** → Apply scale factor and loss allowances.
5. **Calculate costs** → BOM, packaging, overhead.
6. **Measure physicochemical properties:**
   - Brix (refractometer, corrected).
   - pH and TA (titration).
   - aₓ (if shelf-stable product).
   - Density (if needed for dosing/tank calibration).
7. **Predict shelf life** → Based on aₓ, pH, preservatives, packaging.
8. **Verify nutrition facts** → Per RACC, using analyzed or database values.
9. **Cost optimization** → Iteratively substitute ingredients, retest, validate impact.

---

**Document Version:** 1.0
**Last Updated:** 2026-03-23
**Audience:** Food Science, Product Development, QA/QC

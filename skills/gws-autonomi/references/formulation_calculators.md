# Google Sheets Formulation Tools for F&B

## Overview

Google Sheets serves as the operational calculation engine for Autonomi's R&D, QC, and production teams. These spreadsheet tools handle formulation math, nutritional analysis, cost modeling, and process calculations that beverage manufacturers need daily. Each calculator is designed as a standalone sheet or tab within a master formulation workbook, with protected formula cells and clearly marked input fields.

---

## 1. Brix/Acid Ratio Calculator

### Purpose
The Brix-to-acid ratio is a primary quality metric for juice, juice beverages, and flavored drinks. It predicts perceived sweetness-to-tartness balance and is a key specification for incoming juice concentrates and finished products.

### Sheet Layout

| Cell | Label | Type | Notes |
|------|-------|------|-------|
| B2 | Product Name | Input | Dropdown from product master list |
| B3 | Sample ID / Lot | Input | Free text |
| B4 | Date | Input | Date picker |
| B5 | Brix (degrees) | Input | Measured by digital refractometer, corrected for temperature |
| B6 | Titratable Acidity (% as citric) | Input | From titration — expressed as % anhydrous citric acid equivalent |
| B8 | Brix/Acid Ratio | Formula | `=B5/B6` |
| B9 | Target Range | Lookup | From specification database, per product |
| B10 | Status | Formula | Conditional: "PASS" (green) if within range, "OUT OF SPEC" (red) if outside |

### Technical Notes

- Brix must be temperature-corrected to 20C before ratio calculation (most digital refractometers do this automatically; verify)
- Titratable acidity expressed as % anhydrous citric acid is standard for citrus-based beverages; for apple-based, express as % malic acid (conversion factor: 1.0 citric = 0.87 malic)
- Typical Brix/acid ratios: orange juice 12-16, grapefruit juice 7-10, apple juice 20-30, lemonade 8-12
- Ratio trending over shelf life indicates acid degradation or sugar hydrolysis
- Conditional formatting: green for within spec, yellow for within 10% of limit, red for out of spec

---

## 2. Batch Scaling Calculator

### Purpose
Converts laboratory formula (expressed as weight percentages) to production-scale batch weights in any target batch size, with automatic unit conversion.

### Sheet Layout

**Header Section:**

| Field | Input/Calc | Description |
|-------|-----------|-------------|
| Formula Name | Input | Product/formula identifier |
| Formula Version | Input | Matches document control version |
| Lab Batch Size | Input | Size used for formula development (e.g., 10 kg) |
| Production Batch Size | Input | Target production batch size |
| Batch Size Unit | Input | Dropdown: kg, lb, gal, L |
| Density (for volumetric) | Input | g/mL — required when batch size is in gallons or liters |

**Ingredient Table:**

| Column | Type | Description |
|--------|------|-------------|
| A: Ingredient | Input | Ingredient name |
| B: Formula % | Input | Weight percentage in formula (must sum to 100.00%) |
| C: Target Weight (kg) | Formula | `=B*ProductionBatchSize/100` (if batch in kg) |
| D: Target Weight (lb) | Formula | `=C*2.20462` |
| E: Target Weight (gal) | Formula | `=C/(Density*3.78541)` (for liquid ingredients) |
| F: Actual Weight | Input | Operator entry during production |
| G: Variance (%) | Formula | `=ABS(F-C)/C*100` |
| H: Variance Status | Formula | Green <=2%, Yellow 2-5%, Red >5% |
| I: Notes | Input | Lot number, scale ID, operator initials |

**Validation Row:**
- Sum of Formula % must equal 100.00% (conditional format: red if not)
- Sum of Target Weights displayed for verification against batch size
- Water is typically the balancing ingredient — formula may show "water: q.s. to 100%"

### Unit Conversion Reference (Built-in)

| From | To | Factor |
|------|-----|--------|
| kg | lb | x 2.20462 |
| lb | kg | x 0.45359 |
| gal (US) | L | x 3.78541 |
| L | gal (US) | x 0.26417 |
| kg | gal (water) | / 3.78541 |
| Brix to specific gravity | | SG = 1 + (Brix * 0.004) approximately; use lookup table for precision |

### Overage Calculations

For vitamins, minerals, and sensitive ingredients subject to degradation:

| Column | Description |
|--------|-------------|
| Label Claim | Amount per serving on Nutrition Facts label |
| Overage % | Typically 15-30% depending on ingredient stability and shelf life |
| Overage Target | `=LabelClaim * (1 + Overage%/100)` |
| Formula % adjusted | Incorporates overage into the formula percentage |

---

## 3. Nutritional Calculator

### Purpose
Calculates Nutrition Facts panel values from a formula using an ingredient nutrient database. Outputs per-serving nutritional information compliant with FDA 21 CFR 101 labeling requirements.

### Architecture

**Tab 1: Ingredient Database**

| Column | Description |
|--------|-------------|
| Ingredient Code | Internal RM code |
| Ingredient Name | Full name |
| Serving Basis | Per 100g (standard for database) |
| Calories (kcal) | Total calories per 100g |
| Total Fat (g) | |
| Saturated Fat (g) | |
| Trans Fat (g) | |
| Cholesterol (mg) | |
| Sodium (mg) | |
| Total Carbohydrate (g) | |
| Dietary Fiber (g) | |
| Total Sugars (g) | |
| Added Sugars (g) | Requires sourcing distinction — naturally occurring vs added |
| Protein (g) | |
| Vitamin D (mcg) | |
| Calcium (mg) | |
| Iron (mg) | |
| Potassium (mg) | |
| Source | Supplier COA, USDA FoodData Central, analytical testing |
| Last Updated | Date of most recent data verification |

**Tab 2: Formula Input**

| Column | Description |
|--------|-------------|
| Ingredient | Linked to database via VLOOKUP/INDEX-MATCH |
| Formula % | Weight percentage in formula |
| (All nutrient columns) | Auto-calculated: `=FormulaPercent/100 * DatabaseValue` |

**Tab 3: Nutrition Facts Output**

| Field | Calculation | Rounding Rule (21 CFR 101.9) |
|-------|------------|------------------------------|
| Serving Size | Input (e.g., 355 mL / 12 fl oz) | Per RACC table |
| Servings Per Container | Input | Rounded to nearest 0.5 if <2, nearest 1 if 2-5, "about X" if >5 |
| Calories | Sum of (fat*9 + carb*4 + protein*4 + alcohol*7) per serving | Round to nearest 10 if >50, nearest 5 if 5-50, 0 if <5 |
| Total Fat | Sum per serving | Round to nearest 0.5g if <5g, nearest 1g if >=5g |
| Saturated Fat | Sum per serving | Round to nearest 0.5g (0g if <0.5g) |
| Trans Fat | Sum per serving | Round to nearest 0.5g (0g if <0.5g) |
| Cholesterol | Sum per serving | Round to nearest 5mg (0mg if <2mg) |
| Sodium | Sum per serving | Round to nearest 10mg if >140mg, nearest 5mg if 5-140mg |
| Total Carbohydrate | Sum per serving | Round to nearest 1g |
| Dietary Fiber | Sum per serving | Round to nearest 1g |
| Total Sugars | Sum per serving | Round to nearest 1g |
| Added Sugars | Sum per serving | Round to nearest 1g |
| Protein | Sum per serving | Round to nearest 1g |
| Vitamin D | Sum per serving | mcg and %DV |
| Calcium | Sum per serving | mg and %DV |
| Iron | Sum per serving | mg and %DV |
| Potassium | Sum per serving | mg and %DV |

**%DV Calculation:** `=NutrientAmountPerServing / DailyReferenceValue * 100`, rounded to nearest 1%

**Daily Reference Values (2020 FDA):**

| Nutrient | DRV |
|----------|-----|
| Total Fat | 78g |
| Saturated Fat | 20g |
| Cholesterol | 300mg |
| Sodium | 2300mg |
| Total Carbohydrate | 275g |
| Dietary Fiber | 28g |
| Added Sugars | 50g |
| Vitamin D | 20mcg |
| Calcium | 1300mg |
| Iron | 18mg |
| Potassium | 4700mg |

---

## 4. Cost Calculator

### Purpose
Models ingredient cost per batch and per unit at various production volumes, enabling pricing decisions and margin analysis.

### Sheet Structure

**Ingredient Cost Table:**

| Column | Description |
|--------|-------------|
| Ingredient | Name |
| Unit Cost | Cost per purchasing unit ($/lb, $/kg, $/gal) |
| Purchasing Unit | lb, kg, gal, each |
| Usage per Batch (kg) | From batch scaling calculator |
| Cost per Batch | `=UnitCost * UsagePerBatch` (with unit conversion) |
| % of Total Ingredient Cost | `=CostPerBatch / TotalIngredientCost * 100` |

**Batch Cost Summary:**

| Cost Component | Calculation |
|----------------|------------|
| Total Ingredient Cost | Sum of all ingredient costs per batch |
| Packaging Cost | Container + closure + label + secondary packaging per batch |
| Direct Labor | Hours per batch * hourly rate (including burden) |
| Utilities | Estimated per batch (steam, electricity, water, CO2) |
| QC Testing | Cost of in-process and release testing per batch |
| Overhead Allocation | Facility, depreciation, insurance per batch |
| **Total Batch Cost** | Sum of all components |
| **Units per Batch** | Batch volume / unit volume |
| **Cost per Unit** | Total Batch Cost / Units per Batch |

**Volume Sensitivity Table:**

| Production Volume (cases/month) | Ingredient Cost/Unit | Packaging Cost/Unit | Total Cost/Unit | Margin at Retail Price |
|------|------|------|------|------|
| 1,000 | (calc) | (calc) | (calc) | (calc) |
| 5,000 | (calc) | (calc) | (calc) | (calc) |
| 10,000 | (calc) | (calc) | (calc) | (calc) |
| 25,000 | (calc) | (calc) | (calc) | (calc) |
| 50,000 | (calc) | (calc) | (calc) | (calc) |

Volume impacts: ingredient pricing tiers (volume discounts), labor efficiency (setup time amortized), overhead allocation (fixed cost spread).

---

## 5. Label Ingredient Statement Generator

### Purpose
Generates a compliant ingredient statement from a formula, listing ingredients in descending order of predominance with sub-ingredients expanded and allergen declarations per FDA 21 CFR 101.4.

### Input Table

| Column | Description |
|--------|-------------|
| Ingredient (as purchased) | Commercial name (e.g., "Natural Vanilla Flavor") |
| Formula % | Weight percentage in formula |
| Sub-Ingredients | Component ingredients of compound ingredients (e.g., "water, ethanol, vanilla extract") |
| Is Water | Y/N — water is listed by total including water from other ingredients |
| Allergens Present | None, Milk, Soy, Tree Nuts (specify), Wheat, Eggs, Fish, Shellfish, Sesame, Peanuts |
| Organic | Y/N — for organic labeling compliance |

### Output Fields

**Ingredient Statement:**
- Auto-sorted by descending weight percentage
- Sub-ingredients expanded in parentheses for compound ingredients contributing >2% of the formula
- Sub-ingredients of incidental additives (processing aids, insignificant levels) may be omitted per 21 CFR 101.100
- Water positioned based on total water contribution (free water + water from juices, extracts, etc.)
- Common/usual names used per 21 CFR 101.4 (e.g., "sugar" not "sucrose", "water" not "purified water" unless claim-relevant)

**Allergen Contains Statement:**
- Format: "Contains: [allergen list]"
- All major allergens present anywhere in the formula listed alphabetically
- Includes allergens from sub-ingredients
- Precautionary statements ("May contain...") handled separately — based on facility allergen assessment, not formula

**Example Output:**
```
INGREDIENTS: FILTERED WATER, ORGANIC CANE SUGAR, ORGANIC LEMON JUICE
CONCENTRATE (ORGANIC LEMON JUICE, ORGANIC LEMON OIL), CITRIC ACID,
NATURAL FLAVORS, ASCORBIC ACID (VITAMIN C), ORGANIC STEVIA LEAF
EXTRACT.
```

---

## 6. Shelf Life Tracking Sheet

### Purpose
Tracks real-time and accelerated shelf life studies for products in development and production, recording pull dates, test results, and predicted vs actual shelf life.

### Study Setup

| Field | Description |
|-------|-------------|
| Study ID | SLS-YYYY-### |
| Product | Product name and formula version |
| Batch/Lot | Production lot under study |
| Production Date | Date of manufacture |
| Study Type | Real-Time (ambient, refrigerated) or Accelerated |
| Storage Conditions | Temperature and humidity (e.g., 25C/60% RH, 38C/75% RH, 4C) |
| Target Shelf Life | Number of months (e.g., 12 months, 18 months) |
| Pull Schedule | Monthly, bi-monthly, quarterly — dates pre-populated |

### Pull Date Testing Log

| Column | Description |
|--------|-------------|
| Pull Date | Scheduled sampling date |
| Actual Pull Date | When sample was actually pulled |
| Age (days) | Auto-calculated from production date |
| Brix | Measured value |
| pH | Measured value |
| Color (L*a*b*) | Spectrophotometer readings |
| Titratable Acidity | % as citric acid |
| Micro — APC | CFU/mL (aerobic plate count) |
| Micro — Y&M | CFU/mL (yeast and mold) |
| Micro — Coliform | CFU/mL |
| Sensory Score | Overall acceptability (1-9 hedonic scale or pass/fail) |
| Visual Appearance | Pass/fail with notes (sedimentation, color change, clarity) |
| Package Integrity | Pass/fail (seal strength, headspace gas, vacuum) |
| Overall Status | Pass/Marginal/Fail |
| Notes | Observations, deviations |

### Shelf Life Prediction

- Accelerated study results at 38C used to predict real-time shelf life using Q10 factor (typically Q10 = 2-3 for chemical degradation in beverages)
- `Predicted Real-Time Shelf Life = Accelerated Shelf Life * Q10^((T_accelerated - T_storage)/10)`
- Graph: parameter trending over time with specification limits overlaid
- Automatic alert when any parameter reaches 80% of its specification limit

---

## 7. Sweetener Equivalency Calculator

### Purpose
Calculates equivalent sweetness levels when substituting alternative sweeteners for sucrose, optimizing blends for taste and cost.

### Sweetener Database

| Sweetener | Relative Sweetness (vs sucrose = 1.0) | Caloric Value (kcal/g) | Max Usage (FDA) | Typical Use Level | Cost Index (vs sucrose) |
|-----------|---------------------------------------|----------------------|----------------|-------------------|------------------------|
| Sucrose | 1.0 | 4.0 | GMP | 8-12% in beverages | 1.0 |
| HFCS 55 | 1.0 | 3.0 | GMP | 8-12% | 0.7 |
| Stevia (Reb A 95%) | 200-300 | 0 | GMP (GRAS) | 0.02-0.04% | 25-40 |
| Stevia (Reb M) | 200-350 | 0 | GMP (GRAS) | 0.015-0.035% | 50-80 |
| Monk Fruit (Luo Han Guo) | 150-300 | 0 | GMP (GRAS) | 0.02-0.05% | 40-60 |
| Erythritol | 0.6-0.7 | 0.2 | GMP (GRAS) | 2-5% | 3-5 |
| Allulose | 0.7 | 0.2-0.4 | GMP (GRAS) | 3-8% | 4-6 |
| Sucralose | 600 | 0 | 5 mg/kg bw/day ADI | 0.01-0.02% | 15-25 |
| Aspartame | 200 | 4.0 (negligible at use level) | 50 mg/kg bw/day ADI | 0.04-0.06% | 8-12 |
| Acesulfame K | 200 | 0 | 15 mg/kg bw/day ADI | 0.02-0.04% | 10-15 |

### Calculator Input/Output

**Input:**
- Target sweetness equivalent (in % sucrose equivalency, e.g., "10% SE" = sweetness of a 10% sucrose solution)
- Selected sweetener(s) for the blend
- Blend ratio (if using multiple sweeteners)
- Batch size

**Output:**
- Required weight of each sweetener per batch
- Caloric contribution per serving
- Cost per batch and per unit
- Regulatory compliance check (usage level vs maximum permitted)
- Label declaration guidance (ingredient name for label)

### Blend Optimization Notes

- High-intensity sweeteners (stevia, monk fruit, sucralose) benefit from bulking agents (erythritol, allulose) for mouthfeel
- Stevia Reb A at >0.03% can show bitter aftertaste; blend with Reb M or monk fruit to improve profile
- Erythritol above 4% may cause cooling sensation; keep below 3% in most beverages
- Allulose contributes to Maillard browning in thermally processed products — consider for hot-fill
- Sucralose is heat-stable; preferred for pasteurized/retorted products among artificial options

---

## 8. pH/Buffer Calculator

### Purpose
Estimates the amount of acid required to reach a target pH, considering the buffering capacity of the beverage matrix. Critical for acidified foods (21 CFR 114) where pH <= 4.6 is a food safety requirement.

### Input Fields

| Field | Description |
|-------|-------------|
| Current pH | Measured pH of the unbuffered or partially acidified batch |
| Target pH | Desired final pH (e.g., 3.4 for an acidified beverage) |
| Acid Type | Citric, Phosphoric, Malic, Lactic, Tartaric, Ascorbic |
| Acid Concentration | % w/w of acid solution being added (e.g., 50% citric acid solution) |
| Batch Volume (L) | Total batch volume |
| Estimated Buffer Capacity | Low (water-based), Medium (juice blend), High (dairy/protein) |

### Output

- Estimated acid addition volume (mL or L)
- This is an **estimate only** — actual pH must be measured and adjusted
- Recommendation: add 80% of calculated amount, mix, measure pH, titrate remainder
- Warning flag if target pH is near 4.6 (food safety critical limit) — recommend targeting 4.2 or below with process authority validation

### Acid pKa Reference

| Acid | pKa1 | pKa2 | pKa3 | Flavor Profile |
|------|-------|-------|-------|---------------|
| Citric | 3.13 | 4.76 | 6.40 | Bright, clean sour |
| Phosphoric | 2.15 | 7.20 | 12.35 | Sharp, cola-type acidity |
| Malic | 3.40 | 5.11 | — | Smooth, apple-like sour |
| Lactic | 3.86 | — | — | Mild, tangy |
| Tartaric | 2.98 | 4.34 | — | Sharp, grape-like |
| Ascorbic | 4.10 | 11.6 | — | Mild acid, vitamin C function |

---

## 9. Carbonation Volume Calculator

### Purpose
Calculates dissolved CO2 volumes from temperature and pressure using Henry's Law, or determines required pressure to achieve target carbonation at a given temperature.

### Henry's Law Application

CO2 solubility in water follows: `C = kH * P`

Where:
- C = concentration of dissolved CO2
- kH = Henry's law constant (temperature-dependent)
- P = partial pressure of CO2

### Calculator Modes

**Mode 1: Given Temperature + Pressure, Calculate CO2 Volumes**
- Input: product temperature (F or C), applied CO2 pressure (psi or bar)
- Output: dissolved CO2 in volumes (1 volume = 1 L CO2 gas per 1 L liquid at STP)

**Mode 2: Given Temperature + Target Volumes, Calculate Required Pressure**
- Input: product temperature, target CO2 volumes
- Output: required CO2 pressure

**Mode 3: Given Pressure + Target Volumes, Calculate Required Temperature**
- Input: applied pressure, target CO2 volumes
- Output: required product temperature (for setting carbonator chiller)

### Reference Table (CO2 Volumes at Various Temp/Pressure Combinations)

| Temp (F) | 10 psi | 15 psi | 20 psi | 25 psi | 30 psi |
|----------|--------|--------|--------|--------|--------|
| 32 | 2.48 | 3.15 | 3.81 | 4.48 | 5.14 |
| 34 | 2.38 | 3.02 | 3.65 | 4.29 | 4.93 |
| 36 | 2.28 | 2.89 | 3.51 | 4.12 | 4.73 |
| 38 | 2.18 | 2.77 | 3.36 | 3.95 | 4.54 |
| 40 | 2.09 | 2.66 | 3.22 | 3.79 | 4.35 |

### Typical CO2 Volume Targets by Product

| Product | Target Volumes | Tolerance |
|---------|---------------|-----------|
| Still water (slightly carbonated) | 1.0-1.5 | +/- 0.2 |
| Sparkling water | 3.0-4.0 | +/- 0.3 |
| Cola-type CSD | 3.5-4.0 | +/- 0.2 |
| Lemon-lime CSD | 3.5-4.2 | +/- 0.2 |
| Kombucha | 2.0-3.0 | +/- 0.3 |
| Hard seltzer | 2.5-3.0 | +/- 0.2 |
| Sparkling juice | 2.5-3.5 | +/- 0.3 |
| Energy drink | 2.0-3.0 | +/- 0.2 |
| Beer (lager) | 2.4-2.8 | +/- 0.2 |
| Beer (ale) | 2.0-2.6 | +/- 0.2 |
| Nitro cold brew | 0.8-1.2 CO2 + N2 | +/- 0.2 |

### Process Notes

- Product must be chilled to 32-38F for efficient carbonation; warmer product requires significantly higher pressure
- De-aeration before carbonation improves CO2 absorption and reduces foaming
- Dissolved oxygen should be <1 ppm before carbonation (O2 competes for solubility and causes oxidation)
- In-line carbonation preferred over tank carbonation for consistency
- Verify carbonation with Zahm & Nagel shaker or in-line CO2 sensor at filler bowl
- Over-carbonation causes foaming at filler, under-fill, and cap/lid blowoffs
- Under-carbonation results in flat product and customer complaints

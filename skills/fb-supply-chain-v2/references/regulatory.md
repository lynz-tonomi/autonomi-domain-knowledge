# Regulatory Touchpoints — Deep Reference

## 9.1 FSMA 204 Traceability

### Critical Tracking Events (CTEs)

Every food in the Food Traceability List (FTL) must record these CTEs:

```
CTE 1: RECEIVING (ingredient receipt at facility)
CTE 2: TRANSFORMATION (ingredient becomes finished product)
CTE 3: SHIPPING (finished product leaves facility)
```

### Key Data Elements (KDEs) per CTE

**Receiving KDEs:**

| KDE | Description | Example |
|-----|-------------|---------|
| Traceability lot code | Lot identifier assigned by source | LOT-2026-03-001 |
| Quantity and UOM | Amount received | 5,000 lbs |
| Location received (GLN) | Global Location Number of receiving facility | 0012345000010 |
| Date received | Calendar date | 2026-03-15 |
| Supplier info | Name and GLN | "Acme Ingredients" / 0098765000020 |
| Reference document | PO number, BOL | PO-20260315-001, BOL-78234 |

**Transformation KDEs:**

| KDE | Description | Example |
|-----|-------------|---------|
| Input traceability lot codes | All ingredient lots consumed | [LOT-A, LOT-B, LOT-C] |
| Output traceability lot code | Finished good lot code | FG-20260316-L2-001 |
| Quantity transformed | Input and output quantities | In: 10,000 lbs → Out: 9,500 lbs |
| Location (GLN) | Facility where transformation occurred | 0012345000010 |
| Date of transformation | Calendar date | 2026-03-16 |
| Reference document | Batch record number | BR-20260316-001 |

**Shipping KDEs:**

| KDE | Description | Example |
|-----|-------------|---------|
| Traceability lot code | Finished good lot | FG-20260316-L2-001 |
| Quantity and UOM | Cases shipped | 1,200 cases |
| Location shipped from (GLN) | Shipping facility | 0012345000010 |
| Location shipped to (GLN) | Customer facility | 0056789000030 |
| Date shipped | Calendar date | 2026-03-18 |
| Reference document | BOL, invoice | BOL-78300, INV-45678 |

### Food Traceability List (FTL) Applicability

```
PRODUCTS REQUIRING FSMA 204 RECORDS:
  Fresh fruits and vegetables (many — check FDA FTL)
  Shell eggs
  Nut butters
  Fresh herbs
  Certain cheeses
  Ready-to-eat deli salads
  Finfish, crustaceans, mollusks

MOST SHELF-STABLE BEVERAGES ARE NOT ON THE FTL AS OF 2026.

EXCEPTIONS THAT MAY APPLY:
  - Fresh juice (not pasteurized) — check FTL
  - Smoothies with fresh fruit components — check FTL
  - Products containing fresh-cut fruit/vegetables — check FTL

→ Always check current FTL at FDA.gov — it is subject to update.
→ Even if not on FTL, maintaining 204-level traceability is best practice.
```

## 9.2 Lot-Level Traceability

### Trace-Forward (Ingredient → Finished Product → Customer)

```
TRACE-FORWARD QUERY:
  Given: ingredient lot X
  Step 1: Find all batch_ids that consumed lot X
    → JOIN ingredient_lot_usage ON lot_number = X
  Step 2: Find all finished good lots produced from those batches
    → JOIN batch_output ON batch_id
  Step 3: Find all shipments containing those finished good lots
    → JOIN shipment_detail ON fg_lot_number
  Step 4: Find all customers who received those shipments
    → JOIN shipment_header ON shipment_id
  → RESULT: complete distribution list for recall scoping
```

### Trace-Back (Finished Product → Ingredients → Supplier)

```
TRACE-BACK QUERY:
  Given: finished good lot Y
  Step 1: Find batch_id that produced lot Y
    → JOIN batch_output ON fg_lot_number = Y
  Step 2: Find all ingredient lots consumed in that batch
    → JOIN ingredient_lot_usage ON batch_id
  Step 3: Find all suppliers who provided those ingredient lots
    → JOIN receiving_records ON lot_number
  Step 4: Find all OTHER batches that used the same ingredient lots
    → JOIN ingredient_lot_usage ON lot_number (all batches)
  → RESULT: identify root cause supplier/lot + full exposure scope
```

### Mock Recall Requirements

```
FREQUENCY: at least 1 mock recall per year (more if required by GFSI scheme)

PERFORMANCE TARGETS:
  Trace-forward: complete in < 4 hours
  Trace-back: complete in < 4 hours
  Account for ≥ 100% of product (all units accounted for)
  Accuracy: ≥ 95% of records match physical investigation

DOCUMENT:
  Mock recall report with: scope, time to complete, accuracy,
  gaps identified, corrective actions planned
  → Feed gaps into CAPA system
```

## 9.3 FDA Registration & Process Filing

### Facility Registration

```
REQUIREMENT:
  All food manufacturing facilities must register with FDA (21 CFR 1.225)
  Biennial renewal: even-numbered years, Oct–Dec
  Registration number required for all FDA interactions
  Must designate US Agent if foreign facility

EVENTS REQUIRING UPDATE:
  - Facility name change
  - Address change
  - Owner/operator change
  - Activity type change (add/remove food categories)
  → Update within 60 days of change
```

### Scheduled Process Filing (21 CFR 113/114)

```
REQUIRED FOR:
  Low-acid canned foods (LACF):
    pH > 4.6 AND aw > 0.85
    Filed under 21 CFR 113
    Requires thermal process (retort) to achieve commercial sterility

  Acidified foods:
    Natural pH > 4.6, acidified to pH ≤ 4.6 by addition of acid
    Filed under 21 CFR 114
    Requires equilibrium pH monitoring + scheduled process

FILING PROCESS:
  1. Engage recognized Process Authority (university or consulting firm)
  2. Process Authority develops scheduled process:
     - Time, temperature, container size, product formulation
     - Validated by inoculated pack study or heat penetration study
  3. File with FDA via FCE (Food Canning Establishment) number
     - Form FDA 2541 (food process filing)
  4. Receive SID (Submission Identifier) confirmation

CHANGE MANAGEMENT:
  Any change to the following requires re-filing:
    - Container size or type
    - Product formulation (ingredients that affect pH or heat penetration)
    - Retort type or configuration
    - Process time or temperature
    - Fill weight or headspace
```

### Exemptions

```
EXEMPT FROM SCHEDULED PROCESS FILING:
  - Beverages at natural pH ≤ 4.6 (most fruit juices, kombucha)
    → These are naturally acid foods, not "acidified"
  - Beverages with aw ≤ 0.85 (very concentrated products)
  - Alcoholic beverages (regulated by TTB, not FDA)
  - Carbonated beverages in hermetically sealed containers (pH ≤ 4.6)
  - Fermented foods where fermentation naturally produces acid (pH ≤ 4.6)

GRAY AREAS — CONSULT PROCESS AUTHORITY:
  - Oat milk (pH ~6.5–7.0) → if retorted or aseptically processed, LACF rules apply
  - Functional drinks with added protein → may raise pH above 4.6
  - Cold brew coffee (pH ~4.8–5.5) → if shelf-stable, may need LACF filing
```

## 9.4 Labeling Regulatory Requirements

```
REQUIRED LABEL ELEMENTS (FDA):
  1. Statement of identity (product name)
  2. Net quantity of contents
  3. Nutrition Facts panel (21 CFR 101.9)
  4. Ingredient list (descending order by weight)
  5. Allergen declaration ("Contains: ...")
  6. Name and address of manufacturer, packer, or distributor
  7. Country of origin (if imported)

COMMON CLAIMS AND THEIR REQUIREMENTS:
  "Organic":
    → USDA NOP certification required
    → "100% organic": all ingredients organic
    → "Organic": ≥95% organic ingredients
    → "Made with organic [ingredient]": ≥70% organic
  "Non-GMO":
    → Non-GMO Project Verified is dominant third-party cert
  "Gluten-free":
    → <20 ppm gluten (FDA rule, 21 CFR 101.91)
  "Natural":
    → FDA has no formal definition
    → Generally: no artificial ingredients/colors, minimally processed
  "No added sugar":
    → No sugars or ingredients containing sugars added during processing
  "Low calorie":
    → ≤40 calories per RACC (reference amount customarily consumed)
  "Excellent source of [vitamin]":
    → ≥20% DV per RACC
  "Good source of [vitamin]":
    → 10–19% DV per RACC
```

## 9.5 Failure Modes

| Failure | Detection | Action |
|---------|-----------|--------|
| Traceability gap (cannot link ingredient to batch) | Mock recall or actual recall | CAPA, fix data capture at receiving/production |
| Scheduled process not filed for acidified product | Regulatory review or FDA inspection | STOP production, engage process authority, file immediately |
| Label claim unsupported | Regulatory audit or customer complaint | Assess: reformulate, change label, or withdraw claim |
| Biennial registration lapsed | Calendar reminder | Renew immediately — lapsed registration = noncompliant |
| Process deviation without PA notification | Internal audit | Notify process authority retroactively, hold all affected product |
| Allergen undeclared on label | Customer report or internal review | Assess recall scope, correct label, notify FDA if distributed |

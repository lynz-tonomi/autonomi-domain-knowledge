# COGS & Batch Costing for Beverage Manufacturing

## Overview

Batch costing is the primary cost accounting method for beverage manufacturing. Each production run (batch) is a discrete cost object that accumulates ingredient, packaging, labor, and overhead costs. This document covers BOM cost rollup, co-packing fee structures, landed cost calculation, standard vs. actual cost variance analysis, and QBO journal entry patterns for the full production cycle.

---

## 1. Bill of Materials (BOM) Cost Rollup

### BOM Structure for a Typical Beverage

A BOM defines every input required to produce one finished unit (or one batch). For beverage, the BOM is hierarchical:

**Level 0 — Finished Good** (e.g., 12oz can of Sparkling Lemon Water, case of 12)
- **Level 1 — Liquid Formulation** (per gallon of finished beverage)
  - Water (purified/RO) — $0.002/gallon
  - Lemon juice concentrate (65 Brix) — $8.50/gallon, usage 0.03 gal per finished gal = $0.255
  - Citric acid — $1.80/lb, usage 0.008 lb/gal = $0.014
  - Natural lemon flavor — $45.00/lb, usage 0.002 lb/gal = $0.090
  - Stevia extract (Reb M) — $120.00/lb, usage 0.0005 lb/gal = $0.060
  - Ascorbic acid (Vitamin C) — $8.00/lb, usage 0.001 lb/gal = $0.008
  - CO2 carbonation — $0.15/gallon of finished product
  - **Total liquid cost per gallon: $0.579**
  - Gallon yields ~10.67 cans (12oz each) = **$0.054 liquid cost per can**

- **Level 1 — Packaging**
  - 12oz sleek aluminum can (printed) — $0.085/can
  - Can end (lid) — $0.025/can
  - Hi-cone carrier or paperboard clip (6-pack) — $0.03/can equivalent
  - Corrugated case (holds 24 cans, 4x6-packs) — $0.55/case = $0.023/can
  - Pallet + stretch wrap + tier sheet — $12.00/pallet / 100 cases / 24 cans = $0.005/can
  - **Total packaging cost per can: $0.168**

- **Level 1 — Co-Packing**
  - Toll fee: $0.08/can
  - Allocated setup/changeover: $2,500 per run / 50,000 cans = $0.05/can (at minimum run)
  - Allocated setup/changeover: $2,500 per run / 200,000 cans = $0.0125/can (at scale)
  - **Co-pack cost per can: $0.093 (at min) to $0.130 (at min) — $0.093 (at scale 200K)**

Wait — let me recalculate cleanly:

### Cost Per Can at Different Production Volumes

| Cost Component | 50,000 cans | 100,000 cans | 200,000 cans | 500,000 cans |
|---------------|-------------|--------------|--------------|--------------|
| Liquid ingredients | $0.054 | $0.054 | $0.052 | $0.048 |
| Packaging | $0.168 | $0.162 | $0.155 | $0.145 |
| Co-pack toll fee | $0.080 | $0.080 | $0.075 | $0.065 |
| Setup/changeover | $0.050 | $0.025 | $0.013 | $0.005 |
| Yield loss (3%) | $0.011 | $0.010 | $0.009 | $0.008 |
| **Total COGS/can** | **$0.363** | **$0.331** | **$0.304** | **$0.271** |
| **COGS/case (24ct)** | **$8.71** | **$7.94** | **$7.30** | **$6.50** |

Notes on volume pricing:
- Ingredient costs decrease slightly at volume due to bulk purchasing (drums vs. pails)
- Can pricing drops 5-10% at 1M+ annual volume commitments
- Co-pack toll fees are negotiable with volume commitments (annual contracts)
- Setup cost amortization is the single biggest driver of unit cost reduction at low volumes

---

## 2. Co-Packing Fee Structures

### Per-Unit Toll Fee
The base manufacturing fee charged per finished unit. Includes line operation, labor, utilities, QC sampling.
- **Canning line (12oz)**: $0.06-$0.12/can depending on volume, line speed, and region
- **Glass bottling (12-16oz)**: $0.10-$0.18/bottle (slower line speed, more handling)
- **PET bottling (16-32oz)**: $0.08-$0.15/bottle
- **Aseptic (shelf-stable)**: $0.15-$0.30/unit (higher due to sterilization process)
- **HPP processing (cold-pressed)**: $0.08-$0.12/bottle additional HPP toll

### Setup & Changeover Fees
Charged per production run for line preparation, CIP (clean-in-place), flavor changeover.
- **Simple changeover** (same product, different flavor): $1,500-$3,000
- **Full changeover** (different product type, allergen clean): $3,000-$7,500
- **Organic changeover** (requires certified organic flush): $2,000-$5,000 premium
- **Kosher run** (mashgiach supervision): $500-$1,500 per run additional

### Minimum Run Charges
Co-packers set minimum batch sizes to justify line startup.
- **Canning**: Typically 100-200 cases minimum (2,400-4,800 cans)
- **Small/craft co-packer**: May accept 50-case minimums at premium pricing
- **Large co-packer**: 500+ case minimums, better pricing
- If batch falls below minimum, a flat minimum charge applies (e.g., $5,000 minimum per run)

### Overrun/Underrun Tolerances
- Industry standard: **plus or minus 10%** of ordered quantity
- Brand must accept and pay for overrun within tolerance
- Underrun within tolerance is accepted; co-packer not penalized
- Beyond tolerance: negotiated case-by-case (ingredient availability, can supply issues)
- QBO treatment: adjust finished goods inventory and COGS for actual quantity produced

---

## 3. Landed Cost Calculation

Landed cost captures the full cost to get ingredients or finished goods to the point of use or sale.

### Formula
```
Landed Cost = Purchase Price + Inbound Freight + Duties/Tariffs + Insurance + Warehouse Receiving
```

### Example: Imported Coconut Water Concentrate
```
Purchase price (CIF port):        $3,200 per MT (metric ton)
Ocean freight:                    $480 per MT (15% of product cost)
Import duty (HTS 2009.89):       $160 per MT (5% ad valorem)
Customs broker fee:               $85 per MT (allocated)
Inland freight (port to warehouse): $120 per MT
Warehouse receiving & QC:         $45 per MT
Insurance (marine cargo):         $16 per MT (0.5% of CIF value)
-------------------------------------------------------
Landed Cost:                      $4,106 per MT
                                  = $1.86 per lb
                                  = $0.186 per gallon at 10% usage rate
```

### Domestic Ingredient Example: Organic Cane Sugar
```
Purchase price (FOB supplier):    $0.45/lb
Freight (full truckload, 42K lbs): $3,200 / 42,000 = $0.076/lb
Warehouse receiving:              $0.01/lb
-------------------------------------------------------
Landed Cost:                      $0.536/lb
```

### Landed Cost in QBO
- Record purchase at base price to vendor via Bill
- Allocate freight to inventory via separate Journal Entry or landed cost allocation
- QBO does not natively support landed cost allocation — use Journal Entry:
  - Dr. 1200 Inventory — Raw Materials (freight allocation)
  - Cr. 5300 COGS — Inbound Freight (reclassify from expense to inventory)
- Alternative: some F&B companies expense inbound freight directly to COGS (simpler, less accurate)

---

## 4. Standard Cost vs. Actual Cost Variance Analysis

### Standard Cost Setting
Standard costs are established annually (during budgeting) or quarterly for volatile ingredients.

**Components of standard cost per unit:**
| Component | Standard | Source |
|-----------|----------|--------|
| Ingredients | $0.054/can | BOM × budgeted ingredient prices |
| Packaging | $0.160/can | BOM × contracted packaging prices |
| Co-pack toll | $0.080/can | Contract rate |
| Co-pack setup | $0.015/can | Budgeted annual setup cost / budgeted volume |
| Inbound freight | $0.012/can | Budgeted freight / budgeted volume |
| Warehouse | $0.008/can | Budgeted storage + handling / budgeted volume |
| **Total standard cost** | **$0.329/can** | |

### Variance Categories

**Price Variance (Purchase Price Variance — PPV)**
```
PPV = (Actual Price - Standard Price) x Actual Quantity
```
- Tracks ingredient cost fluctuations (coffee futures, sugar prices, aluminum LME)
- Favorable when actual price < standard; unfavorable when actual > standard
- F&B-specific: commodity hedging can reduce PPV; seasonal produce has predictable spikes

**Usage Variance (Material Usage Variance — MUV)**
```
MUV = (Actual Quantity Used - Standard Quantity Allowed) x Standard Price
```
- Tracks formulation efficiency — are we using more ingredient than the BOM specifies?
- Common causes: inaccurate batching scales, recipe deviations, concentrate Brix variation
- Target: within ±2% of standard usage

**Yield Variance**
```
Yield Variance = (Actual Output - Expected Output) x Standard Cost per Unit
```
- Expected output = input volume x standard yield rate (e.g., 97% for canning)
- Loss factors by process:
  - **Beverage filling**: 1-3% (spillage, foam-over, underfills discarded)
  - **Glass bottling**: 2-5% (breakage + filling loss)
  - **HPP processing**: 1-2% (compression loss, seal failures)
  - **Hot fill**: 2-4% (thermal expansion waste, seal rejects)
  - **Aseptic**: 3-7% (sterilization losses, startup/shutdown waste)

**Co-Pack Rate Variance**
```
Rate Variance = (Actual Co-Pack Rate - Standard Rate) x Actual Units
```
- Tracks contract vs. actual charges (overtime premiums, rush fees, rework charges)

### Monthly Variance Journal Entries
```
Unfavorable Price Variance:
  Dr. 5700 COGS — Price Variance         $2,400
    Cr. 1200 Inventory — Raw Materials              $2,400

Favorable Usage Variance:
  Dr. 1200 Inventory — Raw Materials      $800
    Cr. 5710 COGS — Usage Variance                  $800

Yield Loss:
  Dr. 5600 COGS — Shrink & Waste          $1,150
    Cr. 1220 Inventory — WIP                        $1,150
```

---

## 5. QBO Inventory Valuation Methods

### FIFO (First In, First Out) — Recommended for F&B
- Matches physical flow of perishable goods (FEFO in warehouse aligns with FIFO in accounting)
- COGS reflects oldest costs first — important when ingredient prices are rising
- Ending inventory reflects most recent costs — better balance sheet accuracy
- QBO Advanced supports FIFO natively for inventory items
- **Required for tax purposes if using LIFO for any items (IRS conformity rule does not apply to FIFO)**

### Weighted Average
- QBO Simple/Essentials default method
- Each purchase recalculates the average cost of all units on hand
- Simpler to maintain but less accurate for perishable goods with price volatility
- Acceptable for companies with stable ingredient costs and high inventory turns

### Practical Guidance
- Use FIFO for all finished goods and ingredients with meaningful price variation
- Weighted average is acceptable for packaging components (stable pricing, long shelf life)
- Never use LIFO in QBO (not supported; also not recommended for F&B due to perishability)

---

## 6. Journal Entry Patterns for Production

### Batch Start — Raw Material Issuance
When ingredients and packaging are issued from raw material inventory to production:
```
Dr. 1220 Inventory — Work-in-Process       $15,200
  Cr. 1200 Inventory — Raw Materials, Ingredients    $8,400
  Cr. 1210 Inventory — Raw Materials, Packaging      $6,800
Memo: Batch #2024-0847, Sparkling Lemon 12oz, 100,000 cans
```

### During Production — Co-Pack Fee Accrual
When co-packer completes the run (invoice may come later):
```
Dr. 1220 Inventory — Work-in-Process       $10,500
  Cr. 2000 Accounts Payable — Co-Packer             $10,500
Memo: Batch #2024-0847, toll fee 100,000 x $0.08 + setup $2,500
```

### Batch Completion — Transfer to Finished Goods
When batch passes QC and is released to finished goods:
```
Dr. 1230 Inventory — Finished Goods        $24,850
Dr. 5600 COGS — Shrink & Waste             $850
  Cr. 1220 Inventory — Work-in-Process              $25,700
Memo: Batch #2024-0847 complete. 97,200 cans released (2.8% yield loss).
      FG unit cost: $0.2556/can, $6.13/case
```

### Sale — COGS Recognition
When product ships to customer:
```
Dr. 5000-5600 COGS (various)               $6,130
  Cr. 1230 Inventory — Finished Goods               $6,130
Memo: Invoice #INV-4521, 1,000 cases Sparkling Lemon shipped to UNFI
```

### Month-End — Standard to Actual Adjustment
```
Dr. 5700 COGS — Cost Variance              $1,200
  Cr. 1230 Inventory — Finished Goods               $1,200
Memo: October standard-to-actual adjustment.
      Actual COGS $0.263/can vs standard $0.250/can.
      Variance driven by lemon concentrate price increase.
```

---

## 7. Scrap and Waste Accounting

### Types of Production Waste in Beverage
1. **Fill waste**: Liquid lost during filling (foam, spillage, underfills) — 1-3%
2. **Packaging waste**: Damaged cans/bottles, mislabeled units, dented cases — 0.5-2%
3. **QC rejects**: Units failing quality checks (Brix, pH, carbonation level, micro) — 0.5-1%
4. **Startup/shutdown waste**: Product produced before/after line reaches spec — 0.5-1%
5. **Changeover waste**: Product lost during flavor transition — varies by co-packer

### Waste Factor in Standard Cost
Build a standard waste factor into the BOM:
```
Standard yield: 97% (i.e., 3% waste factor)
To produce 100,000 good cans, batch 103,093 cans worth of materials
Waste cost = 3,093 cans x $0.222 material cost = $687 waste per batch
```

### Abnormal vs. Normal Waste
- **Normal waste** (within standard yield factor): included in product cost, flows through WIP
- **Abnormal waste** (above standard): expensed immediately to 5600 COGS — Shrink & Waste
- Threshold for abnormal: any batch with yield loss >2x standard waste factor triggers investigation
- Root cause categories: equipment malfunction, ingredient defect, operator error, recipe error

### QBO Treatment
- Normal waste: absorbed into finished goods cost (no separate entry needed)
- Abnormal waste: separate Journal Entry at time of identification
- Expired inventory: monthly review, write-off via Journal Entry
  ```
  Dr. 5610 COGS — Expired Product Write-Off    $3,400
    Cr. 1230 Inventory — Finished Goods                  $3,400
  Memo: 554 cases Kombucha Ginger expired 10/15/2024. Lot #K-2024-0612.
  ```

---

## 8. Economies of Scale Modeling

### Volume-Cost Relationship
```
Annual Volume    | COGS/Can | COGS/Case(24) | Gross Margin (at $2.24 FOB)
50,000 cases     | $0.363   | $8.71         | -$6.47/case (NEGATIVE — below break-even)
100,000 cases    | $0.331   | $7.94         | -$5.70/case (still negative with full cost load)
250,000 cases    | $0.310   | $7.44         | 47% at net revenue
500,000 cases    | $0.285   | $6.84         | 52% at net revenue
1,000,000 cases  | $0.271   | $6.50         | 55% at net revenue
```

Note: Gross margin above is on net revenue (after trade spend and distributor margin). The table illustrates why emerging F&B brands are often unprofitable at low volumes — fixed cost absorption (setup fees, minimum runs) dominates unit economics until ~200,000+ cases annually.

### Key Scale Inflection Points
- **50K cases**: Can negotiate basic volume pricing on cans; still paying high setup allocation
- **100K cases**: Qualify for mid-tier co-packer pricing; can buy ingredients in drum quantities
- **250K cases**: Unlock annual can contracts with 5-8% savings; dedicated production slots
- **500K cases**: Major co-packer pricing tiers; bulk ingredient contracts; dedicated line time
- **1M+ cases**: Can justify captive manufacturing exploration; vertical integration ROI analysis

---

## 9. Cost Accounting Calendar

### Monthly Procedures
1. **Week 1**: Receive and code all co-packer invoices from prior month production
2. **Week 1**: Reconcile raw material inventory (book vs. co-packer consumption reports)
3. **Week 2**: Calculate actual batch costs for all completed batches
4. **Week 2**: Run standard-to-actual variance analysis
5. **Week 3**: Post inventory adjustments (shrink, damage, expiration)
6. **Week 3**: Post variance journal entries
7. **Week 4**: Review COGS as % of net revenue; flag anomalies

### Quarterly Procedures
1. Review and update standard costs for next quarter (if significant price changes)
2. Physical inventory count reconciliation (full count or cycle count)
3. Obsolescence reserve assessment (slow-moving inventory >90 days, approaching best-by)
4. Co-packer rate review and renegotiation if volume warrants

### Annual Procedures
1. Full standard cost reset aligned with annual budget
2. BOM review and update (reformulations, packaging changes, new suppliers)
3. Inventory valuation audit (FIFO layer verification)
4. 1099 reporting for co-packers and contract manufacturers

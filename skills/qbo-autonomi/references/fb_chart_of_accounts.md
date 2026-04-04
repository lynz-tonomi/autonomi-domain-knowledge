# F&B Chart of Accounts — QBO Structure for Autonomi

## Overview

This chart of accounts is designed for a food and beverage manufacturer/brand selling through retail, DTC, foodservice, and private label channels. It supports SKU-level contribution margin analysis, channel profitability reporting, and GAAP-compliant financial statements. QBO class tracking is used for product line segmentation; location tracking is used for channel or entity segmentation.

---

## 1. Revenue Accounts (4000 Series)

### Revenue by Channel
| Account # | Account Name | Type | Sub-Type | Notes |
|-----------|-------------|------|----------|-------|
| 4000 | Revenue — Retail | Income | Sales of Product | Grocery, mass, natural, convenience |
| 4010 | Revenue — DTC / eCommerce | Income | Sales of Product | Shopify, Amazon Seller, own website |
| 4020 | Revenue — Foodservice | Income | Sales of Product | Restaurants, cafes, catering, institutions |
| 4030 | Revenue — Private Label | Income | Sales of Product | White-label/co-manufacturing for other brands |
| 4040 | Revenue — Club/Wholesale | Income | Sales of Product | Costco, Sam's, BJ's — separate due to margin profile |
| 4050 | Revenue — International | Income | Sales of Product | Export sales, typically through distributors |

### Revenue Adjustments (Contra-Revenue)
| Account # | Account Name | Type | Notes |
|-----------|-------------|------|-------|
| 4100 | Trade Spend — Scan-Backs | Income (contra) | Per-unit rebate triggered at POS scan |
| 4110 | Trade Spend — MCBs (Manufacturer Chargebacks) | Income (contra) | Distributor-funded price reductions |
| 4120 | Trade Spend — OI (Off-Invoice) | Income (contra) | Immediate discount on invoice |
| 4130 | Trade Spend — Slotting Fees | Income (contra) | Shelf placement fees to retailers |
| 4140 | Trade Spend — Billbacks | Income (contra) | Retroactive promotional allowances |
| 4150 | Trade Spend — Free Fills | Income (contra) | Free product for new item placement |
| 4160 | Returns & Allowances | Income (contra) | Customer returns, damage allowances, short-ship credits |
| 4170 | Early Payment Discounts Given | Income (contra) | 2/10 Net 30 discounts taken by customers |

### Revenue Reporting Dimensions (via QBO Classes)
- **Product Line**: Sparkling Water, Cold Brew, Functional Juice, Kombucha, RTD Coffee
- **Customer Tier**: Key Account (top 10), Mid-Market, Emerging, DTC Individual
- **Geography**: West, Central, East, International

---

## 2. Cost of Goods Sold (5000 Series)

### Raw Materials — Ingredients
| Account # | Account Name | Notes |
|-----------|-------------|-------|
| 5000 | COGS — Ingredients, Concentrates & Extracts | Juice concentrates, coffee extract, tea concentrates |
| 5010 | COGS — Sweeteners | Cane sugar, stevia, monk fruit, erythritol, agave |
| 5020 | COGS — Functional Additives | Vitamins, probiotics, adaptogens, nootropics, CBD/hemp |
| 5030 | COGS — Flavors & Colors | Natural flavors, fruit purees, natural colorants |
| 5040 | COGS — Water & Base Liquids | Purified water, coconut water, oat base, almond base |
| 5050 | COGS — Acidulants & Preservatives | Citric acid, ascorbic acid, potassium sorbate |
| 5060 | COGS — Carbonation & Gases | CO2 for sparkling products, nitrogen for nitro cold brew |

### Raw Materials — Packaging
| Account # | Account Name | Notes |
|-----------|-------------|-------|
| 5100 | COGS — Bottles & Cans | Glass bottles, aluminum cans (sleek, standard, slim), PET |
| 5110 | COGS — Caps, Lids & Ends | Crown caps, twist-off, can ends, sport caps |
| 5120 | COGS — Labels & Shrink Sleeves | Pressure-sensitive labels, shrink sleeves, printed cans |
| 5130 | COGS — Cases & Cartons | Corrugated cases, variety pack cartons, shelf-ready packaging |
| 5140 | COGS — Pallets & Stretch Wrap | Pallets, tier sheets, stretch wrap, corner boards |
| 5150 | COGS — Packaging Miscellaneous | Tamper-evident bands, date code ink, QR code inserts |

### Co-Packing & Manufacturing
| Account # | Account Name | Notes |
|-----------|-------------|-------|
| 5200 | COGS — Co-Pack Toll Fees | Per-unit manufacturing fee from co-packer |
| 5210 | COGS — Setup & Changeover Fees | Line setup, flavor changeover, CIP (clean-in-place) |
| 5220 | COGS — Minimum Run Charges | Minimum batch fees when volume is below MOQ |
| 5230 | COGS — Overrun / Underrun Adjustments | Cost adjustment for ±10% production variance |

### Freight & Logistics (Inbound)
| Account # | Account Name | Notes |
|-----------|-------------|-------|
| 5300 | COGS — Inbound Freight, Ingredients | Freight to co-packer or warehouse for raw materials |
| 5310 | COGS — Inbound Freight, Packaging | Freight for packaging materials |
| 5320 | COGS — Inbound Freight, Finished Goods | Freight from co-packer to distribution warehouse |
| 5330 | COGS — Duties & Import Fees | Tariffs on imported ingredients (e.g., cane sugar, coconut) |

### Warehousing & Storage
| Account # | Account Name | Notes |
|-----------|-------------|-------|
| 5400 | COGS — Warehouse Storage | Monthly pallet storage fees |
| 5410 | COGS — Warehouse Handling | Pick, pack, ship fees (inbound receiving, outbound loading) |
| 5420 | COGS — Cold Storage / Refrigeration | Premium storage for refrigerated/frozen products |
| 5430 | COGS — Fulfillment (DTC) | eCommerce pick-pack-ship, including inner pack materials |

### Quality & Compliance
| Account # | Account Name | Notes |
|-----------|-------------|-------|
| 5500 | COGS — Quality Testing & Lab Fees | Micro testing, nutritional analysis, shelf life studies |
| 5510 | COGS — Certifications (Organic, Non-GMO, Kosher) | Certification audit fees, licensing fees |
| 5520 | COGS — Regulatory Compliance | FDA registration, state licensing, label compliance review |

### Shrink, Waste & Write-Offs
| Account # | Account Name | Notes |
|-----------|-------------|-------|
| 5600 | COGS — Shrink & Waste (Production) | Yield loss during production (spillage, filling waste, 1-5%) |
| 5610 | COGS — Expired Product Write-Off | Inventory past best-by date, cannot be sold |
| 5620 | COGS — Damage & Breakage | In-warehouse or in-transit damage |
| 5630 | COGS — Sample & Demo Product | Product used for in-store demos, trade shows, sampling events |

---

## 3. Operating Expenses (6000-7000 Series)

### Research & Development (6000)
| Account # | Account Name | Notes |
|-----------|-------------|-------|
| 6000 | R&D — Formulation Development | Flavor house fees, bench-top trials, pilot batches |
| 6010 | R&D — Packaging Development | Structural design, mold tooling, prototype runs |
| 6020 | R&D — Sensory & Consumer Testing | Focus groups, CLTs, home-use tests |
| 6030 | R&D — Regulatory & Claims Research | Substantiation studies, FDA GRAS determination |

### Sales & Marketing (6100-6300)
| Account # | Account Name | Notes |
|-----------|-------------|-------|
| 6100 | Sales — Broker Commissions | Typically 3-7% of net sales to food brokers |
| 6110 | Sales — Distributor Fees & Programs | UNFI/KeHE new item fees, marketing programs |
| 6120 | Sales — Demos & In-Store Sampling | Demo staffing agencies, product cost for demos |
| 6130 | Sales — Trade Shows & Events | Expo West, Fancy Food, NACS booth + travel |
| 6200 | Marketing — Digital Advertising | Meta, Google, TikTok, programmatic |
| 6210 | Marketing — Influencer & PR | Creator partnerships, PR agency retainer |
| 6220 | Marketing — Creative & Design | Packaging design, brand identity, photography |
| 6230 | Marketing — Content & Social Media | Content creation, social management tools |
| 6240 | Marketing — Consumer Promotions | Coupons (Ibotta, digital), rebates, contests |
| 6300 | Sales — Outbound Freight | Freight to distributor/retailer warehouses |
| 6310 | Sales — Amazon FBA Fees | Referral fees, FBA fulfillment fees, storage fees |

### SG&A (7000 Series)
| Account # | Account Name | Notes |
|-----------|-------------|-------|
| 7000 | Rent & Occupancy | Office space, test kitchen if applicable |
| 7010 | Utilities | Electric, gas, water, internet, phone |
| 7020 | Insurance — Product Liability | Essential for F&B; typically $5-15K/yr for emerging brand |
| 7030 | Insurance — General Liability | Premises, operations |
| 7040 | Insurance — Key-Man / Key-Person | Life insurance on founder/CEO if required by investors |
| 7050 | Insurance — Property & Inventory | Coverage for warehouse inventory |
| 7100 | Payroll — Salaries & Wages | Full-time employee compensation |
| 7110 | Payroll — Benefits | Health, dental, vision, 401k match |
| 7120 | Payroll — Taxes | FICA, FUTA, SUTA, workers' comp |
| 7200 | Professional Services — Legal | Trademark, contracts, regulatory counsel |
| 7210 | Professional Services — Accounting & Audit | CPA firm, annual audit/review, tax prep |
| 7220 | Professional Services — Consulting | Strategy, supply chain, food safety consultants |
| 7300 | Software & Technology | ERP, WMS, CRM, accounting, project management |
| 7310 | Travel & Entertainment | Customer visits, supplier audits, trade shows travel |
| 7400 | Depreciation & Amortization | Equipment, molds, leasehold improvements, intangible assets |
| 7500 | Bank Fees & Merchant Processing | Credit card processing, ACH fees, wire fees |
| 7510 | Interest Expense | Line of credit, term loans, inventory financing |

---

## 4. Inventory Accounts (1200 Series — Balance Sheet)

| Account # | Account Name | Type | Notes |
|-----------|-------------|------|-------|
| 1200 | Inventory — Raw Materials, Ingredients | Other Current Asset | Ingredients on hand at warehouse or co-packer |
| 1210 | Inventory — Raw Materials, Packaging | Other Current Asset | Packaging components on hand |
| 1220 | Inventory — Work-in-Process (WIP) | Other Current Asset | Batches in production, not yet completed |
| 1230 | Inventory — Finished Goods | Other Current Asset | Completed product, ready for sale |
| 1240 | Inventory — In-Transit | Other Current Asset | Product shipped but not yet received at destination |
| 1250 | Inventory — Consignment | Other Current Asset | Product at customer location, title not transferred |
| 1260 | Inventory — Samples & Demo Stock | Other Current Asset | Allocated for marketing use, reclassed to 5630 on use |
| 1290 | Reserve for Inventory Obsolescence | Other Current Asset (contra) | Allowance for expired, slow-moving, or damaged inventory |

---

## 5. Gross Margin Benchmarks by Category

| Product Category | Typical Gross Margin | Autonomi Target | Key Margin Drivers |
|-----------------|---------------------|-----------------|-------------------|
| Shelf-Stable Beverage (ambient) | 40-55% | 48-52% | Ingredient cost, co-pack efficiency, freight |
| Fresh / Refrigerated Beverage | 35-45% | 38-42% | Cold chain cost, shorter shelf life, higher shrink |
| RTD Coffee / Tea | 45-60% | 50-55% | Coffee/tea extract cost, can vs bottle, DTC mix |
| Functional / Enhanced Water | 50-65% | 55-60% | Low ingredient cost, premium pricing, simple BOM |
| Kombucha / Fermented | 40-50% | 42-48% | Fermentation yield, glass packaging cost, cold chain |
| Juice / Cold-Pressed | 30-42% | 35-40% | High ingredient cost, HPP processing, short shelf life |

### Margin Erosion Factors
- **Trade spend**: 15-30% of gross revenue for retail channel (reduces effective gross margin by 8-15 points)
- **Distributor margin**: 20-30% off wholesale for broadline distributors (UNFI, KeHE)
- **Retailer margin**: 35-45% off suggested retail
- **Freight**: 5-12% of COGS depending on weight and distance
- **Shrink/waste**: 2-8% of production volume (higher for fresh/refrigerated)

---

## 6. Break-Even Analysis Framework

### Unit Economics Model
```
Retail Price (SRP)                          $4.99
- Retailer Margin (40%)                    -$2.00
= Wholesale Price                           $2.99
- Distributor Margin (25%)                 -$0.75
= FOB Price to Distributor                  $2.24
- Trade Spend (20% of gross)               -$0.45
= Net Revenue per Unit                      $1.79
- COGS per Unit                            -$0.95
  (Ingredients $0.30 + Packaging $0.25 +
   Co-Pack $0.20 + Freight $0.12 + Storage $0.08)
= Gross Profit per Unit                     $0.84
= Gross Margin on Net Revenue               47%
```

### Contribution Margin by SKU
Contribution margin = Net Revenue - Variable COGS - Variable Selling (broker commission, freight-out)
- Track per-SKU to identify which products/sizes/flavors drive profit
- Flag SKUs below 30% contribution margin for reformulation or discontinuation
- Weighted contribution margin across portfolio drives break-even volume

### Break-Even Volume
```
Break-Even Units = Fixed Costs / Contribution Margin per Unit
Example: $500,000 annual fixed costs / $0.65 CM per unit = 769,231 units
         = ~64,103 cases of 12 = ~5,342 cases/month
```

---

## 7. Trade Spend Accounting Detail

### Scan-Back (Performance-Based)
- Triggered when product scans at register during promo window
- Retailer submits scan data; brand pays per-unit rebate
- Accrue when promo starts: Dr. 4100 Trade Spend — Scan-Backs, Cr. 2100 Accrued Trade Spend
- Settle when billed: Dr. 2100 Accrued Trade Spend, Cr. 1000 Cash/AP

### MCB (Manufacturer Chargeback)
- Distributor sells to retailer at reduced price; charges brand the difference
- Distributor deducts from remittance or issues separate invoice
- Record: Dr. 4110 Trade Spend — MCBs, Cr. Accounts Receivable (if deducted) or Cr. Cash

### OI (Off-Invoice)
- Immediate discount on every unit shipped during promo period
- Simplest to account for: reduced invoice amount at time of sale
- Net revenue recognized at discounted price; OI tracked in 4120 for gross-to-net bridge

### Billback
- Retroactive payment for promotional activity already completed
- Retailer submits proof of performance; brand pays after verification
- Accrue at promo start, settle on proof submission

### Slotting Fees
- One-time payment for shelf placement (new item introductions)
- Can be $5,000-$50,000+ per SKU per retailer depending on chain size
- Expensed immediately or amortized over expected shelf life (12-24 months)
- ASC 606 guidance: reduce transaction price if fee is not for distinct service

### Deduction Management
- Retailers and distributors routinely take deductions from payments
- Common unauthorized deductions: short-ship claims, damage claims, pricing disputes
- Process: receive short-pay, research deduction, code to correct trade spend account or dispute
- Dispute rate target: resolve 85%+ within 60 days
- Write-off threshold: deductions under $50-100 may be auto-written off (cost to research exceeds value)

---

## 8. QBO Configuration Notes

### Class Tracking
Enable class tracking for product line segmentation. Assign classes at the transaction line level to support multi-product P&L reporting. Standard classes: one per product line (e.g., "Sparkling Water", "Cold Brew", "Functional Juice").

### Location Tracking
Use locations for channel segmentation (Retail, DTC, Foodservice, Private Label) or for entity/warehouse tracking if operating multiple locations.

### Custom Fields
QBO Advanced supports custom fields on transactions. Use for: Lot Number, Production Batch ID, Promotion ID, Broker Name, Distributor Region.

### Sub-Accounts vs. Classes
Use sub-accounts for permanent structural distinctions (ingredient types, packaging types). Use classes for analytical dimensions that cross account boundaries (product lines). Avoid creating a separate account for every SKU — use Items for that level of detail.

### Reporting Stack
- **P&L by Class**: Gross margin by product line
- **P&L by Location**: Channel profitability
- **Gross-to-Net Bridge**: Custom report mapping gross revenue through all trade spend deductions to net revenue
- **COGS Variance**: Standard cost vs. actual cost by batch (requires custom report or export to Excel)
- **Inventory Aging**: Days on hand by SKU, flagging items approaching best-by date

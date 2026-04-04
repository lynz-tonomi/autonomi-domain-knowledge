# F&B Supply Chain Operations — Domain Knowledge Base v2

## Purpose

This skill provides deep industry knowledge for food and beverage supply chain operations. It is not platform documentation — it encodes the working expertise of supply chain, procurement, logistics, and planning professionals operating in the beverage manufacturing sector (juice, kombucha, functional drinks, oat milk, cold brew, RTD tea/coffee).

## When to Use

Trigger this skill when the conversation involves any of the following:

- **Commodity procurement** — ingredient sourcing, futures markets, forward contracting, supplier negotiations, landed cost modeling, MOQs, payment terms, hedging
- **Cold chain logistics** — temperature-controlled warehousing, reefer transport, FIFO/FEFO, freight rate analysis, pallet optimization, carrier qualification, last-mile cold chain
- **Demand planning & forecasting** — S&OP, seasonal patterns, promotion lift, POS data integration, safety stock for perishables, forecast accuracy metrics, co-man capacity booking
- **Supplier qualification** — approved supplier programs, GFSI audits, COA management, incoming inspection, supplier scorecards, SCAR process, FSMA 204 traceability, allergen controls

Do NOT use this skill for:

- General software questions unrelated to F&B operations
- Retail or foodservice operations (this covers manufacturing/CPG supply chain)
- Regulatory deep-dives on labeling or claims (see `fb-food-safety-compliance` skill)
- Product formulation science (see `fb-product-formulation` skill)

## Key Concepts

### Commodity Procurement
| Concept | Summary |
|---|---|
| FCOJ-A futures | ICE-traded frozen concentrated orange juice contract; benchmark for citrus pricing globally |
| Sugar #11 | ICE world raw sugar futures; reference price for sweetener procurement |
| Forward contracting | Locking price and volume 3-12 months ahead to hedge commodity volatility |
| Landed cost | Total delivered cost: FOB price + freight + insurance + duties + handling + quality hold costs |
| Organic premiums | Typically 30-80% above conventional depending on ingredient; constrained by certified acreage |
| Specialty sweetener lead times | Stevia 12-16 wk, monk fruit 16-20 wk (China origin), allulose 8-12 wk |
| PET resin pricing | Tracks crude oil and paraxylene; contracted quarterly or semi-annually |

### Cold Chain Logistics
| Concept | Summary |
|---|---|
| Temperature zones | Fresh juice 33-38 deg F / Frozen concentrate -10 deg F / Shelf-stable ambient (heat-sensitive) |
| Reefer monitoring | Real-time GPS + temp loggers (Sensitech TempTale, Emerson/Testo); download at receiving |
| FIFO vs FEFO | First-In-First-Out vs First-Expired-First-Out; FEFO is standard for perishable beverage |
| Pallet Ti x Hi | Cases per layer (Ti) x layers high (Hi); determines pallet cube and truck utilization |
| Freight modes | FTL (full truckload) for high-volume lanes; LTL (less-than-truckload) for emerging brand volumes |
| Cross-docking | Product moves through DC without storage; reduces dwell time for perishables |

### Demand Planning
| Concept | Summary |
|---|---|
| S&OP cadence | Monthly cycle: demand review -> supply review -> pre-S&OP -> executive reconciliation |
| Promotion lift | TPR/BOGO/display typically 2-5x baseline volume; must be isolated from baseline forecast |
| Syndicated data | IRI/Circana and NielsenIQ provide category-level POS; retailer portals give account-level |
| MAPE | Mean Absolute Percentage Error; primary forecast accuracy metric; target <25% at SKU-month |
| Co-man scheduling | Minimum run sizes (often 500-2,000 cases), scheduling windows booked 4-8 weeks out |
| Safety stock (perishable) | Must balance service level against shelf-life waste; dynamic SS based on demand variability and remaining shelf |

### Supplier Qualification
| Concept | Summary |
|---|---|
| GFSI benchmarked | SQF, BRC, FSSC 22000, IFS — any one satisfies "GFSI certified" requirement |
| COA requirements | Micro (APC, yeast/mold, coliforms, pathogens), chemical (Brix, pH, titratable acidity, heavy metals), physical (color, particle size), allergens |
| Supplier scorecard | Weighted composite: Quality 40%, Delivery 25%, Cost 20%, Responsiveness 15% (typical) |
| SCAR | Supplier Corrective Action Request — formal nonconformance process with root cause and CAPA |
| FSMA 204 | FDA Food Traceability Rule; requires KDEs at CTEs for foods on the Food Traceability List |
| Letters of Guarantee | Written supplier attestation of allergen-free status for specific allergens |

## Reference Files

| File | Scope |
|---|---|
| `references/commodity_procurement.md` | Juice concentrates, sweeteners, flavors, packaging materials, contract structures, hedging |
| `references/cold_chain_logistics.md` | Temperature management, warehousing, freight, pallet optimization, carrier qualification |
| `references/demand_planning.md` | Forecasting methods, S&OP, promotion modeling, co-man capacity, inventory classification |
| `references/supplier_qualification.md` | Approved supplier programs, audits, COAs, scorecards, FSMA 204 traceability |

## Usage Pattern

1. Identify which domain area the user's question falls into
2. Load the relevant reference file(s)
3. Apply the domain knowledge to the user's specific operational context
4. Provide actionable guidance grounded in F&B industry norms, not generic supply chain theory

## Industry Context

This knowledge base is calibrated for:
- **Company size**: Emerging to mid-scale CPG brands ($5M-$200M revenue)
- **Production model**: Primarily co-manufactured (co-pack/co-man), with some owned production
- **Channels**: Retail (grocery, natural, mass), e-commerce/DTC, foodservice
- **Product types**: Refrigerated and shelf-stable beverages, functional foods
- **Geography**: US-centric supply chain with global ingredient sourcing

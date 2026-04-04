# Cold Chain Logistics — F&B Beverage Manufacturing

## Overview

Cold chain management is the single largest operational differentiator between beverage categories. A shelf-stable RTD tea can survive days of logistics abuse; a fresh cold-pressed juice has a 30-45 day shelf life where every hour of temperature excursion erodes saleable days. This reference covers the full cold chain from ingredient receipt through last-mile delivery.

---

## 1. Temperature Requirements by Product Type

| Product Category | Storage Temp | Transport Temp | Critical Threshold | Shelf Life (typical) |
|---|---|---|---|---|
| Fresh juice (HPP) | 33-38 deg F | 33-38 deg F | >41 deg F triggers food safety concern | 30-60 days |
| Fresh juice (raw, unpasteurized) | 33-36 deg F | 33-36 deg F | >38 deg F accelerates spoilage rapidly | 3-7 days |
| Cold-brew coffee (RTD) | 33-38 deg F | 33-38 deg F | >41 deg F; sensitive to light exposure | 60-90 days |
| Kombucha (live culture) | 33-38 deg F | 33-38 deg F | >45 deg F causes over-carbonation, blown caps | 60-120 days |
| Frozen juice concentrate | -10 deg F or below | -10 deg F or below | >0 deg F compromises quality | 18-24 months |
| Shelf-stable (aseptic, hot-fill) | Ambient (50-80 deg F ideal) | Ambient | >95 deg F accelerates flavor degradation | 9-18 months |
| Oat/nut milk (refrigerated) | 33-38 deg F | 33-38 deg F | >41 deg F | 45-90 days (ESL) |
| Functional shots (refrigerated) | 33-38 deg F | 33-38 deg F | >41 deg F | 60-90 days |

**Key principle**: The target is not just a temperature number — it is a temperature *history*. Cumulative time-temperature exposure (TTI) determines remaining quality and safety margin. A product that spends 4 hours at 45 deg F during a truck breakdown may still be safe but has lost saleable shelf life.

---

## 2. Reefer Trailer Specifications and Monitoring

### Trailer Types

| Type | Temp Range | Use Case | Capacity |
|---|---|---|---|
| Single-temp reefer (53') | -20 to +70 deg F | Standard for single-zone loads | 22-24 pallets (floor-loaded more) |
| Multi-temp reefer (53') | 2 or 3 zones independently controlled | Mixed temp loads (frozen + refrigerated) | Reduced per-zone; 8-12 pallets per zone |
| Reefer sprinter van | 33-45 deg F | Last-mile, DTC, small retail delivery | 4-6 pallets |
| Insulated (non-mechanical) | Maintains temp for 4-8 hours | Short hauls; pre-cooled product | 22-24 pallets |

### Pre-Trip Protocol (Non-Negotiable for Perishables)

1. **Pre-cool** trailer to target temperature 2+ hours before loading. Never load warm product into a warm trailer expecting the unit to pull down temperature — reefer units are designed to *maintain* temp, not *cool* product.
2. **Verify** set point matches BOL requirement. Photograph the reefer unit display showing set point and actual temp.
3. **Inspect** trailer interior: clean, no residual odors, no damage to walls/floor, drain plugs closed, air chute intact.
4. **Confirm** continuous vs cycle mode: Continuous for frozen; cycle (start-stop) acceptable for refrigerated if product is pre-cooled.

### Temperature Monitoring Devices

| Device | Type | Data | Cost | Use Case |
|---|---|---|---|---|
| Ryan iButton | Single-use logger | Temp at programmable intervals | $3-8 each | Placed in load; downloaded at receiving |
| Sensitech TempTale | Single-use or multi-use | Temp + optional humidity | $5-15 each | Industry standard for food logistics |
| Emerson GO Real-Time | Real-time cellular | GPS + temp; cloud dashboard | $25-50/trip | High-value loads; provides in-transit alerts |
| Carrier/Thermo King telematics | Integrated with reefer unit | Continuous reefer performance + temp | Included with modern units | Fleet-level monitoring; requires carrier cooperation |
| Testo 184 | Multi-use USB logger | Temp, humidity, shock | $60-100 (reusable) | Repeat-lane monitoring |

**Best practice**: Place a minimum of 2 loggers per load — one at the front near the reefer unit and one at the rear doors (warmest spot). For high-value or long-haul loads, add a third logger in the center of the load.

---

## 3. Warehouse Types and Configuration

### Temperature Zones

| Zone | Temp Range | Typical Products | Storage Cost (per pallet/month) |
|---|---|---|---|
| Ambient (dry) | 50-80 deg F | Shelf-stable beverages, packaging materials, dry ingredients | $8-15 |
| Cooler | 35-45 deg F | Fresh juice, kombucha, cold-brew, dairy-based beverages | $18-30 |
| Deep cooler | 28-34 deg F | Extended holding for some dairy; not common for beverages | $22-35 |
| Freezer | -10 to 0 deg F | Frozen concentrates, frozen fruit purees, ice cream mixes | $25-45 |
| Blast freeze | -20 to -30 deg F | Rapid freeze for incoming product; not long-term storage | Premium; per-pallet charge |

### Warehouse Selection Criteria for Beverage Brands

1. **SQF/GFSI certification**: Required by most retailers for food-grade warehousing
2. **Lot traceability system**: WMS must track lot numbers, production dates, and expiration dates at the pallet level
3. **FEFO capability**: WMS must pick by earliest expiration, not just FIFO
4. **Temperature monitoring**: Continuous recording with alarms; accessible logs for audit
5. **Allergen segregation**: If handling allergen-containing products, dedicated storage or documented controls
6. **Pest management**: Licensed pest control provider; documented IPM program
7. **Insurance**: Warehouse legal liability plus product-specific coverage; $500K-$2M typical

### Warehouse Operations — Key Metrics

| Metric | Target | Impact |
|---|---|---|
| Receiving accuracy | >99.5% | Wrong lot/qty receiving cascades to inventory errors |
| On-time shipping | >98% | Retail delivery windows are 30-minute to 2-hour; late = rejection |
| Inventory accuracy | >99.7% (cycle count) | Critical for demand planning and avoiding phantom inventory |
| Order accuracy (pick/pack) | >99.8% | Mis-ships to retailers result in chargebacks ($200-500 each) |
| FEFO compliance | 100% | Shipping older-than-oldest code triggers retailer fines |
| Damage rate | <0.5% of throughput | Wet floors, forklift damage, pallet collapse |

---

## 4. FIFO / FEFO Management

### FEFO (First Expired, First Out) — Industry Standard for Perishables

FEFO is the governing principle for all perishable beverage inventory. Key operational requirements:

- **WMS configuration**: Expiration date (or best-by date) must be a mandatory field at receiving; WMS allocates picks to earliest-expiring lot
- **Retailer code date policies**: Most retailers require minimum remaining shelf life at delivery:

| Retailer Tier | Minimum Remaining Shelf Life | Practical Impact |
|---|---|---|
| Conventional grocery (Kroger, Albertsons) | 60-75% of total shelf life | For 60-day product, must deliver with 36-45 days remaining |
| Natural channel (Whole Foods, Sprouts) | 50-67% of total shelf life | Slightly more flexible; still strict |
| Club (Costco, Sam's) | 67-75% | High volume mitigates; but rejection is costly |
| E-commerce / DTC | 50%+ typical; brand-controlled | More flexibility; brand sets own standard |

- **Short-dated inventory**: Product approaching code date cutoff becomes unsaleable to retail. Options: secondary market (Grocery Outlet, closeout), employee sales, donation (tax benefit under Enhanced Tax Deduction for food donations), destruction (last resort — document for write-off).

### Managing Multiple Production Lots

A single SKU may have 3-5 active lots in the warehouse at any time. The WMS must:
1. Track each lot by production date, expiration date, and co-manufacturer batch code
2. Prevent mixing lots within a single customer order unless customer approves
3. Alert planners when inventory approaches code-date cutoff (typically 30 days before becomes unsaleable)
4. Support lot-level hold/release for quality or food safety investigations

---

## 5. Pallet Configurations

### Standard Pallet: 40" x 48" GMA (Grocery Manufacturers Association)

Pallet configuration is expressed as **Ti x Hi** where Ti = cases per layer and Hi = number of layers.

| Product Format | Case Pack | Case Dimensions (L x W x H) | Ti x Hi | Cases/Pallet | Units/Pallet |
|---|---|---|---|---|---|
| 12 oz can (12-pack) | 2/12-pack per case | 16" x 11" x 5" | 8 x 10 | 80 | 1,920 cans |
| 12 oz PET bottle (12-pack) | 12 per case | 16" x 11" x 9" | 8 x 6 | 48 | 576 bottles |
| 16 oz PET bottle (12-pack) | 12 per case | 16" x 11" x 11" | 8 x 5 | 40 | 480 bottles |
| 10 oz glass bottle (24-pack) | 24 per case | 16" x 11" x 8" | 8 x 6 | 48 | 1,152 bottles |
| 64 oz PET multi-serve | 8 per case | 16" x 11" x 12" | 8 x 5 | 40 | 320 bottles |
| 2 oz functional shot (12-pack) | 12 per case | 8" x 6" x 4" | 20 x 12 | 240 | 2,880 shots |

**Pallet height limits**:
- Warehouse: 48-52" typical for single-stack; double-stack if product can support it
- Truck: 100-102" from floor (to fit under trailer ceiling at 110")
- Retailer: Some retailers specify maximum pallet height (e.g., Whole Foods 48")

### Pallet Stability

- **Stretch wrap**: Machine wrap at 200-250% pre-stretch; 3 bottom wraps, 2-3 spiral wraps, 2 top wraps minimum
- **Corner boards**: Required for stacked pallets and any pallet over 50" height
- **Slip sheets**: Some DCs request slip sheets between pallet and product for automated handling
- **Top caps**: Corrugated cap on top layer prevents crush damage during stacking

---

## 6. Freight Considerations: LTL vs FTL

| Factor | FTL (Full Truckload) | LTL (Less Than Truckload) |
|---|---|---|
| **Volume** | 20-24 pallets; 40,000-44,000 lbs | 1-12 pallets |
| **Cost per pallet** | $30-75/pallet (long haul) | $75-200/pallet |
| **Transit time** | Direct; 1-5 days depending on lane | Multi-stop; 3-10 days |
| **Temperature control** | Full control; single customer | Mixed loads; temp compromise risk |
| **Damage risk** | Lower (no transloading) | Higher (multiple handling points) |
| **Best for** | Warehouse replenishment, DC-to-DC, high-volume retailers | Small retail deliveries, new market testing |

### Freight Rate Structures

| Rate Type | Unit | When Used |
|---|---|---|
| Per mile | $2.50-5.00/mile (reefer FTL) | Long-haul dedicated lanes |
| Per pallet | $75-200 (LTL reefer) | Multi-stop LTL shipments |
| Per CWT (hundredweight) | $8-25/CWT | Dense products; weight-limited loads |
| Flat rate | Negotiated | Dedicated lanes with consistent volume |
| Fuel surcharge | % of line haul (15-30% typical) | Applied on top of base rate; indexed to DOE diesel price |
| Accessorial charges | Per occurrence | Detention ($50-75/hr after 2hr free), liftgate ($75-150), appointment scheduling ($25-50) |

### Seasonal Freight Capacity Impacts

| Season | Impact | Strategy |
|---|---|---|
| May-September | Produce season competes for reefer capacity; rates +15-30% | Book trucks 5-7 days ahead; consider contract rates |
| November-December | Holiday demand; driver shortages | Build inventory in October for holiday promotional volume |
| January-March | Capacity loosens; best rates | Negotiate annual contracts during this window |
| Severe weather events | Spot market spikes 50-100% | Maintain 1-2 week safety stock at forward DCs |

---

## 7. Last-Mile Cold Chain for DTC

Direct-to-consumer shipping of perishable beverages requires specialized packaging:

| Method | Temp Hold | Cost per Shipment | Best For |
|---|---|---|---|
| Insulated box + gel packs | 24-48 hours below 40 deg F | $8-15 packaging cost | 1-2 day ground zones |
| Insulated box + dry ice | 48-72 hours | $12-20 packaging cost + hazmat surcharge | 2-3 day zones; frozen product |
| Insulated pouch (flat rate box) | 12-24 hours | $4-8 | Overnight/same-day local |

**DTC cold chain rules**:
1. Ship Monday-Wednesday only (avoid weekend warehouse sitting)
2. Use 2-day or faster for 2+ day ground zones
3. Include "PERISHABLE — REFRIGERATE UPON ARRIVAL" sticker on outer carton
4. Seasonal adjustment: increase gel pack weight 50% for summer shipping (May-Sept)
5. Carrier selection: FedEx 2Day, UPS 2nd Day Air, or regional cold-chain specialists (AxleHire, Veho)

---

## 8. Carrier Qualification

### Minimum Requirements for Reefer Carriers

1. **Authority**: Active FMCSA operating authority (MC number); verify at safer.fmcsa.dot.gov
2. **Insurance**: $1M auto liability, $100K cargo, $1M general liability minimum
3. **Safety rating**: Satisfactory or better FMCSA rating; or no rating with acceptable BASICs scores
4. **Equipment**: Reefer units less than 10 years old; documented pre-trip inspection records
5. **Temperature monitoring**: Capable of providing continuous temperature records for each load
6. **Food safety training**: Driver training on food transportation sanitary requirements (FSMA 21 CFR 1.908)
7. **Sanitary transport**: Written procedures for cleaning, temperature monitoring, and prevention of contamination

### Temperature Excursion Protocol

When a temperature excursion is detected during transit or at receiving:

| Step | Action | Timeline |
|---|---|---|
| 1. Document | Record actual temp, duration, product affected, lot codes | Immediately |
| 2. Segregate | Place product on hold — do not distribute | Immediately |
| 3. Notify | Alert QA and food safety team | Within 1 hour |
| 4. Assess | QA evaluates severity: minor (<5 deg F over, <2 hours) vs major | Within 4 hours |
| 5. Disposition | QA determines: release, re-inspect, lab test, or reject | Within 24 hours |
| 6. Root cause | Identify cause: equipment failure, loading error, door seal, carrier negligence | Within 48 hours |
| 7. Corrective action | Document corrective action; update carrier scorecard | Within 1 week |
| 8. Claim filing | File freight claim for rejected product with carrier or insurer | Within 9 months (Carmack Amendment) |

---

## 9. Bill of Lading Requirements

The BOL is both a shipping contract and a legal document. For refrigerated food shipments:

| Field | Requirement |
|---|---|
| Shipper / consignee | Full legal names and addresses |
| SCAC code | Standard Carrier Alpha Code of transporting carrier |
| PO number(s) | Retailer/customer PO; must match receiving system |
| Product description | Product name, UPC, lot code, case count, pallet count |
| Weight | Gross weight per pallet and total shipment weight |
| Temperature requirement | **Mandatory for reefer**: "Maintain at 34-38 deg F continuous" — specific language |
| NMFC code | National Motor Freight Classification code for LTL rating |
| Freight class | Determines LTL pricing (Class 50-500; beverages typically 55-85) |
| Seal number | Recorded at loading; verified at receiving (must match) |
| Special instructions | Appointment number, dock assignment, do-not-freeze, no double-stacking |

---

## 10. Cross-Docking Operations

Cross-docking minimizes warehouse dwell time — product moves from inbound to outbound with minimal or no storage. Types relevant to beverage distribution:

| Type | Description | Use Case |
|---|---|---|
| **Pre-allocated** | Inbound already assigned to outbound orders before arrival | Retailer DC replenishment on tight schedules |
| **Consolidation** | Multiple inbound shipments combined into outbound loads | Multi-origin products going to single retailer DC |
| **Deconsolidation** | One inbound load broken into multiple outbound shipments | Co-man full-truck received; split to regional DCs |

**Critical success factors**: Advance shipping notice (ASN) accuracy, receiving dock scheduling precision, adequate staging space, and trained labor for rapid pallet sorting.

---

## 11. Distribution Center Slotting

Velocity-based slotting optimizes picking efficiency and minimizes warehouse labor cost:

| Velocity | Slot Location | Pick Method | Replenishment |
|---|---|---|---|
| A (top 20% of picks) | Floor-level, closest to shipping dock | Case pick from pallet | Daily or continuous |
| B (next 30%) | Floor to second rack level | Case pick from pallet or shelf | 2-3x per week |
| C (next 30%) | Upper rack levels | Pallet pick (full pallet pulls) | Weekly |
| D (bottom 20%) | Deep storage, farthest from dock | Pallet pick; slow movers | As needed |

**Beverage-specific slotting considerations**:
- Weight: Beverages are heavy — slot at floor level to prevent forklift strain at height
- Seasonal rotation: Re-slot before summer peak (lemonade, iced tea move from C to A)
- Promotional staging: Create temporary forward pick locations for promotion builds
- Multi-temperature: Slot high-velocity refrigerated SKUs near cooler outbound staging doors

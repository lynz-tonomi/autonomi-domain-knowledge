# Quality Systems Reference
**Skill:** food-safety-compliance | **Domain:** quality-systems | **Version:** 1.0.0

---

## 1. CAPA Management

### 1.1 CAPA Lifecycle

AGNT-11 (CAPA Manager) manages all Corrective and Preventive Actions from open to close. Every CAPA is tracked on the `capa` page of the dashboard.

| Phase | Steps | Agent Role |
|---|---|---|
| **Opening** | Trigger identification → classification → assignment | AGNT-11 opens CAPA; assigns owner; sets deadline |
| **Root Cause Analysis** | 5-Why, fishbone diagram, process mapping | AGNT-11 prompts and tracks; LynZ assists with analysis |
| **Corrective Action** | Immediate containment + root cause correction | Owner implements; AGNT-11 tracks completion |
| **Preventive Action** | System improvement to prevent recurrence | Owner defines; AGNT-11 tracks |
| **Verification** | Effectiveness check (30/60/90 day) | AGNT-09 verifies; AGNT-11 closes CAPA if effective |
| **Closure** | Final review; documentation complete | AGNT-11 closes; blockchain record written |

### 1.2 CAPA Classification

| Class | Trigger | Response Time | Examples |
|---|---|---|---|
| Critical | Food safety threat; regulatory violation; recall | Immediate; contain within 24 hrs | CCP deviation, undeclared allergen, Class I recall |
| Major | Significant process failure; certification nonconformance | Root cause within 7 days | BRC major nonconformance, supplier quality failure |
| Minor | Minor process deviation; documentation gap | Root cause within 30 days | BRC minor nonconformance, labeling error |
| Preventive | Trend analysis indicates emerging risk | Implement within 60 days | EMP trend, repeat supplier issue |

### 1.3 Active CAPAs (as of 2026-04-04)

| CAPA ID | Class | Description | Status | Due Date |
|---|---|---|---|---|
| CAPA-2026-012 | Major | NutSource allergen incident — root cause | RCA In Progress | 2026-04-18 |
| CAPA-2026-011 | Minor | BRC audit finding: allergen cleaning validation docs incomplete | Corrective Action | 2026-04-14 |
| CAPA-2026-009 | Minor | Metal detector calibration record gap (2 missed entries) | Verification | Closed 2026-03-28 |
| CAPA-2026-007 | Preventive | EMP: L. innocua indicator positive trend in Zone 2 | Preventive Action | 2026-05-01 |

---

## 2. Allergen Control Program

### 2.1 Allergens Present at PPB Facility

| Allergen | US (Big-9) | EU (14) | Present at Facility | Products Affected |
|---|---|---|---|---|
| Milk | Yes | Yes | No | None |
| Eggs | Yes | Yes | No | None |
| Fish | Yes | Yes | No | None |
| Shellfish | Yes | Yes | No | None |
| Tree Nuts | Yes | Yes | No* | *Oat milk uses no tree nuts, but almond labeling reviewed |
| Peanuts | Yes | Yes | Incident-basis (NutSource lot) | Risk: tropical blend if contaminated |
| Wheat/Gluten | Yes | Yes | Yes (oat cross-contact risk) | Oat Milk 1L (gluten-free certified with GF oats) |
| Soybeans | Yes | Yes | No | None |
| Sesame | Yes (FASTER Act 2023) | Yes | No | None |
| Celery | No | Yes | No | None |
| Mustard | No | Yes | No | None |
| Lupin | No | Yes | No | None |
| Molluscs | No | Yes | No | None |
| Sulphur dioxide | No | Yes (>10 ppm) | Trace in wine-derived ingredients | Not in current BOMs |

### 2.2 Allergen Control Measures

**Supplier control:**
- All suppliers must declare allergen status on COA
- Any supplier manufacturing in a facility that also handles Big-9 allergens must declare this on their food safety statement
- AGNT-06 flags any undeclared or changed allergen statements; AGNT-10 validates before lot is cleared

**Line sequencing:**
- Allergen-containing products scheduled last in a production sequence before a full allergen clean (see production_scheduling.md)
- AGNT-10 validates all scheduled changeovers before they appear on the published schedule

**Cleaning validation:**
- Allergen cleaning validated by ELISA rinsate testing for each allergen/surface type combination
- Validation frequency: Initial + annually + after any equipment change
- Positive ELISA on pre-op rinsate: STOP LINE; repeat clean; reswab

**Label verification:**
- CCP-6 covers label allergen declaration (see haccp_ccps.md)
- AGNT-10 cross-references the allergen profile of each BOM against the approved label for that product

### 2.3 Allergen Cross-Contact Risk Assessment

| Scenario | Risk Level | Control |
|---|---|---|
| Tropical blend (may contact peanut at NutSource) | High — currently mitigated | Supplier suspended; backup supplier activated |
| Oat Milk line → juice line changeover | Medium (gluten cross-contact) | Full wet clean + ATP verification; 4-hour downtime |
| Kombucha line → juice line | Low allergen risk; high microbiological risk | Full CIP + culture swab; 6-hour downtime |
| Juice → juice same fruit family | Very low | Rinse + quick wet clean; 45 min |

---

## 3. Environmental Monitoring Program (EMP)

### 3.1 Zone Classification

| Zone | Definition | Sampling Target | Examples at PPB |
|---|---|---|---|
| Zone 1 | Direct product contact surfaces | Target organisms (Listeria sp.) + indicators | Filler nozzles, conveyor belts, product contact tubing |
| Zone 2 | Non-product-contact surfaces near Zone 1 | Indicator organisms (Listeria) | Equipment frames, drip shields, inside of filler shroud |
| Zone 3 | Non-product-contact surfaces away from product | Indicator organisms | Floor drains, walls in processing area |
| Zone 4 | Remote areas, receiving, locker rooms | Indicator organisms (less frequent) | Receiving dock, employee areas |

### 3.2 Sampling Schedule

| Zone | Organism Target | Frequency | Method |
|---|---|---|---|
| Zone 1 | Listeria monocytogenes | Weekly (during production) | Sponge swab, 30 cm² area |
| Zone 2 | Listeria spp. (indicator) | Bi-weekly | Sponge swab |
| Zone 3 | Listeria spp. | Monthly | Sponge swab |
| Zone 4 | Listeria spp. | Quarterly | Sponge swab |

**Lab partner:** Certified external lab; results within 48 hours  
**AGNT-12 monitoring:** Tracks trends; flags any Zone 1–2 positive  

### 3.3 Positive Result Response Protocol

| Result | Response |
|---|---|
| Zone 3 or 4 positive (indicator) | Intensified cleaning + 2 follow-up swabs over next 2 weeks |
| Zone 2 positive (indicator) | Enhanced cleaning; Zone 2 intensified sampling for 4 weeks; evaluate harborage points |
| Zone 1 positive (Listeria spp.) | Stop production; full sanitation; hold all product produced since last negative; 100% Zone 1 sampling before restart; CAPA opened |
| Zone 1 positive (L. monocytogenes) | Stop production; full sanitation; quarantine all RTE product; evaluate recall; immediate escalation to QA manager + AGNT-14 |

---

## 4. Sanitation Program

### 4.1 CIP (Clean-in-Place) Specifications

| CIP Stage | Chemical | Concentration | Temperature | Contact Time |
|---|---|---|---|---|
| Pre-rinse (water) | None | — | Cold | 5 min |
| Caustic wash | Sodium hydroxide | 1.5–2.0% | 160°F (71°C) | 20 min |
| Intermediate rinse | Water | — | Hot | 5 min |
| Acid wash (weekly) | Phosphoric or nitric acid | 0.5–1.0% | 140°F (60°C) | 15 min |
| Final rinse | Potable water | — | 180°F (82°C) | 5 min |
| Sanitize (pre-production) | Peracetic acid | 100–200 ppm | Ambient | 5 min no-rinse |

### 4.2 CIP Validation

- ATP swabs post-CIP: Must be ≤ 100 RLU on product contact surfaces
- Caustic concentration verified by titration at start of each CIP cycle
- CIP log reviewed by AGNT-09; deviations flagged automatically

### 4.3 Master Sanitation Schedule (MSS)

| Frequency | Task |
|---|---|
| Daily | CIP all product contact equipment; sweep and mop floors; sanitize surfaces |
| Weekly | Deep clean drains; acid wash CIP; clean overheads and light fixtures in processing area |
| Monthly | Full facility sanitation audit; clean cooling towers; clean HVAC diffusers |
| Quarterly | Pest control inspection; deep clean warehouse areas; refrigeration coil cleaning |
| Annually | Full facility sanitation validation; allergen cleaning validation; food defense assessment |

---

## 5. Audit Readiness Checklist

AGNT-11 maintains a continuous audit readiness score updated daily. Key readiness items:

| Item | Status |
|---|---|
| HACCP plan current and reviewed within 12 months | Current (reviewed 2025-08-10) |
| All CCP monitoring records up to date | Current (AGNT-09 continuous) |
| All active CAPAs within response deadline | 1 major in progress (due 2026-04-18) |
| Certifications all current (no expired certs) | All current |
| COA library: 100% of active lots have approved COA | 98.4% (3 pending) |
| Employee training records current (all staff) | 96.7% (2 overdue — flagged) |
| Allergen cleaning validation current | 1 gap noted (CAPA-2026-011 in progress) |
| EMP: no Zone 1 positives in last 12 months | Clean (no Zone 1 positives) |
| Recall plan tested within 12 months | Tested 2025-10-15 |
| FDA registration current | Current |

**Overall audit readiness score: 94.2 / 100**

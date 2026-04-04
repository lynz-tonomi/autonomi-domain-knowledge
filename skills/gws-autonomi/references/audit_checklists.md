# Google Forms Audit Checklists for F&B

## Overview

Google Forms serves as Autonomi's primary data collection tool for inspections, audits, and monitoring activities across the production facility. Each form feeds responses into a linked Google Sheet for trend analysis, corrective action tracking, and dashboard integration via Looker Studio. Forms are deployed on tablets and mobile devices for real-time, point-of-use data capture.

---

## 1. Pre-Operational Inspection Checklist

### Purpose
Conducted before every production shift by the lead operator and verified by QC. Confirms that all equipment and the production environment meet sanitary conditions before product contact begins. Required by 21 CFR 117 (CGMP), SQF Code, and BRC Global Standard.

### Form Structure

**Header Section:**
- Date (auto-populated)
- Production Line (dropdown: L1, L2, L3, etc.)
- Shift (dropdown: Day, Swing, Night)
- Inspector Name (dropdown from employee list)
- QC Verifier (dropdown from QC staff list)

**Section 1: Equipment Cleanliness**

| Check Item | Response Type | Corrective Action Trigger |
|-----------|--------------|--------------------------|
| All product contact surfaces visually clean (no residue, staining, buildup) | Pass / Fail / N/A | Fail: re-clean, re-inspect, document |
| Non-product contact surfaces within 1 meter of product zone clean | Pass / Fail / N/A | Fail: clean before startup |
| CIP verification record reviewed and acceptable from previous shift | Pass / Fail / N/A | Fail: do not start; investigate CIP failure |
| ATP swab results from post-CIP verification within limits (<150 RLU) | Pass / Fail / N/A + numeric entry | Fail: re-clean, re-swab |
| No previous-run product residue on any surface | Pass / Fail / N/A | Fail: re-clean; allergen risk assessment if changeover |
| Conveyor belts clean and free of debris | Pass / Fail | Fail: clean before startup |
| Filler nozzles/valves clean and properly seated | Pass / Fail | Fail: disassemble, clean, re-inspect |

**Section 2: Allergen Changeover (Conditional — only displays if changeover occurred)**

| Check Item | Response Type | Notes |
|-----------|--------------|-------|
| Previous product allergen profile | Checkbox list (Milk, Soy, Wheat, Tree Nut, Peanut, Egg, Fish, Shellfish, Sesame, None) | |
| Current product allergen profile | Checkbox list | |
| Allergen changeover cleaning SOP followed | Pass / Fail | Reference SOP-SAN-005 |
| Allergen swab test performed on 3+ product contact surfaces | Pass / Fail | Minimum 3 swab locations per validation protocol |
| Allergen swab results — all negative | Pass / Fail + text for details | Fail: re-clean entire line, re-swab, do not start |
| Visual inspection for residual allergenic material | Pass / Fail | |
| Previous product labels removed from line | Pass / Fail | |

**Section 3: Sanitizer and Chemical Verification**

| Check Item | Response Type | Notes |
|-----------|--------------|-------|
| Sanitizer type in use | Dropdown (Quat, Peracetic Acid, Chlorine, Other) | |
| Sanitizer concentration verified by test strip/titration | Pass / Fail + numeric (ppm) | Target per chemical supplier recommendation |
| Concentration within acceptable range | Auto-calculated | Based on sanitizer type and target range |
| Chemical storage area secure and organized | Pass / Fail | |
| No chemical containers in production zone | Pass / Fail | |
| Hand-wash station sanitizer dispensers functioning | Pass / Fail | |
| Foot bath solution fresh and at correct concentration (if applicable) | Pass / Fail / N/A | |

**Section 4: Facility and Environment**

| Check Item | Response Type | Notes |
|-----------|--------------|-------|
| No evidence of pest activity (droppings, gnaw marks, live/dead insects) | Pass / Fail | Fail: stop, notify pest control, document, QA assessment |
| Hand-wash stations stocked (soap, sanitizer, paper towels, signage) | Pass / Fail | |
| Employee personal hygiene compliance observed (hair nets, gloves, no jewelry, clean uniforms) | Pass / Fail | |
| No condensation dripping from ceiling, pipes, or HVAC onto product zones | Pass / Fail | Fail: address source, wipe down, assess contamination risk |
| Floor drains clean and flowing (no standing water) | Pass / Fail | |
| Lighting adequate and all bulbs/shields intact | Pass / Fail | |
| Waste containers emptied and lined | Pass / Fail | |
| Temperature of production area within spec (if climate-controlled) | Pass / Fail + numeric (F/C) | |

**Section 5: Sign-Off**

| Field | Type |
|-------|------|
| Overall pre-op result | Pass / Fail (auto-calculated: Fail if any critical item fails) |
| Inspector signature (name confirmation) | Text + timestamp |
| QC verification signature | Text + timestamp |
| Corrective actions taken (if any fails) | Long text |
| Corrective action verified by QC | Pass / N/A |
| Production authorized to start | Yes / No (QC decision) |

---

## 2. GMP Audit Checklist

### Purpose
Internal GMP audit conducted monthly by QA to verify ongoing compliance with 21 CFR 117 Subpart B (Current Good Manufacturing Practice) and GFSI scheme requirements. Findings feed into the CAPA system.

### Form Structure

**Header:**
- Audit Date
- Auditor Name
- Area(s) Audited (multi-select: Receiving, Warehouse, Batching, Filling, Packaging, QC Lab, Sanitation, Shipping, Exterior)
- Audit Type (Routine Monthly, Follow-up, For-Cause)

**Section 1: Facility Maintenance and Construction**

| Item | Response | Scoring |
|------|----------|---------|
| Floors in good repair (no cracks, holes, peeling coatings) | Compliant / Minor NC / Major NC / Critical NC | 10/7/3/0 |
| Walls and ceilings smooth, cleanable, in good repair | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Doors and windows properly sealed (no gaps for pest entry) | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Lighting adequate for tasks performed (50 FC production, 20 FC warehouse) | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Light shields/protective covers intact over production areas | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Ventilation adequate, air flow from clean to less clean areas | Compliant / Minor / Major / Critical | 10/7/3/0 |
| No flaking paint, rust, or loose material above product zones | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Drains functioning properly, no backflow potential | Compliant / Minor / Major / Critical | 10/7/3/0 |

**Section 2: Employee Practices**

| Item | Response | Scoring |
|------|----------|---------|
| Hair restraints properly worn (covers all hair, beard nets where needed) | Compliant / Minor / Major / Critical | 10/7/3/0 |
| No jewelry (rings, watches, earrings, piercings visible) | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Clean outer garments appropriate for work area | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Proper handwashing observed (upon entry, after breaks, after touching face/hair) | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Glove usage and change frequency appropriate | Compliant / Minor / Major / Critical | 10/7/3/0 |
| No eating, drinking, tobacco use in production/warehouse areas | Compliant / Minor / Major / Critical | 10/7/3/0 |
| No personal belongings in production areas | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Illness reporting procedures followed (no visibly ill employees working) | Compliant / Minor / Major / Critical | 10/7/3/0 |

**Section 3: Chemical Storage and Control**

| Item | Response | Scoring |
|------|----------|---------|
| Chemicals stored in designated, locked area separate from production | Compliant / Minor / Major / Critical | 10/7/3/0 |
| All chemical containers labeled (contents, concentration, hazards) | Compliant / Minor / Major / Critical | 10/7/3/0 |
| SDS (Safety Data Sheets) available and current | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Chemical inventory log maintained and accurate | Compliant / Minor / Major / Critical | 10/7/3/0 |
| No food-grade and non-food-grade chemicals stored together | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Dispensing equipment clean and dedicated per chemical | Compliant / Minor / Major / Critical | 10/7/3/0 |

**Section 4: Pest Control**

| Item | Response | Scoring |
|------|----------|---------|
| Pest control devices (ILTs, traps, bait stations) in place per map | Compliant / Minor / Major / Critical | 10/7/3/0 |
| No evidence of pest activity (interior) | Compliant / Minor / Major / Critical | 10/7/3/0 |
| No evidence of pest activity (exterior — within 10 feet of building) | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Exterior doors and dock seals properly sealed | Compliant / Minor / Major / Critical | 10/7/3/0 |
| No harborage conditions (clutter, standing water, exposed waste) | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Pest control service reports current and reviewed | Compliant / Minor / Major / Critical | 10/7/3/0 |

**Section 5: Waste Management**

| Item | Response | Scoring |
|------|----------|---------|
| Waste containers adequate in number and size | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Waste containers lined, covered, and emptied regularly | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Waste disposal area clean, not attracting pests | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Waste not accumulating in production or warehouse areas | Compliant / Minor / Major / Critical | 10/7/3/0 |
| Recycling and waste streams properly segregated | Compliant / Minor / Major / Critical | 10/7/3/0 |

**Scoring Summary (auto-calculated in linked Sheet):**
- Total possible points
- Points scored
- Percentage score
- Rating: Excellent (>90%), Good (80-90%), Needs Improvement (70-80%), Unacceptable (<70%)
- Auto-generated CAPA required if any Critical NC or score <80%

---

## 3. SQF Audit Preparation Checklist

### Purpose
Used by QA to systematically verify readiness before an SQF certification or surveillance audit. Organized by SQF Code Edition 9 modules.

### Form Structure (Abbreviated — Key Modules)

**Module 2: Food Safety and Quality Management System**

| Check | Status | Evidence Location | Gap/Action Needed |
|-------|--------|------------------|-------------------|
| Food safety and quality policy current, signed by senior management | Ready / Gap / In Progress | Quality Manual (link) | Text |
| Management responsibility and organizational chart current | Ready / Gap / In Progress | QM Section 2 | Text |
| Management review conducted within last 12 months | Ready / Gap / In Progress | MR minutes (link) | Text |
| Document control procedure current, all docs within review cycle | Ready / Gap / In Progress | Document register | Text |
| Record management and retention policy implemented | Ready / Gap / In Progress | SOP-QA-001 | Text |
| Complaint management system operational with trend analysis | Ready / Gap / In Progress | Complaint register | Text |
| Internal audit program — all elements audited within cycle | Ready / Gap / In Progress | Audit schedule + reports | Text |
| CAPA system — all open CAPAs within SLA | Ready / Gap / In Progress | CAPA register | Text |
| Training program — all personnel current on required training | Ready / Gap / In Progress | Training matrix | Text |
| Approved supplier program — all suppliers approved and current | Ready / Gap / In Progress | ASL + supplier files | Text |

**Module 11: Food Safety Fundamentals (HACCP)**

| Check | Status | Evidence Location | Gap/Action Needed |
|-------|--------|------------------|-------------------|
| HACCP team identified with qualifications documented | Ready / Gap / In Progress | HACCP plan Section 1 | Text |
| Product descriptions current for all products | Ready / Gap / In Progress | HACCP plan Section 2 | Text |
| Intended use and consumer identified | Ready / Gap / In Progress | HACCP plan Section 3 | Text |
| Flow diagrams current and verified on-site | Ready / Gap / In Progress | HACCP plan Section 4 | Text |
| Hazard analysis conducted for all biological, chemical, physical, radiological hazards | Ready / Gap / In Progress | HACCP plan Section 5 | Text |
| CCPs identified with scientific justification | Ready / Gap / In Progress | HACCP plan Section 6 | Text |
| Critical limits established with validation evidence | Ready / Gap / In Progress | Process authority letter | Text |
| CCP monitoring procedures implemented and records current | Ready / Gap / In Progress | Batch records + CCP logs | Text |
| Corrective action procedures for CCP deviations documented | Ready / Gap / In Progress | SOP-FS-003 | Text |
| Verification activities conducted (CCP record review, calibration, testing) | Ready / Gap / In Progress | Verification schedule + records | Text |
| HACCP plan reassessment completed within last 12 months | Ready / Gap / In Progress | Reassessment record | Text |

**Module 11: Allergen Management**

| Check | Status | Evidence Location | Gap/Action Needed |
|-------|--------|------------------|-------------------|
| Allergen management plan documented | Ready / Gap / In Progress | SOP-FS-012 | Text |
| Allergen risk assessment for all products current | Ready / Gap / In Progress | Allergen matrix | Text |
| Production scheduling minimizes allergen changeovers | Ready / Gap / In Progress | Production schedule | Text |
| Allergen changeover cleaning validated and documented | Ready / Gap / In Progress | Validation report | Text |
| Allergen labeling verified for all products | Ready / Gap / In Progress | Label approval files | Text |
| Supplier allergen declarations on file and current | Ready / Gap / In Progress | Supplier COAs/declarations | Text |
| Employee training on allergen awareness current | Ready / Gap / In Progress | Training records | Text |

**Module 11: Product Identification and Traceability**

| Check | Status | Evidence Location | Gap/Action Needed |
|-------|--------|------------------|-------------------|
| Lot coding system provides full traceability | Ready / Gap / In Progress | SOP-QA-015 | Text |
| Mock recall conducted within last 6 months | Ready / Gap / In Progress | Mock recall report | Text |
| Mock recall achieved 100% trace within 4 hours (SQF target) | Ready / Gap / In Progress | Mock recall results | Text |
| Product identification maintained throughout production | Ready / Gap / In Progress | Batch records | Text |
| Rework/reprocessed product traceability maintained | Ready / Gap / In Progress | Rework log | Text |

**Summary Dashboard (linked Sheet):**
- Total items checked
- Ready / Gap / In Progress counts and percentages
- Gap list with responsible person and target close date
- Days until scheduled audit
- Risk assessment: Ready for audit / At risk / Not ready

---

## 4. Incoming Material Inspection Form

### Purpose
Completed by receiving personnel for every incoming shipment of raw materials, packaging materials, and ingredients. Captures critical data for traceability and supplier quality monitoring.

### Form Fields

**Shipment Information:**

| Field | Type | Notes |
|-------|------|-------|
| Date Received | Date (auto-populated) | |
| PO Number | Text | Cross-reference to purchase order |
| Supplier Name | Dropdown (from approved supplier list) | |
| Carrier | Text | Trucking company |
| Bill of Lading # | Text | |
| Seal Number (if sealed load) | Text + photo upload | Verify matches BOL |
| Seal Intact | Yes / No | No: document, photograph, notify QA |

**Material Information:**

| Field | Type | Notes |
|-------|------|-------|
| Material Description | Dropdown (from raw material master) | |
| Material Code | Auto-populated from selection | |
| Supplier Lot Number | Text | From supplier label/COA |
| Internal Receiving Lot | Auto-generated | Format: RL-YYYYMMDD-### |
| Quantity Received | Number + unit (lbs, kg, gal, each, pallets) | |
| Quantity Ordered | Auto-populated from PO | |
| Quantity Match | Auto-calculated (within tolerance?) | |

**Quality Checks:**

| Check | Response Type | Criteria |
|-------|--------------|---------|
| Temperature on receipt | Numeric (F or C) | Refrigerated: <41F; Frozen: <0F; Ambient: per spec |
| Temperature acceptable | Auto-calculated | Green/Red based on material spec |
| Packaging integrity (no damage, tears, leaks, dents) | Pass / Fail + photo | Fail: document damage, assess contamination risk |
| Labeling correct (material name, lot, allergens, storage) | Pass / Fail | Fail: hold, contact supplier |
| COA received with shipment | Yes / No | No: request from supplier; conditional release with 24hr deadline |
| COA reviewed — meets specification | Pass / Fail / Pending | QC completes this field |
| Allergen declaration on COA matches approved specification | Pass / Fail / N/A | Fail: reject, SCAR |
| Sample retained for QC testing | Yes / No + sample ID | Required for all ingredients |
| Organoleptic evaluation (appearance, odor — where applicable) | Pass / Fail | |

**Disposition:**

| Field | Type | Notes |
|-------|------|-------|
| Disposition Decision | Accept / Reject / Hold / Conditional Accept | |
| Reject Reason (if rejected) | Text + dropdown (damage, temp abuse, wrong material, COA fail, spec fail) | |
| Hold Reason (if held) | Text | Pending COA, pending QC test, pending investigation |
| Storage Location Assigned | Dropdown (warehouse zones) | |
| Inspector Name | Dropdown + timestamp | |
| QC Reviewer (if required) | Dropdown + timestamp | Required for holds and conditional accepts |

---

## 5. Environmental Monitoring Sampling Form

### Purpose
Documents the collection of environmental samples (swabs, sponges, air plates) for microbiological testing. Maintains chain of custody from sample collection to lab result entry.

### Form Fields

**Sampling Event Information:**

| Field | Type | Notes |
|-------|------|-------|
| Sampling Date | Date | |
| Sampling Time | Time | |
| Sampling Event Type | Dropdown: Routine Schedule, Post-Sanitation, Post-Construction, Intensified (post-positive), For-Cause | |
| Collector Name | Dropdown from trained sampler list | Only trained personnel may collect EM samples |
| Production Status | Dropdown: Pre-Op, During Production, Post-Production, Idle | |

**Sample Details (repeating section — one per sample):**

| Field | Type | Notes |
|-------|------|-------|
| Sample ID | Auto-generated: EM-YYYYMMDD-### | Unique per sample |
| Sample Location ID | Dropdown from location master (e.g., L1-FN-01 = Line 1, Filler Nozzle #1) | |
| Location Description | Auto-populated from location master | |
| Zone | Auto-populated: 1, 2, 3, or 4 | |
| Sample Type | Dropdown: Sponge Swab, Cotton Swab, Contact Plate, Air Plate, Water Sample | |
| Test Requested | Multi-select: Listeria spp., Salmonella, Coliform/E. coli, APC, Yeast & Mold | |
| Sample Condition | Pass / Fail (visual integrity of sample collection) | |
| Notes | Text | Any observations during collection |

**Lab Submission:**

| Field | Type | Notes |
|-------|------|-------|
| Lab Name | Dropdown: Internal Lab, [External Lab Name] | |
| Lab Submission ID | Text | Lab's tracking number |
| Date/Time Submitted | DateTime | |
| Chain of Custody | Confirmed (checkbox) | Samples maintained under proper conditions during transport |

**Results Entry (completed when results return):**

| Field | Type | Notes |
|-------|------|-------|
| Result Date | Date | |
| Listeria spp. Result | Negative / Presumptive Positive / Confirmed Positive / Not Tested | |
| Salmonella Result | Negative / Presumptive Positive / Confirmed Positive / Not Tested | |
| Coliform / E. coli Result | Numeric (CFU) or Negative / Not Tested | |
| APC Result | Numeric (CFU) / Not Tested | |
| Yeast & Mold Result | Numeric (CFU) / Not Tested | |
| Overall Result | Pass / Fail (auto-calculated against limits by zone) | |
| Corrective Action Required | Yes / No (auto-flagged if any Fail) | |
| Corrective Action Reference | Text (CAPA number if escalated) | |

---

## 6. Production Line Clearance Checklist

### Purpose
Completed before every product changeover and at the start of each production run. Verifies that the correct product is being produced with the correct materials, labels, and codes. Prevents one of the most common quality failures in food manufacturing: mislabeling and cross-contamination.

### Form Fields

**Header:**

| Field | Type |
|-------|------|
| Date | Date |
| Production Line | Dropdown |
| Shift | Dropdown |
| Previous Product Run | Dropdown from production schedule |
| Current Product to be Run | Dropdown from production schedule |
| Lead Operator | Dropdown |
| QC Verifier | Dropdown |

**Section 1: Allergen Changeover Verification**

| Check | Response | Notes |
|-------|----------|-------|
| Is this an allergen changeover? (previous product allergens differ from current) | Yes / No (auto-determined from product profiles) | |
| If yes — allergen changeover cleaning completed per SOP-SAN-005 | Pass / Fail / N/A | |
| Allergen swab results negative | Pass / Fail / N/A | |
| All previous product removed from line (ingredient totes, WIP, finished product) | Pass / Fail | |

**Section 2: Label Verification**

| Check | Response | Notes |
|-------|----------|-------|
| Correct label loaded (product name matches production order) | Pass / Fail | Compare label to production schedule |
| UPC/barcode scans correctly (verify with scanner) | Pass / Fail | Scan and verify against master data |
| Ingredient statement correct (matches current approved artwork) | Pass / Fail | Compare to approved label proof |
| Allergen declaration correct | Pass / Fail | Cross-reference with formula allergen profile |
| Nutritional panel correct | Pass / Fail | Compare to approved Nutrition Facts |
| Net quantity declaration correct | Pass / Fail | Verify matches container size |
| All previous product labels removed from label applicator and line area | Pass / Fail | No wrong labels accessible on the line |

**Section 3: Coding Verification**

| Check | Response | Notes |
|-------|----------|-------|
| Date code format correct (per SOP-QA-020) | Pass / Fail | Example: BB SEP 04 2027 |
| Best-by date calculated correctly | Pass / Fail | Production date + shelf life |
| Lot code correct (matches batch record) | Pass / Fail | Format: YYYYMMDD-LINE-SEQ |
| Plant code correct | Pass / Fail | |
| Code placement on container correct | Pass / Fail | Legible, correct location per spec |
| Code legibility acceptable (not smeared, faded, misaligned) | Pass / Fail | |
| Inkjet/laser printer head clean and functioning | Pass / Fail | |

**Section 4: First-Article Inspection**

| Check | Response | Notes |
|-------|----------|-------|
| First container off the line inspected | Pass / Fail | |
| Fill level/volume correct (within specification) | Pass / Fail + numeric | Measured by QC |
| Cap/lid torque or seam dimensions correct | Pass / Fail + numeric | Measured by QC |
| Metal detector / X-ray verification with test standards | Pass / Fail | Test with Fe, Non-Fe, SS test pieces |
| Checkweigher calibrated and rejecting out-of-spec units | Pass / Fail | |
| Overall first article — approved for production run | Pass / Fail | Must be Pass to continue |

**Section 5: Sign-Off**

| Field | Type |
|-------|------|
| All checks passed | Auto-calculated |
| Lead Operator confirmation | Name + timestamp |
| QC Verifier confirmation | Name + timestamp |
| Line authorized for production | Yes / No |
| If No — corrective actions required | Text |
| Re-verification after corrective action | Pass / Fail / N/A |

---

## Forms-to-Sheets Automation for Trend Analysis

### Architecture

```
Google Form (data collection on floor)
  |
  v
Google Sheet (linked response sheet)
  |
  v
Apps Script (data processing, alerting, cleanup)
  |
  v
Summary Tabs (pivot tables, charts, KPI calculations)
  |
  v
Looker Studio Dashboard (management visibility)
```

### Automated Processing Steps

1. **Form submission triggers Apps Script** that:
   - Validates data completeness
   - Sends immediate alerts for critical findings (email and/or Google Chat)
   - Assigns corrective action tasks (creates entries in a corrective action tracker Sheet)
   - Updates running tallies and KPIs

2. **Nightly batch processing** (time-driven Apps Script trigger):
   - Consolidates daily data into weekly/monthly summary tabs
   - Calculates trend metrics (rolling averages, rate changes)
   - Flags anomalies (statistical process control rules)
   - Generates automated weekly summary email to QA Director

3. **Looker Studio dashboards** connected to summary tabs:
   - Pre-op pass rate by line, shift, week
   - GMP audit score trending (monthly)
   - Incoming material rejection rate by supplier
   - Environmental monitoring positive rate by zone
   - Line clearance first-pass rate
   - Open corrective actions aging report

### Data Retention

- Form responses retained in Sheets for minimum 3 years (active)
- Annual archival: previous year's data copied to archive Sheet, original responses retained
- Archived Sheets stored in designated retention folder with Drive labels
- Data available for FDA inspection, SQF audit, and customer audit requests throughout retention period

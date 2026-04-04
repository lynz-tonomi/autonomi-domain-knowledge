# Excel/SharePoint Batch Record Templates for Beverage Manufacturing

## Overview

Batch records are the single most critical quality document in beverage manufacturing. They provide complete traceability from raw materials through finished product release and must satisfy FDA requirements under 21 CFR 117 (CGMP for human food), 21 CFR 113/114 (thermally processed and acidified foods), and GFSI scheme requirements (SQF, BRC, FSSC 22000). This reference covers the structure, content, and electronic implementation of batch records in Microsoft 365.

---

## Master Batch Record (MBR) Components

The MBR is the approved template from which production batch records are generated. It is a controlled document managed through the document control workflow.

### 1. Batch Record Header

| Field | Description | Data Source |
|-------|------------|-------------|
| Product Name | Full product name as registered | Product master data |
| SKU / Item Number | Unique stock-keeping unit | ERP / product master |
| Batch Number | Unique identifier: format `YYYYMMDD-LINE-SEQ` (e.g., 20260404-L2-001) | Auto-generated |
| Production Date | Date batch is manufactured | Operator entry |
| Production Line | Line designation (L1, L2, L3) | Operator selection |
| Shift | Day / Swing / Night (or A / B / C) | Operator selection |
| Scheduled Start Time | Planned production start | Production schedule |
| Actual Start Time | When batching actually begins | Operator entry |
| Actual End Time | When packaging is complete | Operator entry |
| Batch Size (Target) | Target batch volume in gallons or liters | Formula card |
| Batch Size (Actual) | Actual batch volume produced | Operator entry |
| Lead Operator | Person responsible for the batch | Operator sign-in |
| QC Technician on Duty | QC person assigned to the line | QC assignment |
| Supervisor on Duty | Production supervisor | Shift roster |

### 2. Bill of Materials (BOM) with Target and Actual Weights

**Column Structure:**

| Column | Type | Description |
|--------|------|-------------|
| Line # | Auto | Sequential ingredient line |
| Ingredient Name | Text | Full ingredient name per specification |
| Ingredient Code | Text | Internal raw material code (RM-###) |
| Supplier | Text | Approved supplier name |
| Lot Number | Text | Supplier lot or internal receiving lot |
| COA Reference | Link | Link to filed Certificate of Analysis |
| Allergen Flag | Choice | None, Milk, Soy, Tree Nut, Wheat, Egg, Fish, Shellfish, Sesame, Peanut |
| Target Weight (kg) | Number | Calculated from formula card x batch size |
| Actual Weight (kg) | Number | Operator entry from scale readout |
| Variance (%) | Calculated | `=ABS(Actual-Target)/Target*100` |
| Variance Acceptable | Calculated | Conditional: Green if <=2%, Yellow if 2-5%, Red if >5% |
| Scale ID | Text | Identifier of scale used for weighing |
| Operator Initials | Text | Person who weighed the ingredient |
| Verified By | Text | Second person verification (4-eyes principle for CCPs) |
| Time Weighed | DateTime | Timestamp of weighing activity |

**Variance Tolerance Rules:**
- Flavors and colors: +/- 2% (tight tolerance — impacts sensory)
- Acids and pH adjusters: +/- 1% (CCP-related for acidified foods)
- Sweeteners: +/- 2% (impacts Brix specification)
- Water: adjusted to make up total batch weight (balancing ingredient)
- Preservatives: +/- 5% but must remain above minimum effective concentration
- Vitamins/minerals (if fortified): +/- 2% of label claim overage target

### 3. Processing Steps with CCP Monitoring

| Column | Description |
|--------|-------------|
| Step # | Sequential processing step |
| Process Step Description | Detailed instruction for this step |
| Equipment | Equipment ID used for this step |
| Target Parameter | Specification for this step (temp, time, speed, pressure) |
| Critical Limit (if CCP) | Absolute limit that must not be exceeded/subceeded |
| Actual Reading | Operator-recorded actual value |
| Time of Reading | Timestamp |
| Within Spec? | Auto-calculated pass/fail |
| Operator | Person performing the step |
| Verifier | Person verifying CCP steps (independent verification required) |
| Deviation? | Y/N — if Y, deviation log entry required |
| Notes | Free text for observations |

**Typical Processing Steps for Beverage:**

1. Water treatment verification (UV, filtration, chlorine level)
2. Ingredient staging and weighing (per BOM above)
3. Dry ingredient pre-mix (if applicable)
4. Batch tank fill — add water to target volume
5. Add ingredients per sequence (order matters for solubility and stability)
6. Agitation — speed and duration per formula
7. pH adjustment — **CCP for acidified foods** (target pH and verification)
8. Brix adjustment — target Brix +/- tolerance
9. Thermal processing — **CCP** (temperature and hold time)
10. Cooling to filling temperature
11. Carbonation (if applicable) — CO2 volumes target
12. Transfer to filler bowl / holding tank
13. Filling and sealing — **CCP** (container closure integrity for shelf-stable)
14. Coding (date code, lot code, line ID)
15. Packaging (case packing, palletizing)
16. Pallet tagging and warehouse staging

### 4. In-Process Quality Checks

| Parameter | Method | Frequency | Target | Tolerance | Action if OOS |
|-----------|--------|-----------|--------|-----------|---------------|
| Brix | Digital refractometer | Every batch + every 2 hours during fill | Per spec (e.g., 11.5) | +/- 0.3 | Hold and adjust |
| pH | Calibrated pH meter | Every batch + every 2 hours | Per spec (e.g., 3.4) | +/- 0.1 | Hold; if CCP, deviation procedure |
| Temperature (pasteurizer outlet) | RTD sensor (continuous) + manual verification | Continuous chart + manual every 30 min | Per process authority letter | Per process authority | Divert; deviation procedure |
| Fill Volume | Gravimetric or volumetric check | Every 15 minutes (5 units) | Per spec (e.g., 355 mL) | +/- 3 mL | Adjust filler; evaluate last 15 min production |
| Carbonation (CO2 volumes) | Zahm & Nagel or in-line sensor | Every 30 minutes | Per spec (e.g., 3.0 volumes) | +/- 0.2 | Adjust carbonator |
| Dissolved Oxygen (DO) | In-line or portable DO meter | Every hour | Per spec (e.g., <1 ppm) | Max limit only | Investigate source; purge lines |
| Color | Spectrophotometer or visual against standard | Per batch | Per spec (L*a*b* values or visual) | Per spec | Investigate; adjust if within process window |
| Taste / Sensory | Trained panel or QC evaluation | Per batch | Matches reference standard | Pass/fail | Hold for expanded evaluation |
| Container Closure | Torque meter (caps), seam teardown (cans), dye test (seals) | Every 30 minutes + line start + after jam/stop | Per closure spec | Per closure spec | Stop line; evaluate product since last good check |
| Net Weight / Volume | Checkweigher (continuous) + manual verification | Continuous + manual every 30 min | Per labeled net quantity | Per NIST Handbook 133 | Adjust filler; MAV (Maximum Allowable Variance) assessment |

### 5. Packaging Records

| Field | Description |
|-------|-------------|
| Container Type | Bottle/can/carton specification (e.g., 12oz aluminum can, 202 lid) |
| Container Lot | Supplier lot number for containers |
| Lid/Cap Lot | Supplier lot number for closures |
| Label Lot | Supplier lot number for labels (or print plate ID for printed cans) |
| Shrink/Tray Lot | Secondary packaging material lot |
| Case/Tray Configuration | Units per case (e.g., 24-pack, 12-pack) |
| Total Units Filled | Counter reading (start and end) |
| Rejected Units | By reject type: under-fill, over-fill, no-fill, label defect, closure defect, metal detect reject |
| Yield (%) | `=(Total Units Filled - Rejected Units) / (Batch Size / Unit Volume) * 100` |
| Expected Yield Range | Typically 96-99% for well-run beverage line |
| Yield Variance Investigation | Required if yield <95% or >101% (over-yield suggests under-filling) |
| Cases Produced | Total cases packed |
| Pallets Produced | Total pallets built |
| Pallet IDs | Unique pallet tag numbers for warehouse tracking |

### 6. CCP Records (Critical Control Points)

#### Thermal Process Record (21 CFR 113 / 21 CFR 114)

| Field | Requirement |
|-------|------------|
| Process Authority | Name and contact of process authority who filed the scheduled process |
| Scheduled Process | Minimum temperature and hold time (e.g., 185F for 15 seconds) |
| Equipment ID | Pasteurizer/retort identifier |
| Recorder Chart # | Continuous temperature recording chart number or electronic file reference |
| Initial Temperature | Product temperature entering the holding tube |
| Holding Tube Outlet Temperature | Temperature at the exit of the holding tube — must meet or exceed scheduled process |
| Flow Rate / Pump Speed | Must not exceed the maximum rate used in process filing |
| Deviation Procedure | Reference to documented deviation procedure |
| Chart Reviewed By | QC signature confirming chart review within 1 business day |
| Deviations Noted | Any temperature drops below scheduled process — each documented with time, duration, corrective action |

#### Acidification Record (21 CFR 114 — Acidified Foods)

| Field | Requirement |
|-------|------------|
| Equilibrium pH Target | Per process filing (e.g., pH <= 4.6, typically targeting <= 4.2 with safety margin) |
| pH at Acidification | pH measured after acid addition, before thermal process |
| pH at Filling | pH measured at point of fill (must be <= target) |
| pH Meter Calibration | Documented calibration with pH 4.0 and 7.0 buffers, before and after each batch |
| Acid Type and Concentration | Specific acid used (citric, phosphoric, malic) and concentration |

### 7. Sanitation Records

**Pre-Operational Inspection:**

| Checkpoint | Pass/Fail | Corrective Action if Fail |
|-----------|-----------|--------------------------|
| All product contact surfaces visually clean | | Re-clean and re-inspect |
| No previous product residue | | Re-clean; allergen swab if changeover |
| Sanitizer concentration verified (test strip or titration) | | Adjust concentration; retest |
| Allergen swab results (if applicable) | | Re-clean; re-swab until negative |
| No condensation dripping onto product zone | | Address source; wipe down |
| No evidence of pest activity | | Notify pest control; do not start production |
| Hand-wash stations stocked | | Restock before start |
| Foot baths charged (if applicable) | | Recharge solution |

**CIP (Clean-in-Place) Verification:**

| Parameter | Target | Actual | Verified By |
|-----------|--------|--------|-------------|
| Rinse water temperature | Per SOP | | |
| Caustic concentration (%) | Per SOP (typ. 1.5-2.5%) | | |
| Caustic temperature | Per SOP (typ. 140-160F) | | |
| Caustic contact time (min) | Per SOP (typ. 15-20 min) | | |
| Acid concentration (%) | Per SOP (typ. 0.5-1.0%) | | |
| Acid temperature | Per SOP | | |
| Acid contact time (min) | Per SOP | | |
| Final rinse water quality | Conductivity/pH within spec | | |
| ATP swab result (RLU) | Pass threshold (e.g., <150 RLU) | | |

### 8. Deviation Log

Any deviation from the batch record instructions must be documented:

| Field | Description |
|-------|-------------|
| Step # Reference | Which batch record step was deviated from |
| Time of Deviation | When it was discovered |
| Description | What happened — factual, specific |
| Immediate Action | What was done to contain/correct |
| Impact Assessment | Did this affect food safety? Product quality? |
| Product Disposition | Product produced during deviation: hold, release, reject |
| Reported To | Supervisor, QA, Food Safety (as applicable) |
| NCR/CAPA Reference | If escalated, reference number |
| Operator Signature | Person documenting the deviation |
| QA Review Signature | QA review and disposition decision |

### 9. Release Checklist

The batch is not released for shipment until all items on the release checklist are verified:

| # | Verification Item | Status | Verified By | Date |
|---|-------------------|--------|-------------|------|
| 1 | All CCP records complete and within critical limits | | | |
| 2 | All in-process QC checks complete and within specification | | | |
| 3 | Micro hold results received — all within specification | | | |
| 4 | Sensory evaluation — pass (matches reference standard) | | | |
| 5 | Label verification — correct product, correct code, legible | | | |
| 6 | Net weight/volume compliance — meets NIST Handbook 133 | | | |
| 7 | Container closure integrity verified | | | |
| 8 | All batch record pages complete — no blank fields | | | |
| 9 | All deviations documented and dispositioned | | | |
| 10 | Retained samples collected and stored | | | |
| 11 | COAs on file for all ingredients used | | | |
| 12 | Allergen controls verified (if allergen changeover occurred) | | | |
| 13 | Environmental monitoring results acceptable (no Zone 1/2 positives) | | | |
| 14 | Batch record reviewed and signed by QA | | | |

**Release Authority:**
- QA Technician completes initial review and verification
- QA Manager (or designee) provides final release signature
- No product ships without both signatures

---

## Electronic Batch Record (EBR) Considerations

### 21 CFR Part 11 Compliance Requirements

The FDA's rule on electronic records and electronic signatures applies to all records required by FDA regulations. For batch records implemented in Excel/SharePoint:

**Electronic Signatures:**
- Each signature event must be linked to the signer's unique Azure AD identity
- Signing requires authentication at the moment of signing (username + password or MFA)
- Signatures must include the printed name, date/time, and meaning (e.g., "reviewed by", "approved by", "performed by")
- Power Automate approval actions with Azure AD authentication satisfy this requirement when properly configured

**Audit Trails:**
- Every change to a batch record field must be logged with: who changed it, when, the old value, the new value, and why
- SharePoint version history provides document-level audit trail
- SharePoint Lists with versioning enabled provide item-level audit trail
- Custom Power Automate flows can provide field-level audit trail by logging changes to a separate audit log list
- Audit trails must be retained for the same period as the batch record itself
- Audit trail records must be protected from modification or deletion

**Access Controls:**
- Only authorized personnel can create, modify, or sign batch records
- Role-based access: operators can enter data in designated fields; supervisors can verify; QA can review and release; document control can modify templates
- System administrator access must be logged and periodically reviewed
- Production operators should not have the ability to modify batch record templates

**Data Integrity (ALCOA+ Principles):**

| Principle | Implementation |
|-----------|---------------|
| Attributable | Azure AD identity linked to every entry |
| Legible | Standardized data entry formats, dropdowns where possible |
| Contemporaneous | Timestamps from system clock (not manually entered) |
| Original | First-entry data preserved in audit trail |
| Accurate | Validation rules, range checks, calculated fields |
| Complete | Required fields enforced; no blank fields accepted at release |
| Consistent | Same template used across all batches of same product |
| Enduring | SharePoint retention policies; backed up per IT DR plan |
| Available | Accessible for review throughout retention period |

### Power Apps Integration for Production Floor

**Mobile Data Entry App Design:**

- **Offline-capable** — operators enter data even when Wi-Fi is down; syncs when connection restores
- **Barcode scanning** — scan ingredient lot numbers, container lot numbers, equipment IDs
- **Scale integration** — connect to RS-232 or USB scales for direct weight capture (eliminates transcription errors)
- **Photo capture** — document visual observations, deviations, sanitation checks
- **Timer functions** — built-in timers for process hold times, CIP contact times
- **Validation rules** — immediate alerts for out-of-spec entries (fill volume, temperature, pH)
- **Guided workflow** — steps presented sequentially; operators cannot skip ahead
- **Electronic signature** — PIN or biometric authentication for sign-off steps
- **Dashboard view** — real-time batch status visible to supervisors and QA

**Data Flow:**

```
Power Apps (production floor)
  |
  v
SharePoint List (structured data) + SharePoint Library (batch record PDF)
  |
  v
Power Automate (triggers for OOS alerts, review routing)
  |
  v
Power BI (real-time production dashboard, batch analytics)
```

### Template Management

- Master batch record templates stored in SharePoint library `10-Templates/Batch Records/`
- Each product SKU has its own MBR: `MBR-SKU12345_ProductName_v3.0.xlsx`
- Template revision follows document control workflow (review, approve, train before use)
- When a new batch is started, the operator initiates from the current approved MBR
- The batch-specific record is saved to: `02-Production/Batch Records/YYYY/MM/BatchNumber.xlsx`
- Completed batch records are locked (check-in with no check-out permitted) after QA release

### Reporting and Analytics

**Power BI Batch Record Dashboard:**
- Yield trending by product, line, shift
- OOS rate by parameter (Brix, pH, fill volume, etc.)
- CCP deviation frequency and severity
- First-pass release rate (released without any hold or rework)
- Batch cycle time (start to release) vs target
- Ingredient variance trending (identifies calibration drift or operator issues)
- Right-first-time (RFT) percentage by product and operator
- Cost per batch trending (ingredient cost + labor + utilities + waste)

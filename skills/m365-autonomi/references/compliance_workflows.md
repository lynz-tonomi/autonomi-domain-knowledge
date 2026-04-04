# Power Automate Compliance Workflows for F&B

## Overview

Six core compliance workflows implemented in Power Automate for Autonomi's food and beverage operations. Each workflow is designed for auditability (21 CFR Part 11), traceability, and integration with SharePoint document control, Teams notifications, and Power BI trend analysis.

---

## 1. CAPA (Corrective and Preventive Action) Workflow

### Initiation Triggers

A CAPA can be initiated from any of the following sources:

| Source | Trigger Mechanism | Auto-Classification |
|--------|------------------|---------------------|
| Customer complaint | Complaint form escalation (severity >= 3) | Corrective |
| Internal audit finding | Audit report SharePoint item creation | Corrective or Preventive |
| External audit finding (SQF, FDA, customer) | Manual initiation by QA | Corrective |
| Non-conformance report | NCR escalation (recurring or critical) | Corrective |
| Process deviation | Deviation report closure triggers review | Corrective |
| Trend analysis alert | Power BI threshold trigger | Preventive |
| Management review action item | Meeting minutes action item | Preventive |
| Near-miss or observation | Employee-submitted observation form | Preventive |

### Workflow Stages

**Stage 1 — Initiation (Day 0)**
- Initiator completes CAPA Request Form (SharePoint list item)
- Required fields: source, description, affected product(s), affected lot(s), risk assessment (severity x likelihood), proposed classification (corrective/preventive/both)
- Auto-assigned CAPA number: `CAPA-YYYY-###` (sequential per year)
- QA Director notified via Teams adaptive card within 1 hour

**Stage 2 — Assignment and Investigation (Days 1-5)**
- QA Director assigns investigation lead and cross-functional team
- Investigation lead has 5 business days for initial investigation
- Required investigation tools and documentation:
  - **5-Why Analysis** — iterative root cause questioning; minimum 3 levels, documented in CAPA form
  - **Fishbone / Ishikawa Diagram** — categories for F&B: Materials, Methods, Manpower, Machines, Measurement, Mother Nature (Environment)
  - **Process flow review** — walk the process to identify where the system failed
  - **Data analysis** — pull relevant batch records, CCP logs, environmental monitoring data, complaint history
- Investigation findings documented in SharePoint with supporting evidence attached

**Stage 3 — Root Cause Determination (Days 5-10)**
- Investigation lead proposes root cause(s) with supporting evidence
- QA Director reviews and approves root cause determination
- If root cause is inadequate, QA returns to investigation lead with specific questions
- Root cause categories tracked for trend analysis:
  - Personnel (training gap, human error, staffing)
  - Process (SOP inadequate, process capability, design flaw)
  - Equipment (malfunction, calibration, maintenance)
  - Material (supplier issue, specification, storage)
  - Environment (temperature, humidity, contamination)
  - Management system (document control, communication, resource allocation)

**Stage 4 — Corrective/Preventive Action Plan (Days 10-15)**
- Investigation lead proposes action items with:
  - Specific action description
  - Responsible person
  - Target completion date
  - Required resources/budget (if applicable)
  - Affected documents requiring revision
- QA Director approves action plan
- Each action item becomes a Planner task assigned to responsible person
- Interim containment actions documented and tracked separately

**Stage 5 — Implementation (Variable timeline)**
- Action owners execute assigned tasks
- Progress updates required weekly via Planner
- Overdue tasks trigger escalation: Day 1 overdue to action owner, Day 3 to their manager, Day 7 to QA Director
- Document revisions processed through document control workflow
- Training on revised procedures tracked through training acknowledgment flow

**Stage 6 — Effectiveness Verification (30-90 days after implementation)**
- Effectiveness check scheduled automatically based on risk level:
  - Critical: 30 days
  - Major: 60 days
  - Minor: 90 days
- Verification methods: data review, audit, observation, re-testing
- Effectiveness criteria defined at action plan stage (measurable outcomes)
- If ineffective, CAPA re-opened and returned to Stage 3

**Stage 7 — Closure (Upon successful effectiveness verification)**
- Investigation lead submits closure request with effectiveness evidence
- QA Director reviews and approves closure
- Electronic signature captured (Azure AD authenticated)
- CAPA record locked (no further edits without new revision)
- Closure notification sent to all stakeholders
- Data fed to Power BI CAPA dashboard for KPI tracking

### CAPA KPIs (Power BI Dashboard)

- Open CAPAs by age, department, source, classification
- Average days to closure by risk level
- On-time closure rate (target: >90%)
- Effectiveness verification pass rate (target: >85%)
- Top 5 root cause categories (rolling 12 months)
- CAPA volume trend (monthly, rolling 12 months)
- Recurring CAPAs (same root cause within 12 months — flags systemic issue)

---

## 2. Non-Conformance Reporting (NCR) Workflow

### NCR Categories for F&B

**Incoming Material Non-Conformance:**
- Ingredient fails specification (Brix, pH, micro, foreign material, color, flavor)
- Packaging material defect (dents, seal integrity, print quality, dimensions)
- Missing or non-conforming COA (Certificate of Analysis)
- Temperature abuse during transit (cold chain break)
- Allergen mislabeling or undeclared allergen on supplier documentation
- Short shipment or wrong material received

**In-Process Non-Conformance:**
- CCP deviation (temperature, pH, Brix out of critical limits)
- Process parameter deviation (fill volume, carbonation, dissolved O2)
- Foreign material detection (metal detector, X-ray, visual)
- Equipment malfunction during production
- Sanitation failure (positive environmental swab, failed pre-op inspection)
- Labeling error (wrong label, missing info, incorrect lot code)

**Finished Product Non-Conformance:**
- Failed QC release testing (micro, chemical, physical, sensory)
- Packaging defect found during warehouse inspection
- Shelf life failure (accelerated or real-time)
- Customer return/rejection

### Disposition Workflow

```
NCR Created (SharePoint List item)
  |
  v
QA evaluates and assigns disposition:
  |
  +-- ACCEPT AS-IS (minor deviation, no food safety/quality impact)
  |     Justification required, QA Manager approval
  |
  +-- REWORK (can be brought into spec)
  |     Rework instruction documented
  |     Post-rework re-inspection required
  |     New batch record section for rework activities
  |
  +-- REGRADE (can be used for different product/specification)
  |     Regrading authorization from QA Manager
  |     Product relabeled and re-inspected
  |
  +-- HOLD (pending further investigation or testing)
  |     Physical hold tag placed (warehouse notified)
  |     Hold period and review date established
  |     No shipment permitted until disposition resolved
  |
  +-- REJECT / DESTROY (cannot be salvaged)
  |     Destruction witnessed and documented
  |     Environmental disposal compliance verified
  |
  +-- RETURN TO VENDOR (incoming material NC)
        Supplier notified via SCAR workflow
        RMA (Return Material Authorization) obtained
        Credit/replacement tracked in procurement
```

### Documentation Requirements

Every NCR must include:
- Date and time of detection
- Product name, SKU, lot/batch number, quantity affected
- Description of non-conformance with photos where applicable
- Immediate containment action taken
- Root cause (for in-process and finished product NCs)
- Disposition decision with justification
- Signature of person making disposition decision
- Follow-up actions and CAPA reference (if escalated)
- Cost of quality impact (scrap value, rework labor, investigation time)

### Escalation Rules

| Condition | Escalation |
|-----------|-----------|
| Food safety risk identified | Immediate notification to Food Safety Manager + QA Director |
| Allergen-related NC | Immediate hold; recall assessment within 4 hours |
| Same NC type occurs 3x in 30 days | Auto-generate CAPA |
| NC value exceeds $5,000 | Notify VP Operations and CFO |
| Customer-facing NC (shipped product) | Notify Sales + Customer Service within 2 hours |

---

## 3. Customer Complaint Handling Workflow

### Intake Form (Power Apps or SharePoint)

**Required Fields:**
- Complainant name, company, contact info
- Product name, SKU, UPC
- Lot code / best-by date / production code
- Purchase location and date
- Complaint type: Foreign material, Off-flavor/odor, Texture, Appearance, Packaging defect, Illness/injury, Labeling, Other
- Detailed description (free text)
- Photo upload (up to 5 images)
- Severity auto-classification based on complaint type:
  - **Critical (Severity 5):** Illness/injury claim, allergen issue, foreign material posing injury risk
  - **Major (Severity 3-4):** Quality defect affecting usability, repeated complaints on same lot
  - **Minor (Severity 1-2):** Cosmetic issue, single occurrence, no safety concern

### Investigation and Response SLA

| Severity | Acknowledgment | Investigation | Resolution | Escalation |
|----------|---------------|---------------|------------|------------|
| Critical (5) | 4 hours | 24 hours | 3 business days | VP Quality + Legal immediately |
| Major (3-4) | 24 hours | 5 business days | 10 business days | QA Director at day 5 |
| Minor (1-2) | 48 hours | 10 business days | 15 business days | QA Manager at day 10 |

### Investigation Steps

1. Lot code trace — pull batch record, ingredient lots, CCP data, QC results
2. Production environment review — environmental monitoring results for that production date
3. Retained sample evaluation — pull and test retained sample from same lot
4. Distribution check — identify all customers who received the affected lot
5. Complaint history search — any prior complaints on same product, lot, or complaint type
6. Root cause determination and corrective action (CAPA if warranted)

### Trend Analysis Triggers (Power BI)

- 3+ complaints on same product in 30 days → auto-alert to QA Director
- 2+ complaints on same lot → immediate hold investigation
- Any illness/injury complaint → FDA MedWatch assessment, potential reportable event
- Complaint rate exceeds 1 per 100,000 units → product review triggered
- Seasonal trend analysis (monthly complaint rate by product family)

### Response and Resolution

- Customer receives written response (template in SharePoint, personalized per case)
- Replacement product or refund processed per customer service policy
- Complaint record linked to CAPA if systemic issue identified
- All complaint records retained for 5 years minimum
- Annual complaint summary presented at management review

---

## 4. Supplier SCAR (Supplier Corrective Action Request) Workflow

### Issue Identification Sources

- Incoming material NCR (rejected lot, failed COA verification)
- Audit finding from supplier audit
- Repeated minor deviations (3+ in 12 months)
- Customer complaint traced to supplier material
- Specification non-conformance

### SCAR Process Flow

```
Issue identified → QA creates SCAR (SharePoint)
  |
  v
SCAR number assigned: SCAR-YYYY-###
  |
  v
SCAR sent to supplier via automated Outlook email
  - Includes: issue description, affected lot(s), evidence (photos, test results)
  - Supplier response deadline: 10 business days
  |
  v
Supplier submits response (via SharePoint external sharing or email)
  - Required: root cause analysis, corrective actions, preventive actions, timeline
  |
  v
QA reviews supplier response
  +-- Adequate → Accept response, monitor implementation
  +-- Inadequate → Return with specific questions, 5 additional business days
  |
  v
Implementation verification
  - Review next 3 shipments for conformance
  - Request updated documentation (SOP revisions, test data)
  |
  v
SCAR closure and supplier scorecard update
```

### Supplier Scorecard Integration

SCARs feed into the quarterly supplier scorecard:

| Metric | Weight | Scoring |
|--------|--------|---------|
| Quality (NCR rate) | 30% | <1% = 100, 1-3% = 75, 3-5% = 50, >5% = 25 |
| Delivery (on-time, in-full) | 25% | >98% = 100, 95-98% = 75, 90-95% = 50, <90% = 25 |
| SCAR responsiveness | 15% | On-time response = 100, Late = 50, No response = 0 |
| Documentation (COA accuracy) | 15% | >99% = 100, 95-99% = 75, <95% = 50 |
| Price competitiveness | 15% | Indexed to market benchmark |

**Scorecard Actions:**
- Score 90-100: Preferred supplier, eligible for volume increases
- Score 75-89: Approved supplier, standard terms
- Score 60-74: Probationary, improvement plan required, dual sourcing initiated
- Score <60: Supplier disqualification review, alternative sourcing mandatory

---

## 5. Environmental Monitoring (EM) Workflow

### Sampling Schedule Trigger

Power Automate triggers EM sampling based on:
- **Calendar schedule** — pre-defined sampling plan (weekly, monthly per zone)
- **Event-based** — post-sanitation verification, post-construction, post-maintenance
- **Escalation-based** — increased sampling after positive result

### Zone Classification

| Zone | Description | Sampling Frequency | Examples |
|------|------------|-------------------|----------|
| Zone 1 | Direct product contact surfaces | Per production run | Filler nozzles, blending tank interior, conveyor belts |
| Zone 2 | Adjacent to product contact (within 1 meter) | Weekly | Equipment frames, splash guards, operator gloves |
| Zone 3 | Non-product contact within production area | Monthly | Floors, drains, walls, ceilings, doorframes |
| Zone 4 | Remote areas outside production | Quarterly | Hallways, locker rooms, loading dock, offices |

### Result Entry and Alert Escalation

```
Lab submits results to SharePoint List (or technician enters on-site via Power Apps)
  |
  v
Power Automate evaluates result against limits:
  |
  +-- NEGATIVE / WITHIN SPEC → Record filed, dashboard updated
  |
  +-- PRESUMPTIVE POSITIVE → Alert to QA and Sanitation within 1 hour
  |     Enhanced cleaning of affected area
  |     Re-sample within 24 hours
  |     Confirmation testing initiated
  |
  +-- CONFIRMED POSITIVE (Zone 1 or 2) → CRITICAL ALERT
  |     Food Safety Manager notified immediately
  |     Product hold assessment (affected lots identified)
  |     Root cause investigation initiated (CAPA if confirmed)
  |     Intensive sampling plan activated (daily for 2 weeks)
  |     Sanitation corrective action documented
  |
  +-- CONFIRMED POSITIVE (Zone 3 or 4) → ELEVATED ALERT
        Sanitation Manager notified within 4 hours
        Enhanced cleaning of affected area and adjacent zones
        Re-sample within 48 hours
        Trend review: any pattern with this location?
```

### Organisms of Concern for Beverage Manufacturing

| Organism | Significance | Testing Method | Action Level |
|----------|-------------|---------------|--------------|
| Listeria spp. / L. monocytogenes | Pathogen indicator / pathogen | Environmental swab → enrichment → PCR | Any positive = critical response |
| Salmonella | Pathogen | Environmental swab → enrichment → PCR | Any positive = critical response |
| Total coliform / E. coli | Sanitation indicator | Swab → Petrifilm or plating | Zone 1: any detect; Zone 2: >10 CFU |
| Aerobic plate count (APC) | General cleanliness | Swab → Petrifilm | Zone 1: >100 CFU/surface; Zone 2: >500 CFU |
| Yeast and mold | Spoilage indicator | Swab → YM Petrifilm | Zone 1: >50 CFU; product-specific limits |

### Trend Analysis (Power BI)

- Heat map of positive results by zone and location over 12 months
- Sanitation effectiveness tracking (pre-op vs post-op APC levels)
- Seasonal patterns (summer moisture, construction activity impacts)
- Corrective action closure rate for EM-related CAPAs

---

## 6. Change Control Workflow

### Change Request Initiation

Any change that could impact food safety, product quality, regulatory compliance, or customer requirements must go through change control:

**Change Categories:**
- **Formulation** — ingredient substitution, supplier change, specification change
- **Process** — equipment modification, process parameter change, new production line
- **Packaging** — material change, supplier change, design change, label change
- **Facility** — construction, layout modification, utility change
- **System** — software update, calibration method change, testing method change
- **Supplier** — new supplier qualification, existing supplier facility change
- **Regulatory** — new regulation, updated standard, customer requirement change

### Impact Assessment Matrix

| Impact Area | Assessment Questions | Assessor |
|------------|---------------------|----------|
| Food Safety | Does this change affect the hazard analysis? CCPs? Prerequisite programs? | Food Safety Manager |
| Quality | Does this affect product specifications? Shelf life? Sensory? | QA Manager |
| Regulatory | Does this affect labeling? Nutritional facts? Claims? Registrations? | Regulatory Affairs |
| Customer | Does any customer specification or agreement reference the item being changed? | Sales/Account Manager |
| Production | Does this affect production procedures? Equipment? Throughput? | Production Manager |
| Supply Chain | Does this affect ingredient sourcing? Lead times? Costs? | Procurement Manager |
| Training | Do personnel need retraining on new procedures or equipment? | Training Coordinator |

### Approval Routing Logic

```
Change Request submitted (SharePoint)
  |
  v
Auto-assigned CC number: CC-YYYY-###
  |
  v
Impact assessment routed to all assessors (parallel, 5 business days)
  |
  v
Risk level determined based on assessments:
  |
  +-- LOW RISK (no food safety/regulatory/customer impact)
  |     Approved by Department Manager
  |
  +-- MEDIUM RISK (quality impact, no food safety/regulatory)
  |     Approved by QA Director
  |
  +-- HIGH RISK (food safety, regulatory, or customer impact)
  |     Approved by QA Director + VP Operations
  |     Customer notification may be required
  |     Regulatory assessment may require new filing
  |
  v
Implementation plan with timeline and verification steps
  |
  v
Implementation executed per plan
  |
  v
Post-implementation verification (30-60 days)
  - Confirm change achieved intended outcome
  - No unintended consequences
  - All affected documents updated
  - All affected personnel trained
  |
  v
Change control closed
```

### Change Control Register

All change controls tracked in a SharePoint List with:
- CC number, title, description
- Requestor, date requested
- Category, risk level
- Impact assessment results
- Approval status and approver(s)
- Implementation status and target date
- Verification status and date
- Related documents (revised SOPs, specs, etc.)
- Related CAPAs (if change originated from CAPA)

### Integration Points

- **Document Control** — revised documents processed through document control workflow
- **CAPA** — changes originating from CAPA cross-referenced
- **Supplier Management** — supplier changes trigger supplier re-qualification
- **Training** — personnel training needs identified and tracked
- **Customer Communication** — customer-impacting changes trigger notification workflow
- **Regulatory** — regulatory-impacting changes flagged for pre-market assessment

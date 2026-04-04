# Google Drive Document Management for F&B

## Shared Drive Structure

Autonomi's quality management system lives in Google Shared Drives organized by functional area. Each Shared Drive has defined membership, access levels, and content governance rules.

### Top-Level Shared Drives

| Drive Name | Purpose | Primary Content |
|-----------|---------|-----------------|
| 01-Quality System | QMS foundation documents | Quality Manual, QMS procedures, internal audit, management review, document control |
| 02-Production | Manufacturing operations | Batching/filling/packaging SOPs, work instructions, batch records, production schedules |
| 03-Food Safety | HACCP and prerequisite programs | HACCP plan, prerequisite programs, allergen management, recall procedures, food defense |
| 04-R&D | Formulation and innovation | Formulations (CONFIDENTIAL), trial reports, scale-up protocols, sensory evaluation |
| 05-Supply Chain | Procurement and supplier management | Supplier approval files, purchasing specifications, COAs, receiving procedures |
| 06-Sales & Marketing | Commercial operations | Customer specifications, sales collateral, marketing claims substantiation |
| 07-Finance | Financial documentation | Cost analyses, budgets, capital expenditure requests (linked to QBO for live data) |
| 08-Regulatory | Compliance and registrations | FDA registrations, state licenses, labeling files, nutritional analysis, claims dossiers |

### Sub-Folder Conventions

Within each Shared Drive, organize with a maximum of 3 folder levels:

```
[Shared Drive]/
  [Document Type]/
    [Product Line or Department or Process Area]/
      files...
```

**Example: 02-Production**
```
02-Production/
  SOPs/
    Batching/
      SOP-PROD-001_Receiving_Raw_Materials_v2.0.gdoc
      SOP-PROD-002_Ingredient_Staging_v1.0.gdoc
      SOP-PROD-003_Batching_and_Blending_v3.0.gdoc
    Filling/
      SOP-PROD-010_Hot_Fill_Line_Operation_v2.0.gdoc
      SOP-PROD-011_Can_Line_Operation_v1.0.gdoc
    Packaging/
      SOP-PROD-020_Case_Packing_v1.0.gdoc
  Work Instructions/
    Batching/
      WI-PROD-001a_Scale_Calibration_Check_v1.0.gdoc
      WI-PROD-003a_CIP_Pasteurizer_v2.0.gdoc
    Filling/
      WI-PROD-010a_Filler_Bowl_Changeover_v1.0.gdoc
  Forms/
    FRM-PROD-001_Batch_Record_Template_v4.0.gsheet
    FRM-PROD-010_Line_Clearance_Checklist_v2.0.gsheet
  Batch Records/
    2026/
      04/
        20260401-L1-001_OatMilk_Original.gsheet
        20260401-L2-001_ColdBrew_Classic.gsheet
  Schedules/
    Production_Schedule_2026_Q2.gsheet
```

**Example: 05-Supply Chain**
```
05-Supply Chain/
  Supplier Approval/
    Active Suppliers/
      SUP-001_Acme_Ingredients/
        Supplier_Questionnaire.gdoc
        Audit_Report_2025.gdoc
        Approval_Form.gdoc
        COAs/
          (individual COA files)
    Pending Approval/
    Disqualified/
  Specifications/
    Raw Materials/
      SPEC-RM-001_Organic_Cane_Sugar_v2.0.gdoc
      SPEC-RM-002_Citric_Acid_FCC_v1.0.gdoc
    Packaging Materials/
      SPEC-PKG-001_12oz_Aluminum_Can_v1.0.gdoc
  Receiving/
    SOP-SC-001_Incoming_Material_Receiving_v2.0.gdoc
    FRM-SC-001_Incoming_Inspection_Form.gform
```

---

## Naming Conventions

### File Naming Format

```
TYPE-DEPT-###_Document_Title_vX.X.extension
```

**Components:**

| Component | Format | Example |
|-----------|--------|---------|
| TYPE | 2-4 letter prefix | SOP, WI, FRM, SPEC, POL, QM, EXT, TRN |
| DEPT | 2-5 letter department code | QA, PROD, FS, RD, SC, REG, MAINT, SAN, WH |
| ### | 3-digit sequential number | 001, 015, 042 |
| Document_Title | Underscored descriptive title | Batching_and_Blending, CIP_Pasteurizer |
| vX.X | Version number | v1.0 (first release), v2.0 (second release), v2.1 (minor edit) |
| extension | File type | .gdoc, .gsheet, .gform, .pdf |

**Rules:**
- Use underscores (_) in titles, not spaces (improves URL handling and scripting)
- Title case for document titles
- Version in file name matches version in document header
- Never reuse a document number, even after obsolescence
- Google-native files (.gdoc, .gsheet) preferred over uploaded Office files for collaboration

### Folder Naming Format

- Top-level: numbered prefix for sort order (01-, 02-, etc.)
- Sub-folders: descriptive name, no numbering unless sort order matters
- No special characters except hyphens and underscores

---

## Google Docs for SOPs and Work Instructions

### Template-Based Authoring

All SOPs and WIs are created from organization-approved templates stored in the Template Gallery:

**SOP Template Structure:**
1. **Header block** — document number, title, effective date, revision number, page X of Y
2. **Approval table** — author, reviewer(s), approver, with dates and electronic signatures
3. **Revision history table** — version, date, description of changes, author
4. **Purpose** — why this procedure exists
5. **Scope** — what it covers and what it does not
6. **Definitions** — key terms used in the document
7. **Responsibilities** — who does what (roles, not names)
8. **References** — related documents (cross-linked with bookmarks)
9. **Procedure** — numbered steps with sub-steps
10. **Records** — what records are generated by this procedure
11. **Appendices** — forms, flowcharts, diagrams

**Formatting Standards:**
- Font: Arial 11pt for body, Arial 14pt bold for headings
- Automatic Table of Contents at document start (Docs native TOC)
- Numbered headings (1.0, 1.1, 1.2, 2.0, etc.)
- Tables for structured data (no inline CSV-style text)
- Images/photos captioned with figure numbers
- Page breaks between major sections
- Header: document number and title on every page
- Footer: "CONTROLLED DOCUMENT — printed copies are uncontrolled" + page number

### Automatic TOC and Cross-References

- Google Docs native heading styles (Heading 1, 2, 3) drive automatic TOC generation
- Cross-references between documents use direct hyperlinks to specific headings (bookmarks)
- When a referenced document is revised, the link remains valid (Google Docs URLs are stable)
- Quarterly link audit recommended: Apps Script can crawl documents and verify all hyperlinks resolve

---

## Version History Management

### Hybrid Approach for Regulated Documents

**Native Google Docs Version History:**
- Automatically tracks every edit with editor identity and timestamp
- Useful for collaboration during drafting — see who changed what and when
- "Name this version" feature pins key milestones (e.g., "Submitted for Review", "Approved v2.0")
- Versions can be viewed and restored (restoration creates a new version, preserving history)

**Manual Version Numbering (Regulatory Requirement):**
- Official version number maintained in document header and file name
- Major versions (v1.0, v2.0) for approved releases requiring training
- Minor versions (v1.1, v1.2) for editorial corrections not affecting procedures (typos, formatting)
- Version number incremented only upon formal approval through the document control process
- Revision history table in the document records all version changes

**Reconciliation Process:**
- When a document is approved, Document Control:
  1. Names the version in Google Docs history (e.g., "APPROVED v2.0 — 2026-04-04")
  2. Updates the version number in the document header and file name
  3. Updates the revision history table
  4. Locks editing permissions (removes Editors, sets to Commenters or Viewers)
  5. Generates a PDF snapshot for archival in the approved documents folder

---

## Sharing and Permissions

### Shared Drive Access Levels

| Level | Capabilities | Typical F&B Role |
|-------|-------------|------------------|
| Manager | Add/remove members, move files between drives, delete | Document Control, IT Admin |
| Content Manager | Add/edit/move/delete files, approve access requests | QA Director, Department Managers |
| Contributor | Add and edit files, cannot move or delete | Supervisors, SMEs drafting documents |
| Commenter | View and comment only | Reviewers during document review cycle |
| Viewer | View only, no comments | Operators, External Auditors |

### External Sharing Restrictions

- **Proprietary formulations** (04-R&D): external sharing completely disabled at the Drive level
- **Customer specifications** (06-Sales & Marketing): view-only sharing with specific customer contacts, expiring links
- **Audit documents**: view-only sharing with auditor's organizational Google account during audit window; access revoked within 48 hours post-audit
- **Supplier documents** (COAs, specifications): shared with specific supplier contacts for verification; contributor access on their own supplier folder for COA uploads
- **Default policy**: external sharing disabled at the organizational level; exceptions require QA Director approval

### Link Sharing Policies

- **Never use "Anyone with the link"** for controlled documents — this is unauditable
- **Restricted (specific people only)** is the default for all QMS documents
- **Domain-wide sharing** acceptable for general reference documents (employee handbook, cafeteria menu)
- **Download/copy/print restrictions** applied to confidential documents via Google Drive IRM (Information Rights Management)

---

## Approval Workflow Implementation

### Option 1: Apps Script Custom Workflow

A Google Apps Script bound to the document or triggered from a Sheets-based document register:

```
Author marks document "Ready for Review" in register
  |
  v
Apps Script triggers:
  - Sends email to assigned reviewers with document link
  - Sets document permission to "Commenter" for reviewers
  - Creates calendar event for review deadline
  |
  v
Reviewers add comments in suggestion mode
  - All suggestions tracked with reviewer identity
  |
  v
Author resolves comments, updates document
  |
  v
Author marks "Ready for Approval" in register
  |
  v
Apps Script triggers:
  - Sends email to Approver with document link
  - Approver clicks "Approve" link → runs script that:
    - Captures approver identity and timestamp
    - Updates approval table in document
    - Updates register status to "Approved"
    - Names the version in Docs history
    - Triggers training acknowledgment workflow
  |
  v
Training acknowledgment:
  - Affected personnel receive email with document link
  - Click acknowledgment link → logged in training register (Sheets)
  - Overdue acknowledgments trigger reminder emails at day 3, escalation at day 5
```

### Option 2: Third-Party Add-Ons

- **DocuSign for Google Workspace** — provides legally binding electronic signatures with full audit trail; suitable for regulatory submissions and customer-facing documents
- **SignRequest** — cost-effective e-signature solution for internal approvals
- **Collavate** — purpose-built document approval workflow for Google Workspace with routing, reminders, and audit trail
- **AODocs** — enterprise document management layer on top of Google Drive with compliance-grade workflows

### Document Acknowledgment Tracking via Google Forms

For training acknowledgment after SOP revision:

1. Google Form created with fields: employee name, employee ID, document number, document title, revision number, acknowledgment statement ("I have read and understand this document"), date
2. Form pre-filled with document information via URL parameters
3. Email sent to affected personnel with pre-filled form link
4. Responses collected in a Sheets-based training register
5. Apps Script monitors for overdue acknowledgments and sends reminders
6. Compliance dashboard shows acknowledgment completion percentage by document and department

---

## Archival and Retention

### Google Drive Labels

Drive labels (available in Business Standard and above) enable classification and retention management:

| Label Field | Values | Purpose |
|------------|--------|---------|
| Document Type | Quality Manual, Policy, SOP, WI, Form, Spec, External, Training | Classification |
| Department | QA, Production, Food Safety, R&D, Supply Chain, Regulatory, etc. | Ownership |
| Status | Draft, Under Review, Approved, Effective, Obsolete | Lifecycle stage |
| Confidentiality | Public, Internal, Confidential, Restricted | Access control |
| Retention Period | 2 Years, 3 Years, 5 Years, 7 Years, Permanent | Retention management |
| Review Date | Date field | Triggers review reminders |
| Effective Date | Date field | Official effective date |

### Retention Rules

Labels drive automated retention:
- Files labeled "Obsolete" with retention period of "5 Years" are automatically flagged for disposition review when the 5-year clock expires
- Disposition review notification sent to Document Control and QA Director
- Files cannot be permanently deleted until retention period expires and disposition is approved
- Litigation hold overrides retention rules when applied

### Archival Process for Obsolete Documents

1. Document reaches end of life (replaced by new revision or no longer needed)
2. Document Control updates status to "Obsolete"
3. PDF snapshot generated and stored in `_Archive` folder within the Shared Drive
4. Original Google Doc permissions set to "Viewer" for all (prevents edits)
5. File moved to `_Archive/[Year]` folder
6. File name prepended with `OBSOLETE_` prefix
7. Retention clock starts based on label values
8. File remains searchable and viewable for the retention period

---

## Cross-Referencing Between Documents

### Bookmark and Hyperlink Strategy

- Every major section heading in every SOP has a named bookmark
- Cross-references use direct hyperlinks to these bookmarks: `https://docs.google.com/document/d/DOC_ID/edit#bookmark=id.BOOKMARK_ID`
- When a document is revised, existing bookmarks are preserved (maintaining link integrity)
- New bookmarks added for new sections
- Quarterly link audit script crawls all documents in the QMS drives and reports broken links

### Document Register (Master List)

A Google Sheets document register serves as the master index:

| Column | Content |
|--------|---------|
| Document Number | TYPE-DEPT-### |
| Title | Full document title |
| Type | SOP, WI, FRM, etc. |
| Department | Owning department |
| Current Version | e.g., v2.0 |
| Status | Draft, Under Review, Approved, Effective, Obsolete |
| Effective Date | Date current version became effective |
| Next Review Date | Effective + 12 months (auto-calculated) |
| Owner | Document owner (SME) |
| Approver | Person who approved current version |
| Google Doc Link | Direct link to the Google Doc |
| PDF Archive Link | Link to approved PDF snapshot |
| Change Summary | Brief description of last revision |
| Training Required | Yes/No |
| Training Complete | % of affected personnel acknowledged |

---

## Template Gallery

### Standard F&B Document Templates

Maintained in a dedicated Shared Drive folder `10-Templates/`:

| Template | Format | Description |
|----------|--------|-------------|
| SOP Template | Google Doc | Standard SOP layout with all required sections, header/footer, formatting |
| Work Instruction Template | Google Doc | Step-by-step instruction format with photo placeholders, safety callouts |
| Specification Template | Google Doc | Raw material, packaging, and finished product spec format with acceptance criteria |
| CAPA Form | Google Doc | Investigation form with 5-Why, fishbone, action plan, effectiveness verification |
| Change Control Form | Google Doc | Change request with impact assessment matrix, approval routing |
| Non-Conformance Report | Google Doc | NCR form with disposition options, root cause, corrective action |
| Supplier Questionnaire | Google Doc | Pre-qualification questionnaire covering food safety, quality, capacity |
| Audit Report Template | Google Doc | Internal/external audit report with findings, observations, OFIs |
| Management Review Template | Google Doc | Agenda-based template covering all required MR inputs per SQF/ISO |
| Batch Record Template | Google Sheet | Production batch record with BOM, processing steps, CCP, QC checks |
| Training Record | Google Sheet | Employee training log with competency tracking |
| Document Register | Google Sheet | Master document list (described above) |

### Template Usage Rules

- Templates are stored in a read-only folder; users create copies, never edit the original
- Template version is tracked in the template file name and revision history table
- Template changes go through document control (they are controlled documents)
- Apps Script can auto-create new documents from templates with pre-filled metadata
- All templates include a "Template Instructions" section (highlighted in yellow) that authors delete before submitting for review

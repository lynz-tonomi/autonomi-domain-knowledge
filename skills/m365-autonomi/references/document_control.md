# SharePoint Document Control for F&B

## Document Hierarchy

The quality management system follows a four-tier document hierarchy standard across FDA-regulated and GFSI-certified food and beverage operations:

### Tier 1 — Quality Manual (QM)
- Top-level document defining the organization's quality policy, food safety policy, and QMS scope
- References applicable standards (SQF Code Edition 9, 21 CFR 117, 21 CFR 113/114 for thermal processing)
- Approved by executive leadership (CEO/COO) and Quality Director
- Reviewed annually or upon significant organizational change
- Typically a single document: `QM-001 Autonomi Quality & Food Safety Manual`

### Tier 2 — Standard Operating Procedures (SOPs)
- Define **what** must be done, **who** is responsible, and **when** it applies
- Department-specific with cross-references to related SOPs
- Written by subject matter experts, reviewed by department managers, approved by QA Director
- Examples: `SOP-QA-001 Document Control`, `SOP-PROD-003 Batching and Blending`, `SOP-FS-012 Allergen Management`

### Tier 3 — Work Instructions (WIs)
- Step-by-step **how-to** instructions for specific tasks
- Include photos, diagrams, decision trees where applicable
- Written by supervisors or experienced operators, reviewed by department managers
- Examples: `WI-PROD-015 CIP Procedure for Pasteurizer`, `WI-SAN-008 Allergen Changeover Cleaning`

### Tier 4 — Forms, Records, and Logs
- Blank forms used to capture data; completed forms become records
- Forms are controlled documents (template revision managed); records are evidence of activity
- Examples: `FRM-FS-003 Pre-Operational Inspection Checklist`, `FRM-QA-021 CAPA Investigation Form`

---

## Document Numbering Convention

### Format: `TYPE-DEPT-###`

**Document Type Prefixes:**

| Prefix | Type | Description |
|--------|------|-------------|
| QM | Quality Manual | Top-level quality/food safety manual |
| POL | Policy | Policy statements (allergen, recall, food defense) |
| SOP | Standard Operating Procedure | Departmental procedures |
| WI | Work Instruction | Task-level step-by-step instructions |
| FRM | Form | Blank templates for data capture |
| SPEC | Specification | Raw material, packaging, finished product specs |
| EXT | External Document | Third-party documents (customer specs, regulations) |
| TRN | Training Material | Training presentations, competency assessments |
| DWG | Drawing | Equipment layouts, process flow diagrams |

**Department Codes:**

| Code | Department |
|------|-----------|
| QA | Quality Assurance |
| PROD | Production / Manufacturing |
| FS | Food Safety |
| RD | Research & Development |
| SC | Supply Chain / Procurement |
| REG | Regulatory Affairs |
| MAINT | Maintenance / Engineering |
| SAN | Sanitation |
| WH | Warehouse / Logistics |
| HR | Human Resources |
| FIN | Finance |
| SM | Sales & Marketing |

**Numbering Rules:**
- Sequential within each TYPE-DEPT combination
- Numbers are never reused — retired documents retain their number permanently
- Related documents share a base number with letter suffixes: `SOP-PROD-003` has child WIs `WI-PROD-003a`, `WI-PROD-003b`
- Specifications use a product/material code instead of sequential number when practical: `SPEC-RM-042` (raw material #42)

---

## Version Control and Approval Workflow

### Document Lifecycle States

```
DRAFT (v0.1, v0.2, ...)
  |
  v
UNDER REVIEW (routed to reviewers)
  |
  v
PENDING APPROVAL (routed to approver)
  |
  v
APPROVED / EFFECTIVE (v1.0, v2.0, ...)
  |
  v
TRAINING REQUIRED (acknowledgment period)
  |
  v
FULLY EFFECTIVE (training complete)
  |
  v  (at scheduled review date)
UNDER REVISION → loops back to DRAFT
  |
  v  (when replaced or no longer needed)
OBSOLETE (archived, read-only, watermarked)
```

### SharePoint Implementation

**Minor Versions (0.1, 0.2, 0.3):**
- Used during drafting and revision
- Visible only to contributors and document control
- Check-in/check-out enforced to prevent concurrent edits
- Draft comments captured in version history

**Major Versions (1.0, 2.0, 3.0):**
- Published upon approval — the "effective" version
- Visible to all users with read permissions
- Previous major versions retained but clearly marked as superseded
- Content approval required before major version publish

### Approval Routing via Power Automate

```
Author submits for review
  |
  v
Power Automate triggers on metadata change (Status = "Under Review")
  |
  v
Parallel review assignments sent via Teams adaptive cards
  - Reviewers: SMEs from affected departments
  - Review period: 5 business days (configurable)
  - Reminder at day 3, escalation at day 5
  |
  v
All reviewers approve OR author addresses comments and resubmits
  |
  v
Routed to Approver (QA Director for SOPs, Dept Manager for WIs)
  - Approval includes electronic signature (Azure AD authentication)
  |
  v
Document Control sets effective date and publishes major version
  |
  v
Training acknowledgment flow triggered for affected personnel
  - Training due within 5 business days of effective date
  - Personnel cannot access production areas without current training (enforced by supervisors, tracked in system)
```

---

## SharePoint Library Structure

### Top-Level Document Libraries

| Library Name | Content | Permissions |
|-------------|---------|-------------|
| 01-Quality System | Quality Manual, QMS procedures, management review, internal audit | QA: Edit; All others: Read |
| 02-Production | Batching, filling, packaging SOPs and WIs, production schedules | Prod: Edit; QA: Edit; Others: Read |
| 03-Food Safety | HACCP plan, prerequisite programs, allergen management, recall | FS Team: Edit; QA: Edit; Others: Read |
| 04-Regulatory | FDA registrations, state licenses, labeling compliance, nutritional | Reg: Edit; QA: Read; Others: Restricted |
| 05-Supply Chain | Supplier approval, purchasing specs, COAs, receiving procedures | SC: Edit; QA: Edit; Others: Read |
| 06-R&D | Formulations (CONFIDENTIAL), trial reports, scale-up protocols | R&D: Edit; Exec: Read; Others: No Access |
| 07-Specifications | Raw material specs, packaging specs, finished product specs | QA: Edit; R&D: Contribute; Others: Read |
| 08-Training | Training records, competency matrices, training materials | HR: Edit; Managers: Contribute; Others: Read (own records) |
| 09-External Documents | Customer specifications, regulatory guidance, industry standards | Doc Control: Edit; All: Read |
| 10-Templates | Blank form templates, document templates | Doc Control: Edit; All: Read |

### Sub-Folder Convention

Within each library, organize by:
1. **Document type** (SOPs, WIs, Forms) as the primary sort
2. **Sub-department or process area** as secondary
3. **No nesting beyond 2 levels** — deep nesting breaks SharePoint search and confuses users

Example for 02-Production:
```
02-Production/
  SOPs/
    SOP-PROD-001_Receiving_Raw_Materials.docx
    SOP-PROD-002_Ingredient_Staging.docx
    SOP-PROD-003_Batching_and_Blending.docx
  Work Instructions/
    WI-PROD-001a_Scale_Calibration_Check.docx
    WI-PROD-003a_CIP_Pasteurizer.docx
  Forms/
    FRM-PROD-001_Batch_Record_Template.xlsx
    FRM-PROD-010_Line_Clearance_Checklist.xlsx
```

---

## Metadata and Content Types

### Required Metadata Columns (Site Columns)

| Column | Type | Values / Format | Required |
|--------|------|----------------|----------|
| Document Number | Single line text | TYPE-DEPT-### | Yes |
| Document Title | Single line text | Descriptive title | Yes |
| Document Type | Choice | Quality Manual, Policy, SOP, WI, Form, Spec, External, Training | Yes |
| Department | Choice | QA, Production, Food Safety, R&D, Supply Chain, Regulatory, Maintenance, Sanitation, Warehouse, HR, Finance, Sales | Yes |
| Revision Number | Number | Integer starting at 1 | Yes |
| Effective Date | Date | MM/DD/YYYY | Yes (upon approval) |
| Next Review Date | Date | MM/DD/YYYY | Yes (auto-calculated: effective + 12 months) |
| Document Owner | Person | Author / SME responsible | Yes |
| Approver | Person | Authority who approved current version | Yes |
| Status | Choice | Draft, Under Review, Approved, Effective, Obsolete | Yes |
| Confidentiality | Choice | Public, Internal, Confidential, Restricted | Yes |
| Change Summary | Multi-line text | Description of changes from previous version | Yes (on revision) |

### Content Types

Create SharePoint content types for each document tier to enforce metadata and associate templates:

- **CT_SOP** — inherits from Document; adds SOP-specific metadata; associates SOP template with standard header/footer
- **CT_WorkInstruction** — inherits from Document; adds WI metadata; associates WI template with step-number formatting
- **CT_Form** — inherits from Document; adds form-specific metadata; allows Excel or Word templates
- **CT_Specification** — inherits from Document; adds specification fields (material code, supplier, allergen declarations)

---

## Retention Policies

### FDA Record Retention Requirements

| Record Type | Regulation | Minimum Retention |
|------------|-----------|-------------------|
| Batch/production records | 21 CFR 117.305(b) | 2 years beyond product shelf life |
| Hazard analysis records | 21 CFR 117.305(c) | 2 years beyond superseded |
| Preventive control records | 21 CFR 117.305(d) | 2 years |
| Supplier verification records | 21 CFR 117.305(e) | 2 years |
| Training records | 21 CFR 117.305(f) | 2 years beyond employment |
| Complaint files | 21 CFR 117.315 | Reasonable period |
| Thermal processing records | 21 CFR 113.100(d) | 1 year beyond shelf life (minimum 3 years recommended) |
| LACF container closure records | 21 CFR 113.100(d) | 1 year beyond shelf life |

### SharePoint Retention Implementation

- **Retention labels** applied automatically based on content type and metadata
- **Auto-apply policies** using keyword queries or trainable classifiers
- **Disposition review** — records approaching end of retention trigger review by QA and Legal
- **Litigation hold** capability for records subject to regulatory investigation
- **Records cannot be deleted** during retention period — even by site admins

### Recommended Retention Schedule for Autonomi

| Document Category | Retention Period | Disposition |
|------------------|-----------------|-------------|
| Quality Manual (all versions) | Permanent | Archive |
| SOPs (superseded versions) | 5 years after superseded | Review then destroy |
| Batch records | Shelf life + 2 years | Review then destroy |
| CAPA records | 5 years after closure | Review then destroy |
| Complaint records | 5 years after resolution | Review then destroy |
| Supplier records | Duration of relationship + 3 years | Review then destroy |
| Training records | Duration of employment + 3 years | Review then destroy |
| Internal audit reports | 5 years | Review then destroy |
| Management review minutes | 5 years | Review then destroy |

---

## Access Control Model

### Role-Based Permissions

SharePoint permission levels mapped to F&B roles:

- **Document Control Specialist** — Full Control on all QMS libraries; responsible for publishing, obsoleting, and managing document lifecycle
- **QA Director** — Edit + Approve on Quality System and Food Safety libraries; approval authority for SOPs
- **Department Manager** — Edit within own department library; Read on all others; approval authority for department WIs
- **Supervisor** — Contribute within own department; Read on all others; can submit draft documents for review
- **Operator** — Read on SOPs/WIs for assigned department; cannot access Draft documents; can fill in forms/records
- **External Auditor** — View Only on designated audit libraries; time-limited access (enabled at audit start, disabled at audit close); no download permitted for proprietary documents; activity logged

### Audit Access Protocol

1. Auditor access request submitted by QA Director via Power Automate
2. IT creates time-limited guest account with MFA required
3. SharePoint permissions scoped to audit-relevant libraries only
4. Auditor receives Teams channel invitation for document requests
5. All document access logged via Microsoft 365 audit log
6. Access automatically revoked 48 hours after audit end date
7. Access log exported and filed in audit record

---

## Teams Integration for Document Review

### Document Review Channel Structure

- **#document-review** — General channel for review assignments and status updates
- **Per-review threads** — Each document review gets a dedicated thread with:
  - Document link (SharePoint)
  - Review deadline
  - Reviewer assignments
  - Adaptive card for approve/comment/reject actions
- **@mentions** for reviewer assignments and escalations
- **Tab integration** — Pin the controlled document library as a tab for quick access

### Power Automate Review Notification Flow

```
Trigger: Document Status changed to "Under Review"
  |
  v
Action: Post adaptive card to #document-review
  - Card shows: Doc number, title, change summary, deadline
  - Buttons: Open Document, Approve, Request Changes
  |
  v
Action: Send individual Teams messages to assigned reviewers
  |
  v
Wait: 3 business days
  |
  v
Condition: All reviews complete?
  - Yes → Route to Approver
  - No → Send reminder to outstanding reviewers
  |
  v
Wait: 2 more business days
  |
  v
Condition: Still incomplete?
  - Yes → Escalate to reviewer's manager + QA Director
```

---

## OneDrive Sync Considerations

### Production Facility Offline Access

Many production facilities have limited or unreliable network connectivity. OneDrive sync enables offline access but requires careful management in a controlled document environment:

**Allowed for sync:**
- Published/effective SOPs and WIs (read-only at the user level)
- Reference documents (industry standards, customer specs)
- Training materials

**Prohibited from sync:**
- Draft documents (risk of outdated versions circulating)
- Batch record templates (must be filled online for audit trail integrity)
- Confidential formulations (data loss prevention policy)

**Sync Group Policy Settings:**
- Block sync on unmanaged devices
- Enable Files On-Demand to reduce local storage
- Restrict sync to specific SharePoint libraries via `TenantRestrictions`
- Configure known folder move for standardized user folder structure

### Data Loss Prevention (DLP) Integration

- DLP policies scan for sensitive content types: formulations, supplier pricing, employee PII
- Auto-classification labels applied to documents matching DLP patterns
- External sharing blocked for documents with Confidential or Restricted classification
- Alerts to IT and QA when DLP policy violations detected

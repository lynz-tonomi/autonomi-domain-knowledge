# M365 Integration for F&B — Autonomi

## Summary

Microsoft 365 integration layer for Autonomi's food and beverage operations. Covers SharePoint-based document control for regulated quality systems, Power Automate compliance workflows (CAPA, non-conformance, customer complaints, supplier corrective actions, environmental monitoring, change control), and Excel/SharePoint batch record templates for beverage manufacturing lines. Designed around FDA 21 CFR Part 11 requirements for electronic records, cGMP documentation standards, and SQF/BRC audit readiness.

---

## When to Use

- **Document control operations** — creating, routing, approving, or retiring SOPs, work instructions, forms, and records within a SharePoint-based quality management system
- **Compliance workflow execution** — initiating or managing CAPA, non-conformance reports, customer complaints, supplier SCARs, environmental monitoring investigations, or change control requests through Power Automate
- **Batch record management** — building, filling, reviewing, or releasing electronic batch records in Excel or SharePoint Lists for beverage production runs
- **Audit preparation** — pulling controlled documents, training records, batch records, and compliance logs for SQF, BRC, FDA, or customer audits
- **Regulatory record retrieval** — locating records subject to FDA retention requirements (21 CFR 117, 21 CFR 113/114) or state agency requirements (CDPH, state Dept of Ag)
- **Training acknowledgment tracking** — verifying that personnel have read and acknowledged revised SOPs or new work instructions before the effective date
- **Production floor data integration** — connecting Power Apps mobile data entry to SharePoint Lists or Excel Online for real-time CCP monitoring, in-process checks, and sanitation verification
- **Email-driven quality alerts** — triggering Outlook notifications for out-of-spec results, overdue CAPAs, approaching document review dates, or supplier scorecard thresholds
- **Cross-functional document review** — coordinating multi-department review cycles (QA, Production, R&D, Regulatory, Food Safety) through Teams channels with embedded document links and approval tasks
- **Reporting and trend analysis** — aggregating compliance data from SharePoint Lists into Power BI dashboards for management review, trend monitoring, and continuous improvement

---

## Key Concepts

### SharePoint as QMS Backbone

SharePoint serves as the document management system (DMS) backbone for Autonomi's quality management system. Unlike generic file storage, a food-safe SharePoint deployment requires:

- **Controlled document libraries** with mandatory metadata (document type, department, effective date, review date, revision number, document owner, approver)
- **Content types** mapped to the F&B document hierarchy: Quality Manual, SOPs, Work Instructions, Forms/Records, Specifications, External Documents
- **Check-in/check-out** enforcement to prevent concurrent editing of controlled documents
- **Major/minor versioning** — minor versions for drafts (0.1, 0.2), major versions for approved/effective documents (1.0, 2.0)
- **Retention policies** aligned with FDA requirements: batch records retained for product shelf life + 1 year minimum, some categories 3-5 years, complaint files and CAPA records per 21 CFR 117.315

### Power Automate as Compliance Engine

Power Automate replaces paper-based routing with auditable electronic workflows:

- **Approval flows** with serial or parallel routing, delegation rules for absences, and escalation timers
- **Conditional logic** for risk-based routing — critical CAPAs route to VP Quality, minor findings route to department manager
- **Integration connectors** — SharePoint (document triggers), Outlook (notifications), Teams (adaptive cards for approvals), Planner (task assignment), Power BI (dashboard refresh)
- **Audit trail** — every flow run is logged with timestamps, actor identity, and decision outcome, supporting 21 CFR Part 11 requirements

### Batch Records and 21 CFR Part 11

Electronic batch records in M365 must address:

- **Electronic signatures** — Azure AD identity tied to approval actions; not just clicking a button but authenticating with credentials or MFA at the moment of signing
- **Audit trails** — immutable logs of who changed what, when, and why; SharePoint version history combined with Power Automate run history provides this
- **Access controls** — role-based permissions ensuring only authorized personnel can modify batch record templates (QA/Document Control), while production operators can only fill in designated fields
- **Data integrity (ALCOA+)** — Attributable, Legible, Contemporaneous, Original, Accurate, plus Complete, Consistent, Enduring, Available

### Integration Architecture

```
Production Floor (Power Apps mobile)
        |
        v
SharePoint Lists / Excel Online (data layer)
        |
        v
Power Automate (workflow engine)
       / \
      v   v
Outlook    Teams        Power BI
(alerts)  (approvals)  (dashboards)
```

### Document Numbering Convention

| Prefix | Category | Example |
|--------|----------|---------|
| QM- | Quality Manual | QM-001 |
| SOP- | Standard Operating Procedure | SOP-QA-001 |
| WI- | Work Instruction | WI-PROD-015 |
| FRM- | Form / Record Template | FRM-FS-003 |
| SPEC- | Specification | SPEC-RM-042 |
| POL- | Policy | POL-FS-001 |
| EXT- | External Document | EXT-REG-010 |

Department codes: QA (Quality Assurance), PROD (Production), FS (Food Safety), RD (R&D), SC (Supply Chain), REG (Regulatory), MAINT (Maintenance), SAN (Sanitation), WH (Warehouse).

### Security and Access Model

| Role | SharePoint Permission Level | Scope |
|------|---------------------------|-------|
| Document Control | Full Control | All QMS libraries |
| QA Manager | Edit + Approve | Quality System, Food Safety |
| Production Manager | Edit | Production library; Read on Quality |
| Line Operator | Read | SOPs/WIs for their department |
| External Auditor | View Only | Scoped to audit-relevant libraries, time-limited |
| R&D Scientist | Edit | R&D library; Contribute to Specifications |
| Executive | Read | All libraries; Approve on escalated items |

### Offline and Multi-Site Considerations

- **OneDrive sync** for offline access at production facilities with unreliable connectivity — sync only designated "Reference" folders, never editable controlled documents
- **SharePoint hub sites** for multi-facility deployments — central QMS hub with site-level libraries for facility-specific records
- **Teams channels** per facility for local communication with cross-facility visibility at the hub level
- **Power Apps offline mode** for batch record data entry during network outages, with automatic sync when connectivity restores

---

## References

- `references/document_control.md` — SharePoint document control architecture, library structure, metadata schema, retention policies, approval workflows
- `references/compliance_workflows.md` — Power Automate workflow designs for CAPA, NCR, complaints, SCAR, environmental monitoring, change control
- `references/batch_record_templates.md` — Excel/SharePoint batch record templates for beverage manufacturing, CCP monitoring, 21 CFR Part 11 compliance

---

## Related Skills

- `fb-food-safety-compliance` — HACCP plans, SQF/BRC audit preparation, FDA/FSMA regulatory requirements
- `fb-supply-chain-v2` — production scheduling, BOM management, inventory control
- `gws-autonomi` — Google Workspace equivalent for organizations using GWS instead of or alongside M365
- `bill-com-autonomi` — AP workflows for vendor invoices referenced in supplier management
- `qbo-autonomi` — Financial records integration for cost tracking referenced in batch records

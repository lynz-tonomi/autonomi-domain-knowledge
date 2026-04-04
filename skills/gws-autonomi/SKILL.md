# Google Workspace Integration for F&B — Autonomi

## Summary

Google Workspace integration layer for Autonomi's food and beverage operations. Covers Google Drive-based document management for regulated quality systems, Google Sheets formulation calculators and cost modeling tools, and Google Forms audit checklists with automated data collection for trend analysis. Designed to support SQF/BRC/FSSC 22000-certified operations, FDA 21 CFR 117 record-keeping, and continuous improvement programs in beverage manufacturing environments.

---

## When to Use

- **Document hierarchy and management** — organizing, naming, sharing, and controlling SOPs, work instructions, specifications, and records within Google Drive Shared Drives
- **Formulation calculations** — Brix/acid ratios, batch scaling, nutritional analysis, cost modeling, ingredient statement generation, shelf life tracking, sweetener equivalency, pH buffering, carbonation volumes
- **Audit preparation and execution** — building and deploying GMP audit checklists, SQF audit preparation checklists, incoming material inspections, environmental monitoring sampling forms, and line clearance checklists via Google Forms
- **Data collection and trend analysis** — automated Forms-to-Sheets pipelines feeding dashboards for quality metrics, complaint trends, audit scores, and compliance KPIs
- **Collaborative document review** — leveraging Google Docs real-time collaboration for multi-department SOP review cycles with commenting, suggestion mode, and version history
- **Template management** — maintaining a template gallery of standardized F&B documents (SOP, specification, CAPA, change control, batch record) in Google Docs and Sheets
- **Regulatory record retention** — configuring Drive labels, retention rules, and archival processes to meet FDA, state, and GFSI record retention requirements
- **Production floor tools** — deploying Sheets-based calculators and Forms-based checklists on tablets at production stations for real-time data capture
- **Cross-functional reporting** — aggregating quality, production, and compliance data from Sheets into Looker Studio dashboards for management review
- **External collaboration** — managing controlled sharing of specifications and audit documents with customers, co-manufacturers, and auditors while protecting proprietary formulations

---

## Key Concepts

### Google Drive as Document Management System

Google Drive Shared Drives serve as the backbone for Autonomi's quality document management. Unlike personal My Drive storage, Shared Drives provide:

- **Organizational ownership** — files belong to the organization, not individual users; no data loss when employees leave
- **Consistent permissions** — membership-based access at the drive level with granular folder and file overrides
- **Native version history** — every edit tracked with timestamp and editor identity
- **Built-in search** — full-text search across all document content, not just file names
- **Integration with Workspace apps** — seamless connection to Docs, Sheets, Forms, Slides, and third-party add-ons

### Hybrid Version Control for Regulated Documents

Google Docs maintains automatic version history, but regulated F&B environments require explicit version numbering for audit purposes:

- **Native versioning** tracks every edit for internal collaboration and draft development
- **Manual version numbering** in the document header and file name marks official approved releases (v1.0, v2.0)
- **Named versions** in Google Docs pin specific points in the version history to official release milestones
- This hybrid approach provides both the collaboration benefits of native versioning and the audit trail clarity of explicit numbered versions

### Google Forms as Data Collection Engine

Google Forms replace paper-based checklists and inspection forms across the operation:

- **Pre-operational inspections** completed on tablets at each production line before startup
- **GMP audits** conducted on mobile devices during facility walkthroughs
- **Incoming material inspections** capturing supplier lot data, temperature, and disposition decisions
- **Environmental monitoring** logging sample collection and results
- **All form responses flow to Sheets** for automated trend analysis and dashboard feeds
- **Conditional logic** in forms guides inspectors through branching paths based on findings

### Formulation Tools in Google Sheets

Sheets-based calculators serve as the operational toolkit for R&D and QC:

- **Batch scaling** — convert lab formula to production scale with unit conversions
- **Nutritional analysis** — calculate Nutrition Facts panel from ingredient database
- **Cost modeling** — ingredient costs, batch costs, per-unit costs at various production volumes
- **Label compliance** — generate ingredient statements in descending order with allergen declarations
- **Process calculations** — carbonation volumes, pH buffering, sweetener equivalency

### Security Model for F&B Operations

| Role | Shared Drive Access | Specific Restrictions |
|------|--------------------|-----------------------|
| Document Control | Manager access on all drives | Can organize, move, delete files |
| QA Director | Content Manager on Quality, Food Safety | Can edit and approve documents |
| Department Manager | Content Manager on own dept drive | Can edit within department scope |
| Supervisor | Contributor on own dept drive | Can add files, cannot delete |
| Operator | Viewer on relevant drives | Read-only access to current SOPs/WIs |
| R&D Scientist | Content Manager on R&D drive | R&D drive has restricted membership |
| External Auditor | Viewer on scoped folders | Time-limited, no download for proprietary docs |
| Co-Manufacturer | Viewer on shared specs folder | Only sees approved specifications shared with them |

### Integration Architecture

```
Production Floor (tablets/phones)
  |
  v
Google Forms (data capture)
  |
  v
Google Sheets (data storage + calculations)
  |
  v
Apps Script (automation + workflow logic)
  |         \
  v          v
Gmail        Looker Studio
(alerts)     (dashboards)
  |
  v
Google Drive Shared Drives (document storage)
  |
  v
Google Docs (SOPs, reports, procedures)
```

---

## References

- `references/document_hierarchy.md` — Google Drive structure, naming conventions, permissions, approval workflows, retention policies, template gallery
- `references/formulation_calculators.md` — Sheets-based tools for Brix/acid, batch scaling, nutrition, cost, label statements, shelf life, sweeteners, pH, carbonation
- `references/audit_checklists.md` — Google Forms for pre-op inspection, GMP audit, SQF preparation, incoming material, environmental monitoring, line clearance

---

## Related Skills

- `fb-food-safety-compliance` — HACCP plans, SQF/BRC audit preparation, FDA/FSMA regulatory requirements that drive document and checklist content
- `fb-product-formulation` — formulation science underlying the Sheets calculators
- `fb-supply-chain-v2` — production scheduling and BOM management referenced in batch records and cost calculators
- `m365-autonomi` — Microsoft 365 equivalent for organizations using M365 instead of or alongside Google Workspace
- `qbo-autonomi` — financial integration for cost data feeding formulation cost calculators

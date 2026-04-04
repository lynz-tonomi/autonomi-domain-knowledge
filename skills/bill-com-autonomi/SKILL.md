# Bill.com AP/AR Automation for Autonomi F&B

## Summary

Bill.com integration for food and beverage accounts payable and accounts receivable automation. Covers the full AP lifecycle from vendor invoice intake through payment settlement, AR invoice creation through collections, three-way PO matching for ingredient and packaging procurement, and payment optimization strategies specific to F&B cash flow patterns. Enables AI agents to route approvals, execute payments, manage deductions, and maintain audit trails.

## When to Use

- Processing vendor invoices (ingredient suppliers, co-packers, packaging vendors, freight carriers)
- Routing invoices for approval based on threshold rules and GL coding
- Scheduling and executing vendor payments (ACH, wire, virtual card, check)
- Managing three-way matching between purchase orders, receiving reports, and vendor invoices
- Handling customer invoice creation and payment tracking
- Processing and disputing trade spend deductions from retailers and distributors
- Analyzing payment timing for early pay discount optimization
- Managing 1099 vendor compliance and W-9 collection
- Reconciling Bill.com payments with QBO bank feeds
- Automating cash flow forecasting based on AP/AR aging

## Key Concepts

### AP Workflow for F&B
Food and beverage AP is high-volume and vendor-diverse. A typical F&B brand manages 30-100+ vendors across ingredient suppliers (often small farms or specialty producers), packaging manufacturers, co-packers, freight carriers, warehouse operators, brokers, and service providers. Invoice volume ranges from 50-500+ per month. Bill.com automates intake (email ingestion, OCR), GL coding (AI-suggested based on vendor history), approval routing (threshold-based with role escalation), and payment execution.

### Three-Way Matching
F&B procurement requires matching three documents: the Purchase Order (what was ordered), the Goods Received Note (what was received and passed QC), and the Vendor Invoice (what the vendor is billing). Mismatches are common due to commodity price fluctuations, quantity variances from agricultural supply variability, and quality-related rejections. Tolerance thresholds and exception workflows are configured per vendor category.

### AR and Deduction Management
F&B AR is complicated by trade spend deductions. Retailers and distributors routinely short-pay invoices, deducting promotional allowances, shortage claims, damage claims, and pricing adjustments. Deduction management — identifying, validating, coding, or disputing each deduction — is one of the most labor-intensive accounting functions in CPG. Bill.com integrates with QBO to track deductions against authorized promotions.

### Payment Settlement
F&B companies use multiple payment methods optimized by vendor type: ACH for domestic ingredient suppliers and co-packers, wire transfers for international ingredient suppliers, virtual cards for packaging vendors (earning rebates), and occasionally checks for small farm suppliers. Payment timing is strategically managed around seasonal production cycles, early pay discount opportunities, and cash flow constraints.

### Approval Hierarchies
Bill.com supports multi-tier approval workflows essential for F&B financial controls:
- Under $5,000: Auto-approve (matched to PO with no exceptions)
- $5,000-$25,000: Department manager approval
- $25,000-$50,000: CFO approval
- Over $50,000: Dual approval (CFO + CEO/COO)
- Any amount without PO: Manager + CFO approval regardless of amount

### Audit Trail and Compliance
Bill.com maintains a complete audit trail for every transaction: who submitted, who approved, when, payment method, settlement confirmation, and bank reconciliation. This supports SOX-like controls for growing F&B companies approaching audit readiness, as well as SQF/BRC supply chain traceability requirements.

## References

- `references/ap_ar_workflows.md` — Detailed AP/AR workflow documentation for F&B operations
- `references/three_way_matching.md` — Three-way PO matching rules, tolerances, and exception handling
- `references/payment_settlement.md` — Payment methods, timing optimization, and reconciliation

## Integration Points

| System | Direction | Data Flow |
|--------|-----------|-----------|
| QBO | Bidirectional | Bills sync to QBO AP; payments reconcile; chart of accounts shared |
| Warehouse (WMS) | Inbound | Receiving reports, GRN data for three-way matching |
| ERP / Procurement | Inbound | Purchase orders for matching |
| Bank | Outbound | ACH, wire, check payments; inbound bank confirmations |
| Vendor Portal | Outbound | Payment status, remittance advice |
| Retailer EDI | Inbound | Deduction files, remittance detail |

## Common Agent Tasks

1. **Ingest Vendor Invoice** — Receive invoice via email/upload, OCR extract, suggest GL coding, route for approval
2. **Three-Way Match** — Match vendor invoice against PO and receiving report, flag exceptions
3. **Approve/Reject Invoice** — Execute approval action based on authority level and matching results
4. **Schedule Payment** — Queue approved bills for payment on optimal date (considering cash flow and discounts)
5. **Execute Payment Run** — Process batch payments via ACH, wire, or virtual card
6. **Process Deduction** — Identify deduction on customer payment, match to promotion, code or dispute
7. **Manage Collections** — Identify past-due AR, generate collection communications, escalate aging items
8. **Reconcile Payments** — Match Bill.com payment confirmations to QBO bank feed transactions
9. **Vendor Onboarding** — Collect W-9, set up vendor in Bill.com and QBO, configure payment method
10. **Generate AP Forecast** — Project cash requirements based on open bills, scheduled payments, and upcoming POs

## Guardrails

- Never execute payments over $25,000 without verified CFO approval in Bill.com audit trail
- Never bypass three-way matching for ingredient or packaging vendors without documented exception
- All vendor bank account changes require verbal verification (fraud prevention)
- Payment files must be generated and transmitted on the same business day (no overnight exposure)
- Deduction disputes must be filed within 30 days of deduction date per most retailer policies
- W-9 must be on file before first payment to any new vendor (1099 compliance)
- International wire transfers require OFAC screening verification

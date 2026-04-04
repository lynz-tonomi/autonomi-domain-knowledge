# Bill.com AP/AR Workflows for F&B Operations

## Overview

Accounts Payable and Accounts Receivable workflows for a food and beverage company involve unique complexity: high vendor diversity (farms, co-packers, ingredient brokers, packaging suppliers), commodity price volatility, trade spend deductions from retailers, and seasonal cash flow patterns. This document details the end-to-end AP and AR processes in Bill.com integrated with QBO.

---

## 1. Accounts Payable Workflow

### 1.1 Vendor Invoice Intake

**Email Ingestion**
- Vendors email invoices to a dedicated AP inbox (e.g., ap@autonomi.com)
- Bill.com monitors the inbox and auto-imports attached invoices (PDF, image)
- AI/OCR extracts: vendor name, invoice number, invoice date, due date, line items, amounts, PO reference
- Extraction accuracy: 85-95% for structured invoices; lower for handwritten or non-standard formats

**Manual Upload**
- For invoices not received by email: drag-and-drop upload to Bill.com
- Used for: co-packer invoices with complex line items, international supplier invoices, credit memos

**Vendor Portal Submission**
- Large vendors can submit invoices directly through Bill.com vendor portal
- Reduces intake errors; vendor confirms GL coding and PO reference

### 1.2 GL Coding and Classification

**AI-Suggested Coding**
- Bill.com suggests GL account based on vendor history and invoice description
- Autonomi account mapping by vendor type:

| Vendor Type | Primary GL Account | Secondary Accounts |
|------------|-------------------|-------------------|
| Ingredient supplier | 5000-5060 (COGS Ingredients) | 5300 (Inbound Freight) |
| Packaging supplier | 5100-5150 (COGS Packaging) | 5310 (Inbound Freight) |
| Co-packer | 5200-5230 (COGS Co-Pack) | 5500 (QC Testing) |
| Freight carrier | 5300-5320 (COGS Freight) | 6300 (Outbound Freight) |
| Warehouse/3PL | 5400-5430 (COGS Warehouse) | — |
| Food broker | 6100 (Broker Commissions) | — |
| Marketing vendor | 6200-6240 (Marketing) | — |
| Professional services | 7200-7220 (Professional Services) | — |
| Utilities/rent | 7000-7010 (Occupancy) | — |

**Class and Location Assignment**
- Class: product line the expense relates to (if identifiable — e.g., co-pack invoice for Sparkling Water line)
- Location: channel or entity (if applicable)
- If expense spans multiple classes, split line items proportionally

**PO Reference Linking**
- Agent matches invoice PO reference to open Purchase Orders in QBO
- If PO found: pre-populate expected amounts for three-way matching
- If no PO: flag for review (may be acceptable for recurring services, unacceptable for ingredients/packaging)

### 1.3 Approval Routing

**Threshold-Based Rules**

| Invoice Amount | Approval Path | Max Approval Time |
|---------------|---------------|-------------------|
| < $1,000 | Auto-approve if PO-matched, no exceptions | Immediate |
| $1,000 - $4,999 | Auto-approve if PO-matched; manager if unmatched | 1 business day |
| $5,000 - $24,999 | Department manager required | 2 business days |
| $25,000 - $49,999 | CFO required | 3 business days |
| $50,000+ | Dual approval: CFO + CEO/COO | 5 business days |
| Any amount, no PO | Manager + CFO regardless of amount | 3 business days |
| New vendor (first invoice) | CFO required regardless of amount | 3 business days |

**Escalation Rules**
- If approver does not act within max time: auto-escalate to next level
- If primary approver is OOO: delegate to designated backup
- Urgent invoices (marked by AP team): 24-hour approval SLA with SMS notification

**Approval Actions**
- **Approve**: Invoice proceeds to payment scheduling
- **Reject**: Invoice returned to AP with rejection reason; vendor notified if appropriate
- **Request Information**: Invoice held pending additional documentation (COA, receiving report, PO amendment)
- **Reroute**: Approver redirects to different approver (wrong department, split authority)

### 1.4 Payment Scheduling

**Standard Scheduling**
- Approved invoices queued for payment based on due date and payment terms
- Default: pay on due date (maximize cash float)
- Payment runs: twice weekly (Tuesday/Thursday) for ACH; weekly (Wednesday) for checks

**Early Payment Discount Optimization**
- System flags invoices with early payment discounts
- Standard terms analysis:
  - **2/10 Net 30**: 2% discount if paid within 10 days = 36.7% annualized return
  - **1/10 Net 30**: 1% discount = 18.3% annualized return
  - **2/10 Net 60**: 2% discount for 50 days early = 14.9% annualized return
- Decision rule: take discount if annualized return > cost of capital (typically >10% for F&B)
- Agent calculates: discount value, available cash, opportunity cost, recommends take/skip

**Cash Flow Optimization**
- Agent projects weekly cash position: opening balance + expected AR receipts - scheduled AP payments
- If cash tight: prioritize payments by criticality
  1. Payroll and taxes (non-negotiable)
  2. Co-packer (production continuity)
  3. Key ingredient suppliers (supply chain risk)
  4. Freight carriers (shipment holds)
  5. Warehouse/3PL (storage continuity)
  6. All others (by due date)

### 1.5 Batch Payments

**Payment Run Process**
1. Agent generates payment batch: all approved invoices due within payment window
2. Review batch: verify total, check for duplicates, confirm bank balance sufficiency
3. Authorize batch: designated payment authorizer (CFO or controller) approves
4. Execute: Bill.com initiates ACH/wire/check for each payment
5. Confirm: Bill.com provides payment confirmation numbers
6. Reconcile: payment records sync to QBO; match to bank feed when cleared

**Duplicate Payment Prevention**
- Bill.com checks: same vendor + same invoice number + same amount = potential duplicate
- Agent additional check: same vendor + similar amount (±$10) + date within 7 days
- Duplicate flagged for manual review before payment execution

---

## 2. Vendor Management

### 2.1 Vendor Onboarding

**Required Documentation**
| Document | Purpose | Deadline |
|----------|---------|----------|
| W-9 (US vendors) | Tax ID for 1099 reporting | Before first payment |
| W-8BEN (foreign vendors) | Withholding certificate | Before first payment |
| Certificate of Insurance | Liability coverage verification | Before first PO |
| Food safety cert (SQF, BRC, etc.) | Supplier qualification | Before first ingredient PO |
| Bank account details | ACH setup | Before first payment |
| Vendor master form | Contact, payment terms, remit address | During setup |

**Bill.com Vendor Setup**
1. Create vendor profile: legal name, DBA, address, payment terms
2. Add bank account for ACH (requires micro-deposit verification or instant verification)
3. Link to QBO vendor record (sync bidirectional)
4. Assign default GL accounts based on vendor type
5. Set approval routing rules based on vendor category

### 2.2 1099 Tracking and Compliance

**1099-NEC Reporting** (Non-Employee Compensation)
- Applies to: food brokers, consultants, contract workers, demo staffing agencies
- Threshold: $600+ in calendar year
- Bill.com tracks payments by vendor and generates 1099 data export
- Agent flags vendors approaching threshold who are missing W-9

**1099-MISC Reporting** (Rents, Royalties, Other)
- Applies to: rent payments, royalty payments (license fees for branded products)
- Same $600 threshold and W-9 requirement

**Annual Process**
- November: Agent audits vendor list for missing W-9s; sends collection requests
- January 1-31: Generate 1099 forms from Bill.com payment data
- January 31: Filing deadline for 1099-NEC; February 28 (paper) / March 31 (e-file) for 1099-MISC

---

## 3. Accounts Receivable Workflow

### 3.1 Customer Invoice Creation

**Invoice Sources**
- **Retail/Distributor**: EDI 810 invoice generated from EDI 856 ASN (advance ship notice) upon shipment
- **DTC/eCommerce**: Shopify order → auto-invoice in QBO (not through Bill.com typically)
- **Foodservice**: Manual or template-based invoice in QBO, synced to Bill.com for tracking
- **Private Label**: Invoice per production batch completion and shipment

**Invoice Data**
- Customer PO reference (critical — retailers reject invoices without valid PO)
- Ship date and BOL number
- Line items with UPC, description, quantity, unit price
- Trade spend deductions pre-applied (OI discounts) or noted for post-settlement
- Payment terms (Net 30, Net 45, Net 60 depending on customer agreement)

### 3.2 Payment Tracking

**Payment Methods by Customer Type**
| Customer Type | Typical Payment Method | Typical Terms | DSO Range |
|--------------|----------------------|---------------|-----------|
| Large retailer (Kroger, Walmart) | ACH or check | Net 30-45 | 35-55 days |
| Natural/specialty retailer | Check or ACH | Net 30 | 30-45 days |
| Distributor (UNFI, KeHE) | ACH with deductions | Net 30-45 | 40-60 days |
| Foodservice distributor (Sysco, US Foods) | ACH | Net 30 | 30-40 days |
| DTC customer | Credit card (immediate) | Prepaid | 0 days |
| Amazon | ACH settlement | Net 14-30 | 14-30 days |

### 3.3 Collections Process

**Aging Buckets and Actions**

| Aging Bucket | Action | Owner |
|-------------|--------|-------|
| Current (not yet due) | Monitor; no action | System |
| 1-30 days past due | Automated payment reminder email | Agent |
| 31-60 days past due | Phone call to AP contact; escalate internally to sales | AR specialist |
| 61-90 days past due | Formal demand letter; place account on credit hold | AR manager + sales VP |
| 90+ days past due | Final notice; engage collection agency or legal | CFO |

**Credit Hold Policy**
- Account exceeding 60 days past due: new orders held pending payment
- Exception: documented dispute with active resolution path
- Credit hold release requires: payment received or written payment plan from customer

**Bad Debt Write-Off**
- Accounts deemed uncollectible after 180 days and exhausted collection efforts
- Write-off approval: CFO for amounts >$5,000
- Journal entry: Dr. Bad Debt Expense, Cr. Accounts Receivable
- Continue collection efforts post-write-off; recovery credited to income

### 3.4 Deduction Management (Critical for F&B)

**Types of Deductions**

| Deduction Type | Description | Typical % of Invoice | Valid? |
|---------------|-------------|---------------------|--------|
| Scan-back | Promo rebate per unit scanned | 5-15% during promo | Yes, if authorized |
| MCB | Manufacturer chargeback from distributor | 10-25% during promo | Yes, if authorized |
| OI | Off-invoice discount | 5-15% | Yes, if on price list |
| Slotting | New item shelf fee | Flat fee, not % | Yes, if agreed |
| Shortage claim | Retailer claims short shipment | Varies | Sometimes — verify BOL |
| Damage claim | Product arrived damaged | Varies | Sometimes — verify photos/POD |
| Quality claim | Product quality issue | Varies | Investigate — potential recall |
| Pricing dispute | Incorrect price charged | Varies | Check price agreement |
| Unauthorized deduction | No supporting documentation | Varies | Dispute immediately |

**Deduction Processing Workflow**
1. **Identify**: Payment received short of invoice amount. Bill.com/QBO flags underpayment.
2. **Research**: Agent pulls deduction backup from retailer/distributor portal (if available)
3. **Classify**: Code deduction to appropriate category
4. **Validate**: Cross-reference against authorized promotions, signed agreements, shipment records
5. **Resolve**:
   - **Valid deduction**: Create credit memo in QBO; code to trade spend GL account
   - **Invalid deduction**: File dispute with retailer/distributor within 30 days
   - **Partial validity**: Accept valid portion, dispute remainder
6. **Track**: Monitor dispute resolution; escalate if no response within 30 days
7. **Write off**: Deductions under $50-100 may be auto-written off (cost to dispute exceeds recovery)

**Deduction KPIs**
- Deduction rate: total deductions / gross revenue (target: <15%)
- Invalid deduction rate: disputed deductions / total deductions (target: <20%)
- Dispute win rate: recovered disputes / total disputes (target: >60%)
- Days to resolve: average time from deduction to resolution (target: <45 days)
- Auto-write-off rate: auto-closed deductions / total (target: <10% by value)

---

## 4. F&B-Specific Payment Patterns

### Ingredient Supplier Payments
- **Payment terms**: Net 30-45 typical; some premium/specialty suppliers require Net 15 or COD
- **Commodity suppliers** (sugar, citric acid): Net 30; prices fluctuate with commodity markets
- **Specialty/organic suppliers**: Often smaller companies with tighter cash needs; may offer 2/10 Net 30
- **Farm-direct suppliers**: May require COD or Net 15; often paid by check
- **International ingredient suppliers**: Wire transfer; may require letter of credit for first orders

### Co-Manufacturer Payments
- **Payment terms**: Net 30 standard; some require 50% deposit for first production run
- **Holdbacks**: 5-10% holdback until quality release (48-72 hour micro hold for beverages)
- **Minimum run charges**: Invoiced even if production volume falls below minimum
- **Overrun billing**: Invoiced for actual production quantity (within ±10% tolerance)
- **Rework charges**: If batch fails QC and requires rework, additional charges apply

### Broker Commission Payments
- **Calculation**: 3-7% of net sales (after returns, before trade spend)
- **Frequency**: Monthly, paid 30-45 days after month-end
- **Documentation**: Broker submits commission report; brand verifies against sales data
- **Reconciliation**: Match broker report to QBO sales by customer by product line
- **Disputes**: Common for new item launches (is commission on full case or sample cases?)

### Retailer Deduction Management
- **Cadence**: Deductions appear on payment remittance, often 2-6 weeks after invoice
- **Volume**: Large retailers may take 20-50 deductions per month across SKUs
- **Automation**: Some retailers provide deduction files via EDI 812 or portal download
- **Clearinghouse**: Consider using deduction management service (HighRadius, Vistex) at scale

---

## 5. Bill.com + QBO Sync

### Bidirectional Sync
- **Bill.com → QBO**: Approved bills sync as QBO Bills; payments sync as QBO Bill Payments
- **QBO → Bill.com**: Chart of accounts, vendor list, customer list sync from QBO as master
- Sync frequency: near real-time (within 5-15 minutes)
- Conflict resolution: QBO is system of record for chart of accounts and master data

### Sync Mapping

| Bill.com Entity | QBO Entity | Sync Direction |
|----------------|-----------|----------------|
| Bill (vendor invoice) | Bill | Bill.com → QBO |
| Bill Payment | Bill Payment | Bill.com → QBO |
| Vendor | Vendor | Bidirectional (QBO master) |
| Chart of Accounts | Account | QBO → Bill.com |
| Customer | Customer | QBO → Bill.com |
| Invoice | Invoice | QBO → Bill.com |
| Payment (AR) | Payment | Bill.com → QBO |

### Common Sync Issues
- **Duplicate vendors**: Same vendor created in both systems before sync completes. Fix: merge in QBO.
- **Account mapping mismatch**: Bill.com GL code does not map to QBO account. Fix: verify mapping table.
- **Payment date discrepancy**: Bill.com shows payment date; bank shows clearance date. Fix: use bank clearance date for reconciliation.
- **Partial payment allocation**: Bill.com payment applied to different invoices than QBO auto-match. Fix: manual reallocation in QBO.

---

## 6. Reporting and Analytics

### AP Reports
- **AP Aging Summary**: Total outstanding by vendor, by aging bucket
- **AP Aging Detail**: Individual bills by vendor with due dates and amounts
- **Payment Forecast**: Projected cash outflows for next 4 weeks based on open AP
- **Vendor Spend Analysis**: Total spend by vendor, by category, YoY comparison
- **Early Pay Discount Captured**: Discounts taken vs. discounts available
- **PO Accrual Report**: Open POs with goods received but no invoice (accrual candidates)

### AR Reports
- **AR Aging Summary**: Total outstanding by customer, by aging bucket
- **DSO Trending**: Days Sales Outstanding by month, by customer segment
- **Deduction Summary**: Total deductions by type, by customer, by resolution status
- **Cash Application Report**: Payments received, applied, unapplied, deductions
- **Collection Effectiveness Index (CEI)**: Measures AR team effectiveness at converting receivables to cash

### Cash Flow Reports
- **13-Week Cash Flow Forecast**: Rolling projection of cash in/out based on AR aging + AP scheduling
- **Net Working Capital**: Current assets - current liabilities trending
- **Cash Conversion Cycle**: DSO + DIO - DPO (Days Sales Outstanding + Days Inventory Outstanding - Days Payable Outstanding)
- **F&B benchmark**: Cash conversion cycle target 30-60 days for asset-light brand model

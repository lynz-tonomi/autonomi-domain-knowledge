# Payment Settlement for F&B Operations

## Overview

Payment settlement in food and beverage operations spans multiple methods (ACH, wire, virtual card, check), involves strategic timing decisions driven by seasonal production cycles, and requires robust reconciliation to maintain audit trails. This document covers payment mechanics, timing optimization, international payment handling, and controls for growing F&B companies.

---

## 1. Payment Methods

### 1.1 ACH (Automated Clearing House)

**Standard ACH**
- Settlement: 2-3 business days (next-day ACH available for most banks)
- Cost: $0.25-$1.00 per transaction (Bill.com pricing varies by plan)
- Limit: typically $100,000-$500,000 per transaction (bank-dependent)
- Best for: domestic ingredient suppliers, co-packers, service providers, warehouses
- Batch capable: yes — process multiple vendor payments in a single batch file

**Same-Day ACH**
- Settlement: same business day if submitted before cutoff (typically 2:00 PM ET)
- Cost: $5-$15 per transaction additional fee
- Limit: $1,000,000 per transaction (NACHA limit as of 2024)
- Best for: urgent supplier payments, avoiding production line stoppage, late-discovered early pay discounts
- Use sparingly: the fee premium is only justified for genuine urgency

**ACH Setup Requirements**
- Vendor provides: bank name, routing number (ABA), account number, account type (checking/savings)
- Verification: micro-deposit verification (2 small deposits, vendor confirms amounts) — takes 2-3 days
- Alternative: instant verification via Plaid or similar — real-time
- Security: all bank details encrypted; changes require verbal verification call to vendor (fraud prevention)

**ACH Return Codes (Common)**
| Code | Meaning | Action |
|------|---------|--------|
| R01 | Insufficient funds | Retry in 3 days or contact vendor for alternate account |
| R02 | Account closed | Contact vendor for new bank details |
| R03 | No account/unable to locate | Verify routing/account numbers with vendor |
| R04 | Invalid account number | Correct account number; reverify |
| R08 | Payment stopped by receiver | Contact vendor to understand why; may indicate dispute |
| R10 | Customer advises unauthorized | Investigate — possible fraud or vendor error |
| R16 | Account frozen | Contact vendor; may indicate legal/regulatory issue |
| R29 | Corporate customer advises not authorized | Vendor's bank rejected; verify authorization |

### 1.2 Wire Transfers

**Domestic Wire**
- Settlement: same business day (typically within 2-4 hours)
- Cost: $15-$35 per transaction (sender side) + $10-$20 (receiver side, sometimes)
- Best for: large, time-sensitive payments where ACH timeline is insufficient
- Use case in F&B: emergency ingredient purchases, equipment deposits, legal settlements

**International Wire (SWIFT)**
- Settlement: 1-5 business days depending on correspondent bank chain
- Cost: $25-$50 per transaction (sender) + intermediary fees ($15-$25 each) + receiver fees
- Currency: can send in USD (OUR instructions — sender pays all fees) or foreign currency
- Required information:
  - Beneficiary name and address
  - Beneficiary bank name, address, SWIFT/BIC code
  - Beneficiary account number or IBAN
  - Intermediary bank (if required): name, SWIFT code, ABA (for USD wires)
  - Purpose of payment (required by many countries for compliance)
  - Invoice reference number

**F&B International Wire Scenarios**
| Supplier Type | Currency | Typical Route | Notes |
|--------------|----------|---------------|-------|
| Brazilian orange juice | USD | SWIFT → Banco do Brasil | USD common; BRL settlement adds FX risk |
| European flavors/extracts | EUR | SWIFT → EU bank | SEPA transfer if available (cheaper) |
| Asian packaging (cans, lids) | USD | SWIFT → Hong Kong/China bank | Letter of credit may be required initially |
| Mexican ingredients | USD or MXN | SWIFT → Mexican bank | USD preferred to avoid FX |
| Indian spices/botanicals | USD | SWIFT → Indian bank | RBI regulations may cause delays |
| Colombian coffee | USD | SWIFT → Colombian bank | Verify OFAC compliance (narcotics screening) |

**FX Considerations**
- If paying in foreign currency: use forward contracts to lock rates for recurring purchases
- Spot rate risk: a 2% FX swing on a $50,000 payment = $1,000 unexpected cost
- Bill.com international payments: handles FX conversion; rate includes margin (compare to bank)
- Hedge strategy: for predictable recurring payments (e.g., monthly ingredient imports), lock 3-6 month forwards
- Accounting: FX gains/losses recorded in 7600 Other Income/Expense — Foreign Currency Gain/Loss

### 1.3 Virtual Card Payments

**Mechanics**
- Bill.com generates a single-use virtual credit card number for the vendor payment
- Vendor processes the card payment like a normal credit card sale
- Buyer earns cash-back rebate: typically 1.0-1.5% of transaction amount

**Rebate Economics**
```
Monthly packaging payments:          $150,000
Virtual card rebate rate:            1.25%
Monthly rebate earned:               $1,875
Annual rebate:                       $22,500
```

**Best Vendors for Virtual Card**
- Packaging suppliers (large, card-accepting corporations)
- Office supplies, software subscriptions
- Marketing and creative agencies
- Travel and entertainment vendors
- Generally NOT suitable for: ingredient suppliers (margins too thin to absorb 2-3% card fees), co-packers, small farm suppliers

**Vendor Adoption Challenges**
- Many vendors prefer ACH (lower processing cost for them: 0% vs. 2-3% card processing fee)
- Strategy: offer early payment in exchange for card acceptance (net benefit to vendor if early payment value exceeds card fee)
- Conversion rate: typically 20-30% of vendors will accept virtual card

### 1.4 Check Payments

**Still Used For**
- Small farm suppliers without ACH capability
- Government agencies (licenses, permits, fees)
- Vendors who refuse electronic payment
- Refund checks to consumers (rare)

**Process in Bill.com**
- Bill.com prints and mails check on your behalf (no physical check stock needed)
- Cost: $1.50-$2.50 per check (includes printing, envelope, postage)
- Timeline: 5-10 business days for delivery + clearance
- Positive pay: recommended for check fraud prevention (bank matches check details before clearing)

**Declining Usage**
- Target: <5% of payments by check (industry trend toward 100% electronic)
- Convert check vendors to ACH: offer faster payment timing as incentive

---

## 2. Payment Timing Strategy

### 2.1 Cash Flow Calendar for F&B

F&B companies experience seasonal cash flow patterns driven by production and sales cycles.

**Typical F&B Cash Flow Seasonality**

| Quarter | Production Activity | Sales Activity | Cash Flow Pattern |
|---------|-------------------|----------------|-------------------|
| Q1 (Jan-Mar) | Build inventory for spring/summer | Post-holiday slowdown | Cash outflow (buying ingredients, production) |
| Q2 (Apr-Jun) | Peak production | Ramping up (outdoor/summer demand) | Cash neutral to slight outflow |
| Q3 (Jul-Sep) | Moderate production | Peak sales (summer beverages) | Cash inflow (receivables collecting) |
| Q4 (Oct-Dec) | Reduced production; holiday builds | Moderate; holiday gifting spike | Cash inflow from Q3 sales; holiday outflow |

### 2.2 Payment Timing Rules

**Rule 1: Never Miss a Critical Supplier Payment**
- Co-packers, key ingredient suppliers, and freight carriers directly impact production continuity
- These vendors get priority payment even during cash-tight periods
- Maintain a "critical supplier list" with zero tolerance for late payment

**Rule 2: Capture All Economically Rational Early Pay Discounts**
Analysis framework:
```
Annualized Return = (Discount % / (100% - Discount %)) x (365 / (Full Term - Discount Term))

2/10 Net 30:  (2/98) x (365/20) = 37.2% annualized  → ALWAYS TAKE
1/10 Net 30:  (1/99) x (365/20) = 18.4% annualized  → TAKE if cash available
2/10 Net 45:  (2/98) x (365/35) = 21.3% annualized  → TAKE if cash available
1/10 Net 45:  (1/99) x (365/35) = 10.5% annualized  → TAKE if cost of capital < 10%
2/10 Net 60:  (2/98) x (365/50) = 14.9% annualized  → TAKE if cost of capital < 15%
Net 30 vs Net 45: paying 15 days early for no discount → 0% return → PAY ON DUE DATE
```

**Rule 3: Optimize DPO Without Damaging Relationships**
- Days Payable Outstanding (DPO) target: 30-40 days
- Do not systematically pay late — damages vendor relationships and can trigger credit holds
- Do not pay early without discount — wastes cash float
- Exception: strategic early payment to a critical small supplier to ensure loyalty and priority allocation

**Rule 4: Batch Payments to Reduce Administrative Cost**
- Consolidate payments to same vendor on same payment date
- Run payment batches 2x/week (not daily) to reduce processing overhead
- Exception: same-day ACH for urgent or time-sensitive payments

### 2.3 Cash Buffer Management

**Operating Cash Reserve**
- Maintain minimum 30-45 days of operating expenses in cash
- For F&B startup/growth stage: 60-90 days recommended (higher risk, less predictable revenue)
- Cash below minimum triggers: defer non-essential AP, draw on credit line, accelerate AR collection

**Line of Credit Usage**
- Revolving credit line sized at 2-3 months of COGS
- Draw when: seasonal inventory build requires cash exceeding operating reserves
- Repay when: peak-season receivables convert to cash
- Cost: Prime + 1-3% (varies by company stage and bank relationship)
- Inventory-based lending: some lenders advance against finished goods inventory (50-70% of value)

---

## 3. Early Payment Discount Analysis

### Discount Capture Report (Monthly)

| Vendor | Terms | Invoice Amount | Discount Available | Discount Taken? | Savings / Loss |
|--------|-------|---------------|-------------------|----------------|----------------|
| Pacific Juice Concentrate | 2/10 Net 30 | $42,000 | $840 | Yes | +$840 saved |
| Western Sweeteners | 1/10 Net 30 | $18,500 | $185 | Yes | +$185 saved |
| Premium Can Corp | Net 30 | $85,000 | $0 | N/A | No discount offered |
| Green Organic Farms | 2/10 Net 45 | $12,000 | $240 | No (cash tight) | -$240 missed |
| **Monthly Total** | | **$157,500** | **$1,265** | | **+$1,025 net** |

### Negotiation Strategy by Supplier Type

**Ingredient Suppliers**
- Request 2/10 Net 30 on all contracts >$10,000/month
- Offer volume commitment in exchange for discount terms
- For commodity ingredients: negotiate pricing indexed to public benchmark + fixed margin

**Packaging Suppliers**
- Large packaging companies often offer 1-2% discount for Net 10
- Combine with virtual card rebate opportunity for maximum savings
- Negotiate annual rebates tied to volume thresholds

**Co-Packers**
- Payment terms are often fixed (Net 30, no discount)
- Negotiate: quarterly volume bonus (rebate on per-unit fee if minimum volume met)
- Alternative: offer 50% advance payment for 3-5% discount (works for smaller co-packers)

**Freight Carriers**
- Typically Net 30, no discount
- Negotiate: quarterly rate review based on lane volume
- Consider prepaid freight programs with carriers for 2-5% discount

---

## 4. Bill.com Payment Processing

### Payment Authorization

**Single Authorization**
- One authorized signer approves the payment batch
- Suitable for: routine payment runs within normal parameters
- Threshold: configurable in Bill.com (e.g., batches up to $100,000)

**Dual Authorization**
- Two authorized signers must approve
- Required for: payment batches over threshold, new vendor first payment, international wires
- Bill.com supports sequential approval: first approver → second approver → payment execution

**Payment Authorizer Roles**
| Role | Payment Authority | Limits |
|------|------------------|--------|
| AP Specialist | Cannot authorize; can prepare batch | N/A |
| Controller | Authorize standard payment runs | Up to $100,000/batch |
| CFO | Authorize all payments | Unlimited with dual for >$250K |
| CEO/COO | Second approver for large payments | Dual approval partner |

### Bill.com IVA (Intelligent Virtual Assistant)

Bill.com's IVA handles routine payment tasks:
- Auto-categorize vendor invoices based on historical coding
- Suggest payment date based on terms and cash flow forecast
- Flag potential duplicate invoices before approval
- Auto-generate remittance advice on payment execution
- Track payment status and provide real-time updates

### Payment File Generation

**ACH File (NACHA Format)**
- Bill.com generates NACHA-formatted ACH file
- File transmitted to bank via secure connection
- Bank processes and initiates ACH transactions
- Confirmation returned to Bill.com; synced to QBO

**Check File**
- Bill.com prints checks via partnership with check fulfillment provider
- Positive pay file generated and transmitted to bank (fraud prevention)
- USPS First Class delivery; optional expedited delivery

**Wire Instructions**
- Bill.com submits wire instructions to partner bank
- Each wire individually processed (not batched)
- SWIFT confirmation received and stored

---

## 5. International Payments

### Cross-Border ACH
- Available for: Canada (via EFT), UK (via BACS), Eurozone (via SEPA)
- Cost: typically $5-$15 per transaction (cheaper than SWIFT wire)
- Settlement: 2-5 business days
- Currency: local currency or USD (local currency preferred to avoid double-conversion)
- Bill.com supports cross-border ACH for select countries

### Currency Conversion
- Bill.com converts USD to foreign currency at market rate + margin (typically 1-2%)
- Compare to: bank wire with FX conversion (bank rate typically market + 0.5-1.5%)
- For recurring large payments: consider FX broker (market + 0.1-0.5%) for better rates
- Lock rates with forward contracts for predictable recurring payments

### Compliance Requirements

**OFAC Screening**
- All international payments screened against OFAC Specially Designated Nationals (SDN) list
- Bill.com performs automated screening
- False positives (common names matching SDN list) require manual clearance
- Blocked transactions cannot proceed until OFAC clearance confirmed

**Anti-Money Laundering (AML)**
- Unusual payment patterns flagged: large payments to new international vendors, payments to high-risk countries
- Documentation required: commercial invoice, purchase order, proof of goods/services received
- Beneficial ownership verification for new international vendors

**Tax Withholding (Foreign Vendors)**
- W-8BEN or W-8BEN-E must be on file for foreign vendors
- Some payments subject to 30% withholding (reduced by tax treaty)
- Withholding responsibility: Autonomi must withhold and remit to IRS if applicable
- Common treaty-reduced rates: UK 0%, Germany 0%, Mexico 10%, India 15%, China 10%

---

## 6. Payment Reconciliation

### Daily Reconciliation Process

1. **Morning**: Agent pulls previous day's payment settlements from Bill.com
2. **Match to bank**: Compare Bill.com payment confirmations against bank transactions
3. **Record matched**: Matched payments marked as reconciled in both Bill.com and QBO
4. **Flag unmatched**: Payments in Bill.com but not in bank (timing difference — allow 1-3 days for ACH)
5. **Flag unknown**: Bank debits not matching any Bill.com payment (investigate — bank fee, unauthorized)

### Bank Feed Matching Rules

| Match Type | Rule | Confidence |
|-----------|------|------------|
| Exact amount + exact date | Bill.com payment = bank debit | 99% — auto-match |
| Exact amount + date ±1 day | Bill.com payment = bank debit (timing) | 95% — auto-match |
| Exact amount + date ±3 days | Likely match; confirm vendor name | 85% — suggest match |
| Amount ±$5 + same date | Possible (bank fee deducted from payment) | 70% — manual review |
| No match found | Unknown bank debit | 0% — manual investigation |

### Common Reconciliation Issues

**ACH Settlement Delay**
- Standard ACH: 2-3 business days between Bill.com payment date and bank debit date
- Agent should expect and tolerate this delay; only flag if >4 business days

**Wire Amount Discrepancy**
- International wires may arrive with intermediary bank fees deducted
- Example: wire sent for $50,000; bank debit shows $50,025 (sender fee) or $49,975 (beneficiary fee deducted)
- Difference posted to 7500 Bank Fees

**Voided/Returned Payments**
- Check voided: Bill.com reflects void; reverse payment entry in QBO
- ACH returned: return code received; payment reversed in QBO; bill returns to unpaid status
- Wire recalled: rare; requires receiving bank cooperation; can take weeks

**Duplicate Payments**
- Prevention: Bill.com duplicate detection (same vendor + same amount + date range)
- Detection: reconciliation flags two bank debits matching same vendor invoice
- Recovery: contact vendor for refund; issue via credit memo or apply to future invoices

---

## 7. Audit Trail and Controls

### SOX-Like Controls for Growing F&B Companies

Even pre-IPO, F&B companies benefit from SOX-like controls for:
- Investor confidence (VC/PE due diligence)
- Acquisition readiness
- Bank lending compliance (loan covenants)
- SQF/BRC audit requirements (financial controls section)

### Key Controls

| Control | Implementation | Evidence |
|---------|---------------|----------|
| Segregation of duties | Different people: create PO, receive goods, approve invoice, authorize payment | Bill.com user roles and audit log |
| Approval thresholds | Dollar-based approval matrix in Bill.com | Approval chain recorded per transaction |
| Three-way matching | PO/GRN/Invoice matching before approval | Match documentation stored with bill |
| Duplicate payment prevention | System check + manual review | Duplicate flag log in Bill.com |
| Vendor bank change verification | Verbal callback on any bank detail change | Change log with verification timestamp |
| Payment authorization limits | Role-based authority in Bill.com | Authorization recorded per payment |
| Reconciliation timeliness | Daily bank rec, monthly close within 10 days | Reconciliation report with dates |
| Void/credit controls | Voiding requires manager approval; logged | Void log with approver and reason |

### Audit Documentation Package

For each payment, the following audit trail should be retrievable:
1. Purchase Order (authorized, dated, approved)
2. Goods Received Note (dated, signed by receiver, QC release if applicable)
3. Vendor Invoice (original document, OCR extraction, GL coding)
4. Three-Way Match Report (match result, exceptions and resolution)
5. Approval Chain (each approver, timestamp, action)
6. Payment Authorization (authorizer, timestamp, payment method)
7. Payment Confirmation (ACH confirmation, wire SWIFT message, check image)
8. Bank Reconciliation (matched to bank statement, reconciliation date)

---

## 8. Fraud Prevention

### Common AP Fraud Schemes in F&B

| Scheme | Description | Prevention |
|--------|-------------|------------|
| **Fictitious vendor** | Employee creates fake vendor and submits invoices | Vendor onboarding requires W-9, valid address, phone verification |
| **Billing scheme** | Employee inflates vendor invoices or creates duplicate payments | Three-way matching; duplicate detection; PO requirement |
| **Check tampering** | Employee alters payee or amount on physical check | Positive pay; minimize check usage; dual authorization |
| **Bank account hijack** | Fraudster impersonates vendor, requests bank account change | Verbal verification of all bank changes; callback to known number |
| **Invoice email spoofing** | Fraudulent email with fake invoice from "known vendor" | Verify sender email domain; cross-reference PO; unusual amount flags |
| **Kickback** | Employee receives payment from vendor in exchange for inflated orders | PO approval by separate person; competitive bidding for >$10K |

### Technical Controls
- Multi-factor authentication for all Bill.com users (mandatory)
- IP allowlisting for payment authorization (optional but recommended)
- Email domain verification for vendor invoice intake
- Payment velocity alerts: flag unusual payment volume or amount spikes
- New vendor payment cooling period: 7-day hold on first payment to new vendor
- Dual authorization for: any payment >$50K, any payment to new vendor, any international wire

### Behavioral Monitoring
- Agent monitors for patterns: same approval on all invoices (collusion risk), approvals outside business hours, frequent small payments to same vendor (splitting to avoid threshold)
- Monthly: review vendor master for inactive vendors, duplicate vendor records, vendors with only a PO box address
- Quarterly: sample 10% of payments for full audit trail verification

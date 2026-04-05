# Payment Flows Reference
**Skill:** agentic-wallet | **Domain:** payment-flows | **Version:** 1.0.0

---

## 1. AP Workflow — 10-Step PO to Payment

The Autonomi AP (Accounts Payable) workflow integrates with Bill.com and QuickBooks Online to provide a fully auditable, mostly-automated purchase-to-pay cycle. Most steps are handled by agents; human approval is required only at defined thresholds.

### 1.1 The 10-Step Flow

**Step 1 — Purchase Order Generation**
- Trigger: Inventory Agent (AGNT-04) signals reorder point reached
- Actor: Procurement Agent (AGNT-05)
- Action: PO drafted with vendor, quantity, price, delivery date, smart contract conditions
- Output: PO issued in Autonomi system; mirrored to Bill.com as a draft bill; blockchain TX written

**Step 2 — Vendor PO Acknowledgment**
- Trigger: PO sent to vendor via email (LynZ `send_email` tool) or EDI
- Actor: Vendor / LynZ
- Action: Vendor confirms PO acceptance; estimated ship date provided
- Output: PO status updated to Acknowledged; AGNT-05 confirms delivery window

**Step 3 — Goods Receipt + IoT Confirmation**
- Trigger: Delivery arrives at PPB-WH-01 dock
- Actor: AGNT-22 (IoT Monitor) + receiving staff
- Action: IoT dock sensors confirm: temperature ≤ 40°F, weight verified, BOL matched
- Output: Goods Receipt posted; lot created in inventory; smart contract condition #1 and #2 satisfied

**Step 4 — COA Submission and Validation**
- Trigger: Vendor uploads COA via supplier portal (or attaches to Bill.com)
- Actor: AGNT-06 (Supplier Scorer)
- Action: Automated COA validation against spec limits
- Output: COA status = APPROVED or FAILED; smart contract condition #4 evaluated

**Step 5 — QA Release**
- Trigger: COA approved + receiving checks passed
- Actor: AGNT-09 (QC Inspector)
- Action: Lot released to usable inventory; batch eligibility confirmed
- Output: AGNT-17 smart contract: all 4 release conditions satisfied → payment queued

**Step 6 — Invoice Ingestion**
- Trigger: Vendor submits invoice (PDF, email, or Bill.com portal)
- Actor: AGNT-18 (Invoice Processor)
- Action: OCR + structured extraction; 3-way match (PO, receipt, invoice); tolerance check ±2%
- Output: Invoice validated or flagged; routed to approval queue in Bill.com

**Step 7 — Approval Routing**
- Trigger: Invoice enters Bill.com approval queue
- Actor: Automated routing by AGNT-18; human approvers by dollar tier
- Action:
  - ≤ $2,500: Auto-approved by AGNT-18
  - $2,501–$10,000: Weston 1-click in Bill.com or Agentic Wallet
  - $10,001–$25,000: Operations manager approval
  - > $25,000: CFO approval via Bill.com app

**Step 8 — Compliance Check**
- Trigger: Invoice approved
- Actor: AGNT-15 (Certification Tracker)
- Action: Verify vendor certification is current (SQF, organic, halal, etc. if required); verify no active holds or disputes
- Output: Compliance cleared or flagged

**Step 9 — Payment Execution**
- Trigger: Compliance cleared + approval received
- Actor: AGNT-17 (Settlement Agent) via Ampersend
- Action:
  - If vendor USDC-enabled: Smart contract executes; USDC transferred in 2.4 seconds
  - If vendor ACH-only: Payment scheduled in Bill.com per terms (Net-15 or Net-30)
- Output: Payment record written to blockchain; QBO entry posted automatically

**Step 10 — Reconciliation**
- Trigger: Payment settles (USDC confirmed or ACH cleared)
- Actor: AGNT-19 (Cost Tracker) + AGNT-24 (ERP Sync)
- Action: Cost allocation to BOM runs; COGS updated; journal entry posted to QBO; SAP/NetSuite updated via ERP sync
- Output: Full 3-way match closed; PO status = Closed; lot cost finalized

---

## 2. AR Workflow — Invoice to Collection

### 2.1 AR Process

**Invoice Generation:**
- AGNT-20 (AR Manager) generates customer invoices at shipment dispatch
- Invoice data: customer PO reference, lot TLC, units shipped, price per case, payment terms
- Invoice posted to QBO; Bill.com AR record created; customer notified via email

**Payment Receipt:**
- Customer pays via ACH, wire, or USDC (if enabled)
- AGNT-20 matches payment to open invoice
- QBO receipt posted; AR balance updated

**Collections and Aging:**
- AGNT-20 monitors AR aging daily
- Escalation schedule:
  - 0–30 days past due: Automated reminder email (LynZ)
  - 31–60 days: Personal follow-up from AGNT-20 via email; LynZ alert to Weston
  - > 60 days: Escalate to Weston for customer call; evaluate credit hold

### 2.2 Current AR Aging (PurePress Beverages)

| Aging Bucket | Amount | % of Total AR |
|---|---|---|
| Current (not yet due) | $284,600 | 72.1% |
| 1–30 days past due | $64,200 | 16.3% |
| 31–60 days past due | $28,400 | 7.2% |
| > 60 days past due | $17,800 | 4.5% |
| **Total AR** | **$395,000** | |

DSO (Days Sales Outstanding): 28.4 days (target: < 30 days)

---

## 3. Bill.com Integration

### 3.1 Connection Architecture

Autonomi connects to each tenant's Bill.com account via the Bill.com API (v2 REST + v3 GraphQL):
- **Authentication:** OAuth 2.0 with tenant-specific API credentials
- **Sync frequency:** Real-time webhooks for status changes; full sync every 6 hours
- **AGNT-18 capabilities:**
  - Create bills (from PO data)
  - Set approvers (SetApprovers API)
  - Approve or reject bills on behalf of Weston (with explicit policy)
  - Mark bills as paid (after USDC settlement)
  - Retrieve payment history

### 3.2 Bill.com Approval Chain (PurePress)

| Amount | Approver Role | Bill.com User |
|---|---|---|
| ≤ $2,500 | Auto-approve (AGNT-18) | — |
| $2,501–$10,000 | Primary approver | Weston Mitchell |
| $10,001–$25,000 | Operations manager | [Operations Manager] |
| > $25,000 | CFO | [CFO] |
| Any amount (food safety dispute) | Weston Mitchell | Required regardless of amount |

---

## 4. QuickBooks Online Integration

### 4.1 What Syncs Automatically

| Event | Autonomi Action | QBO Entry |
|---|---|---|
| PO issued | AGNT-05 creates PO | Purchase Order in QBO |
| Goods received | AGNT-04 GR posted | Item Receipt in QBO |
| Invoice validated | AGNT-18 approves | Bill in QBO (matched to PO) |
| USDC payment settled | AGNT-17 confirms | Bill Payment in QBO (from USDC account) |
| ACH payment cleared | Bank feed match | Bill Payment in QBO |
| Customer invoice issued | AGNT-20 generates | Invoice in QBO |
| Customer payment received | AGNT-20 matches | Payment in QBO |
| USDC off-ramp to fiat | AGNT-17 initiates | Journal Entry: USDC Wallet → Bank |

### 4.2 USDC Chart of Accounts in QBO

| Account | Type | Purpose |
|---|---|---|
| USDC Operating Wallet | Other Current Asset | Day-to-day USDC balance |
| USDC Escrow | Other Current Asset | Funds committed to pending contracts |
| USDC Dispute Hold | Other Current Asset | Escrowed dispute amounts |
| USDC Payment Expense | Expense | Transaction fees (< $0.01/tx) |

---

## 5. Micro-Transaction Revenue (Platform Layer)

Every agent decision that executes a task records a billable micro-transaction on the platform:

| Task Type | Unit Price (USDC) |
|---|---|
| Fleet route optimization | $0.55 |
| QC inspection record | $0.42 |
| Auto-reorder execution | $0.78 |
| Compliance filing | $0.65 |
| FSMA CTE record | $0.18 |
| Demand forecast update | $0.35 |
| Blockchain write (general) | $0.08 |
| Allergen check | $0.22 |

**PurePress Beverages micro-transaction spend (last month):** $28,400  
**Network total micro-transaction revenue:** $449,000 (MoM growth: +22%)

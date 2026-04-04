# QBO Integration for Autonomi F&B

## Summary

QuickBooks Online integration purpose-built for food and beverage company operations. Covers chart of accounts design for CPG/beverage manufacturing, COGS and batch costing workflows, inventory valuation for perishable goods, and API integration patterns for agent-driven automation. This skill enables AI agents to read, write, and reconcile financial data in QBO on behalf of Autonomi's finance team.

## When to Use

- Setting up or modifying chart of accounts for F&B operations (revenue by channel, COGS by cost component, inventory accounts)
- Recording production batch costs (raw materials consumption, co-pack fees, packaging, yield loss)
- Creating or modifying invoices, bills, purchase orders, or journal entries via the QBO API
- Running financial reports (P&L by product line, gross margin by SKU, COGS variance analysis)
- Syncing inventory between warehouse management systems and QBO
- Reconciling bank feeds, payment records, or trade spend deductions
- Automating month-end close procedures (accruals, inventory adjustments, cost variance entries)
- Querying QBO data for cash flow forecasting or budget-vs-actual analysis
- Managing multi-entity or multi-location financials within QBO Advanced

## Key Concepts

### Chart of Accounts Architecture
F&B companies require a deeply segmented chart of accounts that tracks revenue by channel (retail, DTC, foodservice, private label), COGS by cost component (ingredients, packaging, co-pack, freight, storage), and operating expenses by functional area. The CoA must support contribution margin analysis at the SKU level and gross margin reporting by product line. QBO class and location tracking dimensions overlay the CoA to enable multi-dimensional reporting without account proliferation.

### COGS and Batch Costing
Beverage manufacturing uses batch-based costing where each production run accumulates costs through a WIP (Work-in-Process) account. The Bill of Materials (BOM) drives standard cost rollup: ingredient costs (per-gallon or per-pound usage rates), packaging costs (bottle/can + cap + label + case + pallet), co-packing fees (per-unit toll + setup + minimums), and landed cost adders (inbound freight, duties, warehouse receiving). Standard cost is set at budget time; actual cost is captured per batch. Variance analysis (price variance, usage variance, yield loss) is critical for margin management.

### Inventory Valuation
QBO supports FIFO and weighted average costing. FIFO is strongly preferred for perishable F&B products because it aligns with FEFO (First Expired, First Out) warehouse practices and provides better COGS accuracy when ingredient costs fluctuate. Inventory accounts include Raw Materials, Work-in-Process, Finished Goods, In-Transit, and Reserve for Obsolescence. Cycle count adjustments and shrink/waste are recorded through inventory adjustment journal entries.

### API Integration Model
QBO REST API (v3) uses OAuth 2.0 authorization code grant. Agents authenticate per-realm (company), manage refresh tokens, and execute CRUD operations against core entities: Invoice, Bill, Payment, JournalEntry, Item, PurchaseOrder, Vendor, Customer. Query endpoint supports SQL-like syntax. Rate limit is 500 requests/minute/realm. Webhook subscriptions enable real-time event processing. Idempotency keys prevent duplicate transactions.

### Trade Spend Accounting
F&B trade spend (slotting fees, scan-backs, MCBs, OI, billbacks) represents 15-30% of gross revenue and requires careful contra-revenue or expense classification. Deduction management—matching retailer deductions against authorized promotions—is one of the most complex accounting workflows in CPG. QBO handles this through credit memo and journal entry patterns that net deductions against the correct promotion or customer account.

### Month-End Close
Automated close procedures include: inventory valuation adjustment (standard-to-actual), accrued co-pack fees (production complete, invoice not received), trade spend accruals (promotions running, settlement pending), freight accruals, and intercompany elimination entries for multi-entity structures.

## References

- `references/fb_chart_of_accounts.md` — Full F&B chart of accounts with account numbers, types, and reporting dimensions
- `references/cogs_batch_costing.md` — Batch costing methodology, BOM rollup, variance analysis, journal entry patterns
- `references/qbo_api_patterns.md` — API authentication, endpoints, query syntax, webhook patterns, error handling

## Integration Points

| System | Direction | Data Flow |
|--------|-----------|-----------|
| Bill.com | Bidirectional | Bills sync to QBO AP; payments reconcile back |
| Warehouse (WMS) | Inbound | Inventory levels, receiving reports, lot tracking |
| Shopify/DTC | Inbound | Sales orders, refunds, gift cards |
| Bank Feeds | Inbound | Transaction matching, reconciliation |
| Payroll (Gusto/ADP) | Inbound | Payroll journal entries, tax liabilities |
| EDI/Retailer Portals | Inbound | PO confirmations, deduction files, remittance |

## Common Agent Tasks

1. **Record Production Batch** — Create JournalEntry debiting WIP, crediting Raw Materials for ingredients consumed; then debit Finished Goods, credit WIP upon completion
2. **Create Customer Invoice** — Generate Invoice entity with line items mapped to revenue accounts by product and channel
3. **Process Vendor Bill** — Create Bill entity coded to appropriate COGS or expense accounts with PO reference
4. **Run Margin Report** — Query ProfitAndLoss report filtered by class (product line) and date range
5. **Reconcile Deductions** — Match retailer deduction against authorized promotion, create credit memo or dispute
6. **Adjust Inventory** — Record cycle count variance, expired product write-off, or damage via JournalEntry
7. **Accrue Month-End** — Create reversing JournalEntries for co-pack, freight, and trade spend accruals

## Guardrails

- Never delete or void transactions without explicit CFO approval
- All journal entries over $10,000 require dual review
- Inventory adjustments require lot-level documentation
- Trade spend entries must reference the promotion ID or agreement number
- API operations must use idempotency keys to prevent duplicates
- Refresh tokens must be stored encrypted; never log access tokens

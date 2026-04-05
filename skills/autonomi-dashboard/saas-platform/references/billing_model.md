# Billing Model Reference
**Skill:** saas-platform | **Domain:** billing | **Version:** 1.0.0

---

## 1. Revenue Architecture — Four Layers

Autonomi generates revenue from four compounding layers:

| Layer | Type | Current Revenue |
|---|---|---|
| 1. Platform subscriptions | MRR (fixed) | $785,000/month |
| 2. Agent micro-transactions | Usage (USDC) | $449,000/month |
| 3. USDC on-chain lending | Interest (TBD — launching Year 2) | — |
| 4. Data intelligence subscriptions | Subscription (TBD — launching Year 2) | — |
| **Total current** | | **$1,234,000/month** |

---

## 2. Subscription Plan Tiers

### 2.1 Starter — $7,500/month base

| Feature | Limit |
|---|---|
| AI agents | 5 |
| Supplier connections | Up to 10 |
| IoT sensors | Up to 50 |
| ERP connections | 1 |
| Participant portals | 0 |
| Blockchain records | Up to 5,000/month |
| Support | Business hours, 8-hr response |
| Onboarding | Self-service + guided |

**Overage pricing:**
- Additional agent: $250/month per agent
- Additional supplier: $50/month per supplier
- Additional IoT sensor: $5/month per sensor

### 2.2 Growth — $12,500/month base

| Feature | Limit |
|---|---|
| AI agents | 10 |
| Supplier connections | Up to 25 |
| IoT sensors | Up to 500 |
| ERP connections | 2 |
| Participant portals | Up to 5 |
| Blockchain records | Up to 50,000/month |
| USDC payments | Enabled |
| Support | Business hours, 4-hr response |
| Shared CSM | 1:8 ratio |

**Overage pricing:**
- Additional agent: $200/month per agent
- Additional supplier: $40/month per supplier
- Additional IoT sensor: $3/month per sensor
- Additional participant portal: $200/month per portal

### 2.3 Enterprise — Custom (starting ~$20,000/month base)

| Feature | Limit |
|---|---|
| AI agents | 29 (full fleet) + custom agents |
| Supplier connections | Unlimited |
| IoT sensors | Unlimited |
| ERP connections | Unlimited |
| Participant portals | Unlimited |
| Blockchain records | Unlimited |
| USDC payments | Enabled + USDC lending |
| Network Intelligence | Full access + API |
| Dedicated infrastructure | Yes |
| Dedicated CSM | 1:1 |
| Custom SLA | 99.9% uptime guarantee |
| Custom agent development | Available |

**PurePress Beverages Enterprise price:** $185,000/month (includes high micro-transaction volume, 29 agents, 342 IoT sensors, 28 suppliers, full compliance suite)

---

## 3. Micro-Transaction Pricing

Every agent decision that executes a billable task is charged as a micro-transaction to the tenant's USDC wallet.

| Task Type | Unit Price (USDC) | Example Volume/Month |
|---|---|---|
| Blockchain write (standard) | $0.08 | ~435,000 events |
| FSMA 204 CTE record | $0.18 | ~25,000 |
| QC inspection record | $0.42 | ~9,800 |
| Allergen check | $0.22 | ~4,700 |
| Demand forecast update | $0.35 | ~9,300 |
| Auto-reorder execution | $0.78 | ~240 |
| Fleet route optimization | $0.55 | ~2,800 |
| Compliance filing | $0.65 | ~880 |
| Smart contract payment execution | $0.30 | ~420 |
| Supplier score update | $0.15 | ~5,400 |
| ERP sync event (per record) | $0.05 | ~13,400 |
| IoT alert processing | $0.03 | ~90,000 |
| Risk assessment | $0.45 | ~4,300 |

### 3.1 Volume Discounts (Enterprise)

| Monthly Volume (USDC) | Discount |
|---|---|
| < $10,000 | 0% |
| $10,000–$25,000 | 5% |
| $25,001–$50,000 | 10% |
| > $50,000 | 15% |

**PurePress average micro-transaction spend:** $28,400/month (after Enterprise volume discount)

---

## 4. USDC Billing Mechanics

### 4.1 Billing Cycle
- Subscription: 1st of each month; invoiced in USD; paid via ACH or USDC
- Micro-transactions: Real-time USDC deduction from tenant wallet as events occur
- Monthly statement: Itemized micro-transaction report + subscription invoice sent by the 5th of following month

### 4.2 Wallet Balance Management
Tenants must maintain a minimum USDC balance to cover projected micro-transaction volume:
- Minimum balance: 14-day projected micro-transaction spend
- Low balance warning: At 7-day projected spend
- Auto-top-up (opt-in): Replenishes from registered fiat bank account via ACH when balance drops below 7-day threshold

### 4.3 USDC to USD Conversion for Billing
Micro-transactions are priced in USD. USDC is pegged 1:1, so 1 USDC = $1.00 always (no conversion risk for tenants).

---

## 5. Current Billing Dashboard (SaaS Billing Page)

### 5.1 Revenue Summary (April 2026)

| Metric | Value |
|---|---|
| MRR (subscriptions) | $785,000 |
| MRR (micro-transactions) | $449,000 |
| Total MRR | $1,234,000 |
| ARR | $14.8M (annualized including usage) |
| MoM growth | +22% |
| Net Revenue Retention | 118% (upsell from usage growth) |
| Churn | 0 tenants in last 12 months |

### 5.2 Revenue by Tenant

| Tenant | Base Subscription | Micro-Transactions | Total MRR |
|---|---|---|---|
| PurePress Beverages | $20,000 | $165,000 | $185,000 |
| Cascade Drinks | $12,500 | $235,500 | $248,000 |
| VitaFlow | $12,500 | $179,500 | $192,000 |
| SunRise RTD | $7,500 | $152,500 | $160,000 |
| **Total** | **$52,500** | **$732,500** | **$785,000** |

Note: The micro-transaction figures above are the billed amounts. Total platform micro-transaction revenue including Autonomi's platform margin is reported separately.

---

## 6. Future Revenue Layers

### 6.1 On-Chain Lending (Year 2 Launch)

The USDC transaction data creates a unique underwriting dataset. Autonomi can offer:
- **Supplier credit lines:** Extended to suppliers with ≥ 90 supplier score and 12+ months of on-time payment history. Line = 90 days of average invoice volume. Interest rate: Prime + 2%.
- **Manufacturer working capital:** Short-term PO financing for production scale-ups. Terms: 30–60 days. Interest rate: Prime + 3%.
- **Revenue projection:** At 20 tenants with $50M/month USDC volume, lending portfolio could reach $15–20M with $1.8–2.4M annual interest income.

### 6.2 Data Intelligence Subscription (Year 2 Launch)

Standalone subscription for companies not running full Autonomi operations:
- **Commodity intelligence:** F&B ingredient demand and pricing index. $2,500/month.
- **Supplier benchmarking:** Network-wide supplier performance data. $5,000/month.
- **Regulatory intelligence:** Recall prediction, FDA alert monitoring, trend analysis. $3,500/month.
- **Full intelligence suite:** $8,500/month.

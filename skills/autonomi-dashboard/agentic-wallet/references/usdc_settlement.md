# USDC Settlement Reference
**Skill:** agentic-wallet | **Domain:** settlement | **Version:** 1.0.0

---

## 1. What is USDC?

USDC (USD Coin) is a fully regulated stablecoin issued by Circle Financial, pegged 1:1 to the US dollar. Every USDC token is backed by cash and short-term US Treasuries held in segregated reserve accounts, audited monthly by Grant Thornton. USDC is not speculative cryptocurrency — it is a digital representation of a US dollar with the ability to move on blockchain rails.

**Why Autonomi uses USDC:**
- Agents can hold and move USDC programmatically without a bank account or ACH batch window
- Settlement in 2.4 seconds vs. 1–3 business days for ACH
- Smart contracts can verify conditions and release payment atomically
- Every transaction is permanently on-chain — no reconciliation disputes
- Easy off-ramp back to fiat at any time

---

## 2. Ampersend — The Economic Control Plane

Ampersend (by Edge & Node) sits between every agent and every USDC payment. Built on Coinbase's x402 protocol and Coinbase AgentKit, it enforces policy-based controls before any transaction executes.

### 2.1 How It Works

When the Settlement Agent (AGNT-17) initiates a payment:

1. AGNT-17 sends payment intent to Ampersend policy engine
2. Policy engine evaluates:
   - Is the destination address on the approved supplier allowlist?
   - Is the payment within the agent's daily budget?
   - Is the payment below the per-transaction auto-approve threshold?
   - Has the smart contract trigger condition been satisfied?
3. If all checks pass: USDC executes via Coinbase AgentKit on Base L2
4. If any check fails: Payment escalated to human; reason logged to blockchain
5. Settlement confirmed in 2.4 seconds; on-chain transaction ID returned

### 2.2 Agent Cards

Each of the 29 agents has its own virtual "Agent Card" in the Agentic Wallet UI. An Agent Card shows:
- Agent name and ID
- Spend today / spend this month
- Daily budget remaining
- Per-transaction limit
- Last 5 transactions
- Current escrow holds

---

## 3. Budget Control Configuration — Per Tenant

| Tenant | Daily Spend Limit | Per-Transaction Auto-Approve | Weekend Policy | Monthly Aggregate |
|---|---|---|---|---|
| PurePress Beverages (Enterprise) | $150,000 | $10,000 | Full access | No cap |
| Cascade Drinks (Growth) | $75,000 | $5,000 | Reduced to 50% | $1.2M |
| VitaFlow (Growth) | $60,000 | $5,000 | Full access | $900K |
| SunRise RTD (Starter) | $25,000 | $2,500 | Weekdays only | $350K |

**Platform aggregate (all tenants, last 30 days):** $84.2M USDC

---

## 4. Smart Contract Architecture

### 4.1 Standard Delivery Payment Contract

```
Contract Type: DELIVERY_PAYMENT
Parties: PurePress Beverages → CitroSource Inc (VND-001)
PO Reference: PO-PPB-20260404-012
Amount: 8,420.00 USDC
Escrow: Pre-funded at PO issuance

Release Conditions (ALL must be true):
  1. delivery_scan_confirmed == TRUE
     (IoT dock reader confirms BOL number matches)
  2. temperature_at_receipt <= 40°F
     (IoT temperature logger on incoming dock, sensor IOT-DOCK-01)
  3. quantity_received >= (po_quantity × 0.98)
     (receiving scale weight ≥ 23,520 lbs of 24,000 ordered)
  4. coa_status == "APPROVED"
     (AGNT-06 COA validation passed)

If all conditions met: → EXECUTE PAYMENT (2.4 seconds to finality)
If any condition fails: → ESCROW_HOLD (human review required)
```

### 4.2 Contract States

| State | Meaning |
|---|---|
| `PENDING` | Contract created; awaiting delivery |
| `MONITORING` | Delivery in transit; IoT tracking active |
| `CONFIRMED` | All conditions met; payment queued |
| `SETTLED` | USDC transferred; TX hash recorded |
| `ESCROW_HOLD` | Condition(s) failed; human review required |
| `DISPUTED` | Formal dispute raised; funds locked |
| `CANCELLED` | PO cancelled; funds returned to wallet |

### 4.3 x402 Protocol — Pay-Per-Query API

The x402 protocol enables any Autonomi data endpoint to be monetized directly. External AI agents query commodity intelligence:

1. External agent sends HTTP request to Autonomi Network Intelligence API
2. Autonomi responds with HTTP 402 (Payment Required) + Ampersend payment address
3. External agent's wallet sends 0.04 USDC to Ampersend address
4. Ampersend verifies payment cryptographically (< 200ms)
5. Autonomi serves the data
6. No API key, no subscription management, no invoicing — just cryptographic proof of payment

---

## 5. Wallet Balance and Liquidity

### 5.1 PurePress Beverages Wallet

| Account | Balance (USDC) | Purpose |
|---|---|---|
| Operating account | 284,200 | Day-to-day PO payments |
| Escrow account | 47,800 | Active contracts in flight |
| Dispute hold | 12,600 | NutSource allergen dispute |
| Reserve | 150,000 | 30-day emergency buffer |
| **Total** | **494,600** | |

### 5.2 Liquidity Management

AGNT-17 monitors wallet balance against projected 30-day spend. Alert thresholds:

| Condition | Action |
|---|---|
| Balance < 14-day projected spend | Alert to Weston via LynZ |
| Balance < 7-day projected spend | Critical alert; initiate USDC top-up from bank |
| Balance < 3-day projected spend | Auto-pause non-critical POs; emergency escalation |

Top-up process: ACH wire → Circle USDC minting → wallet credited (T+1 banking day)

---

## 6. Settlement Speed Comparison

| Payment Method | Settlement Time | Cost per Transaction | On-Chain Audit |
|---|---|---|---|
| ACH (standard) | 1–3 business days | $0.10–0.30 | No |
| Wire transfer | Same day (if cut-off met) | $15–35 | No |
| USDC on Base L2 | 2.4 seconds | < $0.01 | Yes, permanent |
| USDC on Ethereum L1 | 12 seconds | $1–10 (gas) | Yes, permanent |
| Credit card | T+2 days to settle | 1.5–3.5% interchange | No |

---

## 7. Off-Ramp to Fiat

The Agentic Wallet View 2 page shows the off-ramp interface. USDC can be converted back to USD at any time:

1. Initiate off-ramp: amount + destination bank account
2. Ampersend/Coinbase bridge processes conversion
3. USDC burned; USD initiated via ACH
4. ACH settles T+1 banking day
5. Transaction recorded on-chain (burn event) + QBO entry posted

**Off-ramp fee:** 0.15% of conversion amount (Coinbase off-ramp fee)  
**Minimum:** $1,000 per conversion  
**Maximum per day:** $500,000 (KYB-verified enterprise accounts)

# Blockchain Architecture Reference
**Skill:** blockchain-traceability | **Domain:** architecture | **Version:** 1.0.0

---

## 1. Overview

Autonomi's blockchain layer uses a Hyperledger Fabric-based distributed ledger simulation. It is not a public chain — it is a permissioned ledger purpose-built for food manufacturing audit requirements. Every platform event is recorded as a transaction. Blocks are finalized every 30 seconds or when 50 transactions are queued, whichever comes first. All data is cryptographically signed, and the ledger is append-only — no record can be altered or deleted.

---

## 2. Ledger Architecture

### 2.1 Node Topology

| Node Type | Count | Role |
|---|---|---|
| Ordering nodes | 3 | Deterministic ordering via Raft consensus |
| Peer nodes (Autonomi) | 4 | Ledger maintenance + endorsement |
| Peer nodes (per Enterprise tenant) | 2 | Tenant-owned copy of their channel |
| CA nodes | 2 | Certificate authority for identity |

### 2.2 Channels

Each tenant operates on a private channel. Only the tenant and Autonomi platform nodes can read transactions on that channel. Cross-tenant intelligence (Network Intelligence Agent) operates on a separate aggregated analytics channel where individual transaction details are anonymized before aggregation.

| Channel | Participants | Data |
|---|---|---|
| `purepress-main` | PurePress + Autonomi nodes | All PPB production, quality, procurement, payment events |
| `cascade-main` | Cascade Drinks + Autonomi nodes | All Cascade events |
| `network-intelligence` | Autonomi analytics nodes only | Anonymized aggregate metrics |

---

## 3. Block Structure

```json
{
  "block_number": 48291,
  "timestamp": "2026-04-04T14:23:11.847Z",
  "previous_hash": "a4f7c3d9e2b81f6a...",
  "merkle_root": "9c2e8b4f1a7d3c6e...",
  "transactions": [
    {
      "tx_id": "0x4a7f3c8d1e9b2f5a...",
      "tx_type": "BATCH_RELEASE",
      "timestamp": "2026-04-04T14:23:09.201Z",
      "agent_id": "AGNT-09",
      "agent_signature": "MFYwEAYHKoZIzj0CAQY...",
      "payload": {
        "batch_id": "PPB-L01-20260404-003",
        "decision": "RELEASED",
        "confidence": 0.96,
        "qc_checks_passed": 14,
        "qc_checks_total": 14,
        "release_timestamp": "2026-04-04T14:23:08.000Z"
      }
    }
  ],
  "block_hash": "7f3c9a2e4b8d1f5c...",
  "validator_signatures": [
    "node-peer-01: MFYwEAYH...",
    "node-peer-02: MFYwEAYH...",
    "node-peer-03: MFYwEAYH..."
  ]
}
```

---

## 4. Transaction Types

| TX Type | Triggering Event | Agent | Volume/Day |
|---|---|---|---|
| `BATCH_CREATED` | Production scheduler confirms batch | AGNT-03 | ~18 |
| `BATCH_STARTED` | First unit fills on line | AGNT-03 | ~18 |
| `BATCH_RELEASED` | QA sign-off | AGNT-09 | ~16 |
| `BATCH_HELD` | QA hold placed | AGNT-09 | ~2 |
| `INGREDIENT_RECEIVED` | Receiving dock confirmation | AGNT-04 | ~24 |
| `INGREDIENT_CONSUMED` | Lot picked and consumed | AGNT-04 | ~120 |
| `PO_ISSUED` | Purchase order generated | AGNT-05 | ~8 |
| `PAYMENT_INITIATED` | USDC smart contract triggered | AGNT-17 | ~14 |
| `PAYMENT_SETTLED` | Base L2 confirmation received | AGNT-17 | ~14 |
| `PAYMENT_HELD` | Payment escrow placed | AGNT-17 | ~1 |
| `QC_CHECK` | Individual quality test recorded | AGNT-09 | ~280 |
| `ALLERGEN_EVENT` | Allergen alert or clearance | AGNT-10 | ~4 |
| `TEMP_EXCURSION` | IoT temp deviation recorded | AGNT-22 | ~3 |
| `CAPA_OPENED` | CAPA action initiated | AGNT-11 | ~2 |
| `FSMA_CTE` | FSMA 204 critical tracking event | AGNT-13 | ~842 |
| `RECALL_EVENT` | Recall action taken | AGNT-14 | rare |
| `AGENT_DECISION` | Any agent auto-executed decision | Multiple | ~7,250 |

---

## 5. Smart Contract Execution

Payment smart contracts are the most operationally critical contracts on the platform. A standard payment contract:

```
Contract ID: SC-PPB-VND001-20260404-012
Trigger Conditions:
  AND(
    delivery_confirmed == TRUE,           // Receiving dock scan
    temperature_at_receipt <= 40°F,       // IoT dock sensor
    quantity_received >= po_quantity * 0.98, // Fill rate ≥ 98%
    coa_status == "APPROVED"              // QC agent validation
  )
Payment: 8,420.00 USDC
Destination: CitroSource wallet (0x7f3c9a2e...)
Settlement: Coinbase AgentKit → Base L2
Finality: 2.4 seconds (Base L2 finality time)
```

If any condition fails, the contract moves to `ESCROW_HELD` state. AGNT-17 logs the failure reason and escalates to human review.

---

## 6. Blockchain Explorer — Dashboard Page

The Blockchain Explorer page (`blockchain`) shows:
- Live block creation feed — new blocks appear as they are finalized
- Transaction hash, type, agent, and timestamp for each TX
- Block detail drill-down: full payload, signatures, Merkle proof
- Search by: batch ID, lot number, PO number, transaction type, date range
- Verification panel: paste any TX hash to verify it against the live ledger

---

## 7. FDA Audit Use Case

When an FDA inspector asks "How do you know this decision was made correctly and the agent only accessed what it was supposed to access?":

1. Inspector provides the batch ID or incident timestamp
2. AGNT-23 retrieves the complete decision chain for that event
3. Blockchain Explorer shows every agent action, in sequence, with cryptographic proof
4. OttoClaw sandbox logs confirm exactly which data paths were accessed
5. Agent signature on every transaction proves which agent made each decision
6. Complete chain of custody from ingredient receipt to finished good dispatch — provably unbroken

This closes the most challenging audit question in AI-assisted food manufacturing.

---

## 8. Data Retention

| Data Category | On-Chain Retention | Off-Chain Archive |
|---|---|---|
| FSMA 204 records | Permanent (regulatory requirement) | Mirror in secure cloud archive |
| Batch records | 2 years on-chain + permanent archive | Yes |
| Payment records | 7 years (financial audit) | Yes |
| QC check data | 2 years | Yes |
| Agent decision logs | 1 year on-chain | Archive to cold storage |
| IoT sensor readings | 90 days on-chain | Archive to cold storage |

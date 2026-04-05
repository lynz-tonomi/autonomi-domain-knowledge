# Agent Configuration Reference
**Skill:** ai-agent-orchestration | **Domain:** agent-config | **Version:** 1.0.0

---

## 1. OttoClaw Sandbox Architecture

Each of the 29 agents runs inside a dedicated OttoClaw OpenShell sandbox with kernel-level enforcement. The security model uses three Linux security primitives:

### 1.1 Landlock (Filesystem Access Control)
Each agent blueprint declares exactly which filesystem paths it may read or write. Example — Procurement Agent (AGNT-05) blueprint:
```
allow_read:  /data/ingredients/, /data/vendors/, /data/pricing/
allow_write: /data/purchase_orders/, /data/po_queue/
deny_all:    /data/formulations/, /data/quality_records/, /data/blockchain_keys/
```
If prompt injection attempts to read formulation data, the kernel blocks the syscall — it is physically impossible regardless of model behavior.

### 1.2 seccomp (System Call Filtering)
Each sandbox applies a strict seccomp profile allowing only required syscalls:
- **All agents:** read, write, open, close, stat, fstat, mmap, exit_group
- **Agents with network access:** socket, connect, send, recv (allowlisted endpoints only)
- **Agents without network access:** socket syscall blocked entirely
- **Blocked for all agents:** ptrace, fork (no agent can spawn child processes), raw disk access

### 1.3 Network Namespaces
Each agent has an isolated network namespace. Egress is restricted by allowlist:
- Outbound HTTPS connections only to endpoints declared in the blueprint
- AGNT-05 (Procurement): approved supplier domains + Ampersend payment endpoint
- AGNT-22 (IoT Monitor): MQTT broker on internal network only
- AGNT-23 (Blockchain Ledger): Hyperledger Fabric peer nodes only
- No agent can initiate connections to external addresses not in its allowlist

---

## 2. Inference Routing

### 2.1 On-Premises Deployment
Agents use localized Nemotron inference models running on-site. Formulation data, COA documents, and batch records never leave the facility. This is the standard configuration for Enterprise tenants.

### 2.2 SaaS / Cloud Deployment
SaaS tenants route to NVIDIA cloud inference or Anthropic Claude via secure API. Data is encrypted in transit (TLS 1.3) and at rest. No training on tenant data.

### 2.3 Model Selection by Agent

| Agent Domain | Model Tier | Rationale |
|---|---|---|
| Operations (scheduling, inventory, procurement) | Nemotron-mini / fast tier | High decision frequency; speed > depth |
| Quality & Food Safety | Nemotron-standard | Regulatory precision required |
| Compliance & Regulatory | Claude Sonnet / advanced tier | Complex document analysis, regulatory citations |
| Finance & Payments | Nemotron-standard | Arithmetic precision; low hallucination risk |
| IoT & Infrastructure | Rules engine + Nemotron-mini | Mostly threshold-based; LLM for edge cases |
| Intelligence & Analytics | Claude Sonnet / advanced tier | Deep cross-dataset reasoning |

---

## 3. Confidence Thresholds

Each agent operates with configurable confidence thresholds that determine whether a decision is auto-executed or escalated for human review.

### 3.1 Global Defaults

| Confidence Level | Action |
|---|---|
| ≥ 0.92 | Auto-execute (no human review) |
| 0.75–0.91 | Auto-execute + log for async review |
| 0.60–0.74 | Queue for human review within 4 hrs |
| < 0.60 | Block; immediate human escalation |

### 3.2 Per-Agent Overrides

| Agent | Min Auto-Execute Confidence | Notes |
|---|---|---|
| AGNT-13 (FSMA 204 Recorder) | 0.99 | Regulatory records require near-certainty |
| AGNT-14 (Recall Coordinator) | — | Recall decisions always require human sign-off |
| AGNT-16 (Regulatory Filing) | 0.95 | FDA filings — high accuracy requirement |
| AGNT-17 (Settlement Agent) | 0.88 | Payment execution; slightly lower due to policy controls |
| AGNT-27 (Risk Assessment) | 0.70 | Risk signals prefer to escalate earlier |
| AGNT-28 (Formulation Advisor) | 0.75 | Suggestions only; human judgment required |

---

## 4. Auto-Approve Dollar Thresholds

Financial decisions have a separate approval layer independent of confidence scores.

| Decision Type | Auto-Approve Limit | Escalation Path |
|---|---|---|
| PO issuance (AGNT-05) | ≤ $2,500 USDC | > $2,500 → Weston 1-click; > $25K → CFO |
| Emergency PO override | ≤ $15,000 USDC | Always notify LynZ; human confirm > $15K |
| USDC settlement (AGNT-17) | ≤ $10,000 per transaction | > $10K → Weston approval |
| Freight tender (AGNT-07) | ≤ $5,000 | > $5K → operations manager |
| Sample request (LynZ) | Any value | Always confirm with Weston before submitting |

---

## 5. Escalation Rules

### 5.1 Escalation Queue
All escalated decisions appear in the Mission Control view under "Pending Human Actions." Each item shows:
- Agent ID and decision description
- Confidence score
- Recommended action (with reasoning)
- Time in queue
- Approve / Override / Reject buttons

### 5.2 Escalation SLAs

| Priority | SLA | Escalation Path if Missed |
|---|---|---|
| Critical (recall, food safety) | 15 min | LynZ voice notification + SMS |
| High (payment > $10K, quality hold) | 1 hr | LynZ voice notification |
| Medium (PO > $2,500, schedule change) | 4 hrs | Dashboard notification |
| Low (recommendations, log review) | 24 hrs | Dashboard badge |

### 5.3 Auto-Escalation Triggers

Agents self-escalate (regardless of confidence) when:
- Any food safety critical limit is approached (CCP deviation) — AGNT-09
- Allergen cross-contact risk detected — AGNT-10
- Recall investigation initiated — AGNT-14
- Supplier score drops below 60 — AGNT-06
- Single-source supply risk for critical ingredient — AGNT-27
- USDC wallet balance below 24-hr projected spend — AGNT-17

---

## 6. Agent Activity Logs

Every agent writes structured activity logs to both the Autonomi platform database and the blockchain ledger:

```json
{
  "agent_id": "AGNT-05",
  "timestamp": "2026-04-04T14:23:11Z",
  "decision_type": "PO_GENERATION",
  "confidence": 0.94,
  "auto_executed": true,
  "decision": {
    "vendor_id": "VND-001",
    "po_number": "PO-PPB-20260404-012",
    "amount_usd": 8420.00,
    "ingredient": "FCOJ concentrate",
    "quantity_lbs": 24000
  },
  "reasoning_summary": "Inventory at 89% of ROP; lead time 5 days; VND-001 score 96.4; within auto-approve limit",
  "blockchain_tx_id": "0x4a7f3c8d..."
}
```

---

## 7. Per-Tenant Configuration

Each tenant can configure agent behavior within platform policy limits:

| Parameter | Configurable by Tenant | Platform Limits |
|---|---|---|
| Auto-approve thresholds | Yes | Cannot exceed platform maximums |
| Confidence cutoffs | Yes (±0.10 from default) | Min 0.60 absolute floor |
| Escalation SLA targets | Yes | Cannot exceed 15 min for Critical |
| Agent assignment (which agents active) | Yes, within plan limits | Starter: 5 agents; Growth: 10; Enterprise: 29 |
| Model tier selection | Enterprise only | — |
| OttoClaw blueprint customization | Enterprise only | Security team review required |

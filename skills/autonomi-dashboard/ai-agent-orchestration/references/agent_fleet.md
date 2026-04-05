# Agent Fleet Reference
**Skill:** ai-agent-orchestration | **Domain:** agent-fleet | **Version:** 1.0.0

---

## 1. Overview

The Autonomi platform deploys 29 specialized AI agents. Each agent runs inside a dedicated OttoClaw sandbox with kernel-level security. Agents are organized across six functional domains. Every agent decision is recorded to the immutable blockchain ledger. Collectively the fleet makes approximately 250 decisions per agent per day, totaling ~7,250 decisions daily per tenant.

---

## 2. Agent Fleet — Complete Directory

### Domain: Operations

| Agent ID | Agent Name | Role | Decisions/Day | Auto-Approve Rate |
|---|---|---|---|---|
| AGNT-01 | Demand Planning Agent | Forecast demand signals, update S&OP plan, signal production triggers | 312 | 94% |
| AGNT-02 | Capacity Planning Agent | Evaluate line utilization, flag bottlenecks, recommend overtime or downshift | 148 | 88% |
| AGNT-03 | Production Scheduler | Sequence batches, allergen changeovers, assign lines, re-optimize every 15 min | 487 | 91% |
| AGNT-04 | Inventory Agent | Manage FEFO rotation, safety stock, lot tracking, hold/release | 594 | 96% |
| AGNT-05 | Procurement Agent | Generate POs, route to approved vendors, manage delivery tracking | 263 | 78% |
| AGNT-06 | Supplier Scorer | Calculate and update vendor composite scores after every delivery event | 180 | 100% |
| AGNT-07 | Logistics Agent | Carrier selection, route optimization, OTIF monitoring, cold chain alerts | 241 | 85% |
| AGNT-08 | Fleet Route Optimizer | Optimize delivery routes for outbound multi-stop loads | 94 | 90% |

### Domain: Quality & Food Safety

| Agent ID | Agent Name | Role | Decisions/Day | Auto-Approve Rate |
|---|---|---|---|---|
| AGNT-09 | QA / QC Inspector Agent | Review in-process check data, release or hold batches | 328 | 82% |
| AGNT-10 | Allergen Control Agent | Validate allergen sequencing, screen COAs for allergen declarations | 156 | 99% |
| AGNT-11 | CAPA Manager | Open, track, and close Corrective and Preventive Actions | 74 | 76% |
| AGNT-12 | Environmental Monitor | Correlate EMP swab results, flag Listeria indicator trends | 118 | 88% |

### Domain: Compliance & Regulatory

| Agent ID | Agent Name | Role | Decisions/Day | Auto-Approve Rate |
|---|---|---|---|---|
| AGNT-13 | FSMA 204 Recorder | Write CTEs and KDEs to blockchain for full traceability chain | 842 | 100% |
| AGNT-14 | Recall Coordinator | Manage recall decision trees, distribution trace, regulatory notifications | 38 | 22% |
| AGNT-15 | Certification Tracker | Monitor cert expiry dates, schedule audits, manage document library | 62 | 91% |
| AGNT-16 | Regulatory Filing Agent | Prepare and track FDA filings, FSMA registrations, process authority records | 29 | 55% |

### Domain: Finance & Payments

| Agent ID | Agent Name | Role | Decisions/Day | Auto-Approve Rate |
|---|---|---|---|---|
| AGNT-17 | Settlement Agent | Execute USDC smart contract payments on delivery confirmation | 184 | 89% |
| AGNT-18 | Invoice Processor | Ingest, validate, and route supplier invoices through AP workflow | 146 | 73% |
| AGNT-19 | Cost Tracker | Calculate real-time COGS, yield variance costs, freight allocations | 312 | 97% |
| AGNT-20 | AR Manager | Generate customer invoices, track collections, flag aging items | 88 | 84% |
| AGNT-21 | Budget Monitor | Compare actuals vs. budget, flag variances > thresholds | 124 | 93% |

### Domain: IoT & Infrastructure

| Agent ID | Agent Name | Role | Decisions/Day | Auto-Approve Rate |
|---|---|---|---|---|
| AGNT-22 | IoT Monitor Agent | Process sensor readings, fire environmental alerts, manage sensor health | 6,840 | 99.8% |
| AGNT-23 | Blockchain Ledger Agent | Write all platform events to Hyperledger Fabric ledger | 14,200 | 100% |
| AGNT-24 | ERP Sync Agent | Bidirectional sync with SAP / NetSuite / QBO | 448 | 95% |
| AGNT-25 | Data Pipeline Agent | Clean, transform, and route data between systems | 2,140 | 98% |

### Domain: Intelligence & Analytics

| Agent ID | Agent Name | Role | Decisions/Day | Auto-Approve Rate |
|---|---|---|---|---|
| AGNT-26 | Demand Intelligence Agent | Cross-network demand pattern analysis, commodity index, trend detection | 187 | 94% |
| AGNT-27 | Risk Assessment Agent | Evaluate supply chain risk, concentration exposure, single-source dependency | 144 | 68% |
| AGNT-28 | Formulation Advisor | BOM optimization suggestions, ingredient substitution analysis | 56 | 65% |
| AGNT-29 | Network Intelligence Agent | Cross-tenant benchmarking, supplier network scoring, anomaly detection | 203 | 91% |

---

## 3. Agent Status Indicators

| Status | Color | Meaning |
|---|---|---|
| Active | Green | Running normally, within thresholds |
| Busy | Amber | Processing high volume; response slightly delayed |
| Escalated | Red | One or more decisions held for human review |
| Idle | Gray | No pending decisions; standby mode |
| Offline | Dark gray | Sandbox unavailable; auto-restart triggered |

---

## 4. Agent Views on the Dashboard

### Grid View
Shows all 29 agents as cards. Each card displays:
- Agent ID and name
- Current status indicator
- Decisions made today (running count)
- Last action timestamp
- Auto-approve rate (7-day rolling)

### Neural Map (Cerebro)
Visual network diagram showing agent-to-agent communication in real time. Active message passing appears as animated connection pulses. Color coding indicates domain. Use `show_agent_view('map')` to navigate here.

### Mission Control
Operational command center view. Shows:
- Live decision feed (scrolling ticker)
- Active escalations requiring human input
- Cascade demo trigger
- Per-domain KPI gauges
Use `show_agent_view('mission')` to navigate here.

---

## 5. Inter-Agent Communication Patterns

Agents communicate via a structured event bus. Common patterns:

**Procurement → Production:**
AGNT-05 fires `INGREDIENT_CONFIRMED` event when PO is accepted → AGNT-03 unlocks batch from pending to scheduled.

**IoT → QA → Blockchain:**
AGNT-22 fires `TEMPERATURE_EXCURSION` → AGNT-09 places affected lot on Hold → AGNT-23 writes Hold event to ledger.

**QC + Supplier Scorer → Settlement:**
AGNT-09 COA fail → AGNT-06 flags vendor → AGNT-17 escrows payment pending resolution.

**Demand → Production → Procurement:**
AGNT-01 fires `DEMAND_SPIKE` (>20%) → AGNT-03 adds Tier 1 batch → AGNT-05 verifies ingredient coverage or issues emergency PO.

**Risk → Procurement → LynZ:**
AGNT-27 detects single-source concentration risk → AGNT-05 flags for backup supplier activation → LynZ voice notification to Weston.

---

## 6. The Cascade Demo — Supplier Quality Failure Scenario

This is the centerpiece demo triggered at CUE 6 of the investor tour.

**Scenario:** QC agent detects peanut allergen cross-contamination in incoming tropical concentrate lot from NutSource.

**Timeline:**
- T+0.0s: AGNT-09 (QC Inspector) flags allergen test failure — peanut protein 48 ppm (spec: < 5 ppm)
- T+3.2s: AGNT-10 (Allergen Control) raises CRITICAL alert, blocks lot from production
- T+6.8s: AGNT-27 (Risk Assessment) flags concentration risk — NutSource is sole supplier for this blend
- T+11.4s: AGNT-05 (Procurement) diverts to backup supplier TrapicoBlend, issues emergency PO
- T+18.0s: AGNT-17 (Settlement) places $12,600 USDC escrow hold — payment to NutSource paused
- T+24.6s: AGNT-18 (Invoice Processor) blocks NutSource invoice; flags for dispute review
- T+29.1s: AGNT-19 (Cost Tracker) recalculates batch COGS with premium backup supplier pricing
- T+38.8s: AGNT-23 (Blockchain Ledger) writes complete event chain to immutable ledger — all 8 agents, 9 decisions, 3 systems

**Total elapsed: 38.8 seconds.** The same event would take 48 hours manually.

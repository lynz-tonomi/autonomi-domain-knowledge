# Cascade Demo Scenarios Reference
**Skill:** ai-agent-orchestration | **Domain:** demos | **Version:** 1.0.0

---

## 1. Overview

The Autonomi platform has three pre-built demo scenarios accessible via the `run_demo` tool and the Mission Control view. The cascade demo (Supplier Quality Failure) is the centerpiece of the investor tour and fires automatically at CUE 6. Each demo is a choreographed simulation using realistic data — all agent decisions, blockchain records, and payment events are generated as representative examples, not live production data.

---

## 2. Demo 1 — Happy Path (run_demo: 'happy')

### 2.1 Scenario
Normal day operations. A kombucha demand spike triggers a complete agentic procurement-to-production cycle without any human intervention.

### 2.2 Sequence

**T+0s:** Demand Intelligence Agent (AGNT-26) detects 23% POS acceleration for Kombucha 355ml at a regional retail chain.

**T+4s:** AGNT-01 (Demand Planning) updates the 14-day forecast: +18,400 units added to the plan.

**T+9s:** AGNT-03 (Production Scheduler) evaluates LINE-06 capacity. LINE-06 currently at 72% utilization. Adds 2 additional Kombucha batches to the schedule for the coming week.

**T+14s:** AGNT-04 (Inventory Agent) checks SCOBY / starter culture stock. Current on-hand: 1,840 lbs. Requirement for 2 additional batches: 760 lbs additional. Projected balance at run date: 920 lbs — above safety stock. No procurement trigger.

**T+19s:** AGNT-04 also checks black tea extract and sugar supply. Both sufficient. AGNT-03 confirms all 2 additional batches as Tier 2 (scheduled within 72 hrs).

**T+28s:** AGNT-17 (Settlement Agent) pre-stages USDC contracts for projected fermentation inputs — $4,200 total, within auto-approve limit.

**T+34s:** AGNT-13 (FSMA 204 Recorder) opens batch traceability records for both new batches, linking to existing ingredient lot numbers.

**T+41s:** LynZ notification: "We've added two Kombucha batches to the schedule — demand looks strong. Everything's covered, no human action needed."

**Human touchpoints:** 0  
**Total decisions: 14**  
**Blockchain records created: 8**

---

## 3. Demo 2 — Crisis Response (run_demo: 'crisis') / Cascade Demo (trigger_cascade)

### 3.1 Scenario
Supplier Quality Failure with allergen contamination. This is the demo shown at CUE 6 of the investor tour. It demonstrates all three technology layers (OttoClaw security, Ampersend payment hold, domain intelligence) working together.

### 3.2 Full Agent Cascade Sequence

**T+0.0s — AGNT-09 (QC Inspector) fires:**
- Event: Incoming lot LOT-ING-005-20260404-002 (Tropical fruit blend, VND-002 PacificFruit batch)
- Test result: Peanut protein ELISA = 48 ppm
- Internal spec: < 5 ppm (allergen-free declaration)
- Decision: FAIL. Lot placed on HOLD. Production consuming this lot blocked.
- Confidence: 0.999 (analytical result, not AI judgment)

**T+3.2s — AGNT-10 (Allergen Control) fires:**
- Event: Evaluates CCP 3 (Allergen Control) critical limit exceeded
- Decision: CRITICAL ALLERGEN ALERT issued. Tropical 350ml (BOM-04) run blocked pending lot substitution. Allergen sequencing schedule invalidated.
- Blockchain record: ALLERGEN_CCP_DEVIATION written (immutable)

**T+6.8s — AGNT-27 (Risk Assessment) fires:**
- Event: NutSource flagged as allergen-contaminated source
- Cross-reference: NutSource is the sole contracted tropical blend supplier for peanut-adjacent SKUs
- Decision: SUPPLY CONCENTRATION RISK — CRITICAL. Single-source exposure for 28% of BOM-04 ingredient cost.

**T+11.4s — AGNT-05 (Procurement) fires:**
- Event: Backup supplier evaluation triggered
- Selected: VND-011 TrapicoBlend (score 88.3; lead time 6 days)
- Decision: Emergency PO issued. $14,200 USDC. Premium freight included.
- Ampersend policy check: $14,200 > $10,000 auto-approve limit → escalated to Weston (appears in Mission Control)

**T+18.0s — AGNT-17 (Settlement Agent) fires:**
- Event: Outstanding payment to NutSource — invoice #NSI-2847 for $12,600 USDC
- Decision: ESCROW HOLD placed. Smart contract execution suspended.
- Ampersend policy: Payment paused pending quality dispute resolution
- Blockchain record: PAYMENT_HOLD written with allergen event reference

**T+24.6s — AGNT-18 (Invoice Processor) fires:**
- Event: NutSource invoice #NSI-2847 status updated
- Decision: BLOCKED. Invoice routed to dispute queue. BILL.com dispute flag raised.
- ESG Tracker Agent co-fires: Supplier ESG score impact logged (-8 points allergen incident)

**T+29.1s — AGNT-19 (Cost Tracker) fires:**
- Event: COGS recalculation for BOM-04 with TrapicoBlend pricing
- Calculation: TrapicoBlend price $1.84/lb vs. NutSource $1.62/lb; additional 180,000 lbs affected
- Impact: +$39,600 incremental COGS for affected production run
- Decision: Flag for CFO review; COGS variance report generated

**T+38.8s — AGNT-23 (Blockchain Ledger) fires:**
- Event: Complete cascade chain finalized
- Written: 8 agent decision records, 3 cross-system events, 2 payment actions, 1 FSMA 204 deviation record
- All records: cryptographically signed, tamper-proof, timestamped to millisecond

**Human touchpoints:** 1 (PO approval for $14,200 emergency purchase)  
**Total decisions: 18 across 8 agents**  
**Total elapsed: 38.8 seconds**  
**Manual equivalent: 48 hours**

### 3.3 Post-Cascade Summary (shown in Mission Control)

- Contaminated lot: QUARANTINED (ZONE-Q)
- NutSource: SUSPENDED (supplier score flagged for investigation)
- BOM-04 production: BLOCKED until TrapicoBlend lot arrives (ETA: 6 days)
- Payment: $12,600 USDC escrowed (pending dispute resolution)
- Recall risk: NONE (lot never entered production — caught at incoming inspection)
- FSMA record: COMPLETE (full CTE/KDE chain for lot from origin to quarantine)

---

## 4. Demo 3 — Scale Test (run_demo: 'scale')

### 4.1 Scenario
Platform stress demonstration — shows Autonomi operating at network scale across all 4 active tenants simultaneously.

### 4.2 What It Shows

**Network metrics flashing live:**
- 2,417 active nodes
- 842 production lines
- 126,840 IoT sensors reporting
- 2.4M decisions processed in prior 24 hours
- $84.2M USDC monthly transaction aggregate

**Simulated multi-tenant activity:**
- PurePress (Enterprise): 29 agents active, 487 decisions/hr
- Cascade Drinks (Growth): 10 agents active, 198 decisions/hr
- VitaFlow (Growth): 10 agents active, 214 decisions/hr
- SunRise RTD (Starter): 5 agents active, 87 decisions/hr

**Cross-tenant intelligence demonstration:**
- Network Intelligence Agent (AGNT-29) surfaces: "Citrus concentrate prices trending +6.2% across 18 buyers on the platform — your contract with CitroSource locks your cost for 90 more days. That's a $184K advantage vs. spot market."
- Predictive recall detection: "Batch correlation analysis across 3 tenants sharing a common pectin supplier shows a Brix deviation pattern. Flag raised for proactive investigation."

**Total runtime:** ~45 seconds  
**Purpose:** Show investors the platform's scale and the unique value of cross-network data.

---

## 5. Demo Trigger Reference

| Tool | Scenario | When to Use |
|---|---|---|
| `trigger_cascade()` | Supplier Quality Failure (Demo 2) | CUE 6 of investor live tour |
| `run_demo('happy')` | Normal operations cycle | When asked to show day-to-day flow |
| `run_demo('crisis')` | Same as cascade but via run_demo API | Ad-hoc crisis demo outside tour |
| `run_demo('scale')` | Network scale visualization | When pitching platform scale to investors |

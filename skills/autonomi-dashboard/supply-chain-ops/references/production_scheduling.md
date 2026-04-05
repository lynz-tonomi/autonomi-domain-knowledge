# Production Scheduling Reference
**Skill:** supply-chain-ops | **Domain:** production-scheduling | **Version:** 1.0.0

---

## 1. Overview

Autonomi manages production scheduling across PurePress Beverages' beverage manufacturing operation. The scheduling system handles 8 active product lines, batch sequencing, allergen changeovers, and capacity planning. The Production Scheduler Agent (AGNT-03) runs continuously, re-optimizing the schedule every 15 minutes based on ingredient availability, demand signals, equipment status, and allergen sequencing rules.

---

## 2. Active Production Lines

| Line ID | Type | Capacity (gal/hr) | Fill Format | Current OEE |
|---|---|---|---|---|
| LINE-01 | Hot-fill juice | 3,200 | 500ml PET | 87.4% |
| LINE-02 | Hot-fill juice | 3,200 | 330ml / 1L PET | 84.1% |
| LINE-03 | Cold-fill | 2,800 | 350ml / 500ml PET | 91.2% |
| LINE-04 | Cold-fill | 2,800 | 250ml / 500ml PET | 88.6% |
| LINE-05 | Aseptic | 4,100 | 1L Tetra | 79.3% |
| LINE-06 | Kombucha fermentation/fill | 1,600 | 355ml glass | 82.7% |
| LINE-07 | Oat milk (UHT) | 2,200 | 1L Tetra | 86.0% |
| LINE-08 | Overflow / flex | 2,400 | Any PET | 74.5% |

**OEE Target:** 85.0% across all lines  
**Network Average OEE (all tenants):** 83.2%

---

## 3. Active BOM Assignments to Lines

| BOM ID | Product | Line Assignment | Batch Size (gal) | Run Duration |
|---|---|---|---|---|
| BOM-01 | OJ 500ml | LINE-01 | 8,500 | ~2.7 hrs |
| BOM-02 | Citrus 330ml | LINE-02 | 12,000 | ~3.75 hrs |
| BOM-03 | Apple 1L | LINE-02 or LINE-05 | 6,500 | ~2.0 hrs |
| BOM-04 | Tropical 350ml | LINE-03 | 42,000 | ~15.0 hrs |
| BOM-05 | Berry 250ml | LINE-04 | 18,750 | ~6.7 hrs |
| BOM-06 | Mango 500ml | LINE-03 or LINE-04 | 15,000 | ~5.4 hrs |
| BOM-07 | Kombucha 355ml | LINE-06 | 28,500 | ~17.8 hrs |
| BOM-08 | Oat Milk 1L | LINE-07 | 10,000 | ~4.5 hrs |

---

## 4. Scheduling Logic

### 4.1 Priority Tiers

The scheduler applies a 3-tier priority system every scheduling cycle:

**Tier 1 — Immediate (run within 24 hrs):**
- Confirmed customer orders with delivery date ≤ 72 hrs
- Ingredients expiring within 14 days (FEFO trigger from inventory agent)
- Reactive production triggered by demand forecast spike > 20%

**Tier 2 — Planned (run within 72 hrs):**
- Regular replenishment batches from demand plan
- Seasonal volume buildup (flagged by Demand Planning Agent AGNT-12)
- Safety stock replenishment below 1.5× reorder point

**Tier 3 — Scheduled (run within 7 days):**
- Advance production for promotional periods
- Campaign runs for long-run efficiency (see Section 6)
- Trial batches for new formulations

### 4.2 Constraint Hierarchy

When the scheduler encounters conflicts, it resolves them in this order:
1. Allergen sequencing (non-negotiable — see Section 5)
2. Ingredient availability (confirmed by procurement agent)
3. Customer order due dates
4. Line OEE optimization (group similar fills, minimize changeovers)
5. FEFO compliance for expiring ingredients
6. Energy cost (off-peak scheduling preferred when constraints allow)

---

## 5. Allergen Changeover Protocols

PurePress produces products with tree nuts (almond milk adjacent), oats (gluten cross-contact risk), and soy. Allergen sequencing is the highest-priority constraint in the schedule.

### 5.1 Allergen Matrix

| From Product | To Product | Changeover Type | Min Downtime |
|---|---|---|---|
| Oat Milk (BOM-08) | Any juice | Full wet clean + ATP verify | 4 hrs |
| Any juice | Oat Milk (BOM-08) | Full wet clean + ATP verify | 4 hrs |
| Citrus (BOM-02) | OJ (BOM-01) | Rinse + quick wet clean | 45 min |
| OJ (BOM-01) | Citrus (BOM-02) | Rinse + quick wet clean | 45 min |
| Any juice | Kombucha (BOM-07) | Full CIP + culture swab | 6 hrs |
| Kombucha (BOM-07) | Any other | Full CIP + culture swab | 6 hrs |
| Tropical (BOM-04) | Berry (BOM-05) | Flavor flush + wet clean | 1.5 hrs |
| Berry (BOM-05) | Tropical (BOM-04) | Flavor flush + wet clean | 1.5 hrs |

### 5.2 Scheduling Rule
The allergen agent (AGNT-18) must validate every scheduled changeover before the run is confirmed. If an allergen conflict is detected, the scheduler blocks the transition and proposes an alternative sequence.

---

## 6. Campaign Runs

Campaign runs batch multiple production lots of the same product consecutively to minimize changeover frequency and maximize line OEE. The scheduler identifies campaign opportunities when:
- Forecast demand covers ≥ 3 consecutive batches
- Ingredient supply is secured for all batches (confirmed by procurement agent)
- Storage capacity is available for finished goods (checked against warehouse capacity)

**Campaign run savings (average):**
- OJ 500ml: 2–3 batches per campaign → saves 1.5 hrs changeover per campaign cycle
- Tropical 350ml: 2 batches → saves 3.2 hrs (long hot-fill rinse)
- Kombucha: single campaign per fermentation cycle (biological constraint)

---

## 7. Capacity Planning

### 7.1 Weekly Available Hours

Each line operates on a 5-day / 2-shift schedule with a 4-hr maintenance window on Sundays.

| Shift | Hours |
|---|---|
| Day shift | 06:00–18:00 (12 hrs) |
| Night shift | 18:00–06:00 (12 hrs) |
| Planned downtime | ~1.5 hrs/day (CIP, micro, pre-op) |
| Net available per line/day | ~22.5 hrs |
| Net available per line/week | ~112.5 hrs |

### 7.2 Utilization Thresholds

| Status | Utilization Range | Action |
|---|---|---|
| Underutilized | < 60% | Flag for campaign consolidation |
| Optimal | 60–85% | No action |
| High load | 85–95% | Request capacity confirmation from ops manager |
| Overloaded | > 95% | Auto-escalate: block new Tier 3 orders, alert LynZ |

### 7.3 Line Balance Logic

The scheduler distributes load across lines to avoid single-line overloading. When LINE-03 utilization exceeds 90%, the scheduler evaluates whether Mango (BOM-06) or Berry (BOM-05) can shift to LINE-04 or LINE-08 without allergen conflict.

---

## 8. Schedule Change Triggers

The scheduler auto-revises the published schedule when any of the following events occur:

| Trigger | Source Agent | Response |
|---|---|---|
| Ingredient ETA slip > 4 hrs | Procurement Agent (AGNT-05) | Reschedule affected batch; prioritize next available ingredient lot |
| IoT temperature excursion on raw material | IoT Monitor (AGNT-19) | Hold batch; flag QA agent; reschedule if ingredient quarantined |
| Line downtime > 2 hrs unplanned | Maintenance system / manual flag | Re-sequence remaining batches; evaluate overtime or LINE-08 overflow |
| Customer order expedite request | Order Management | Promote batch to Tier 1; evaluate Tier 3 deferral |
| Demand spike > 20% | Demand Planning Agent (AGNT-12) | Add Tier 2 batch; verify ingredient coverage with procurement |
| Quality hold on finished goods | QA Agent (AGNT-08) | Pull hold batch from dispatch; evaluate rework or disposal |

---

## 9. Key Performance Indicators

| KPI | Target | Current | Trend |
|---|---|---|---|
| Overall OEE (all lines) | 85.0% | 85.8% | +0.4% MoM |
| Schedule Adherence | ≥ 92% | 94.1% | Stable |
| Batch Start On-Time (within 30 min) | ≥ 95% | 96.3% | +0.8% MoM |
| Unplanned Downtime | ≤ 3.0% of available time | 2.7% | Improving |
| Changeover Efficiency | ≤ 110% of standard time | 104.2% | Improving |
| Fill Accuracy | ≥ 98.5% | 98.7% | Stable |

---

## 10. Batch Numbering Convention

All batches follow the convention: `{SITE}-{LINE}-{YYYYMMDD}-{SEQ}`

Example: `PPB-L01-20260404-003` = PurePress Beverages, Line 01, April 4 2026, 3rd batch of the day.

Batch records are written to the blockchain at:
- Batch creation (schedule confirmed)
- Run start (first unit filled)
- Run end (last unit filled)
- QA release or hold decision
- Outbound dispatch

---

## 11. Integration Points

- **Inventory Agent (AGNT-04):** Confirms ingredient availability before batch confirmation
- **Procurement Agent (AGNT-05):** Triggers emergency POs if ingredient coverage < 1 batch
- **QA Agent (AGNT-08):** Releases or holds each batch upon completion
- **Blockchain Ledger (AGNT-20):** Records all batch events as immutable transactions
- **ERP Sync (AGNT-21):** Pushes production orders to SAP/NetSuite in real time
- **IoT Monitor (AGNT-19):** Feeds real-time line status to scheduler for reactive re-sequencing

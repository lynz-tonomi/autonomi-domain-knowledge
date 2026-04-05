# Recall Management Reference
**Skill:** blockchain-traceability | **Domain:** recall | **Version:** 1.0.0

---

## 1. Overview

Recall management is one of the highest-stakes operations in food manufacturing. Autonomi's Recall Coordinator Agent (AGNT-14) manages the full recall workflow: detection, classification, distribution trace, customer notification, regulatory reporting, and recovery. All recall decisions require human sign-off — AGNT-14 provides analysis and recommendations but does not execute a public recall autonomously. Response time from trigger to full distribution trace is under 4 hours.

---

## 2. Recall Classifications

### 2.1 FDA Class Definitions

| Class | Definition | Example Trigger | Response Timeline |
|---|---|---|---|
| Class I | Reasonable probability of serious adverse health consequences or death | Undeclared peanut allergen; Listeria monocytogenes in RTE; E. coli O157:H7 | Initiate within 24 hrs; public notification possible |
| Class II | Remote probability of adverse health consequences, or consequences are temporary/reversible | Undeclared minor ingredient; slight label error; low-level pesticide | Initiate within 48 hrs |
| Class III | Unlikely to cause adverse health consequences | Minor labeling discrepancy; fill weight slightly below declared | Initiate within 5 days |
| Market Withdrawal | Not a formal FDA recall; voluntary removal for minor quality issues | Off-specification color; minor sensory defect | No FDA reporting required |

---

## 3. Recall Trigger Sources

AGNT-14 monitors for recall triggers from multiple sources:

| Source | Trigger Type | Example |
|---|---|---|
| AGNT-09 (QC Inspector) | Failed finished product testing | Pathogens detected in retain sample |
| AGNT-10 (Allergen Control) | Undeclared allergen risk identified | Post-production discovery of allergen in ingredient |
| AGNT-22 (IoT Monitor) | Cold chain failure during distribution | Extended temperature excursion in transit |
| Customer complaint | Consumer adverse event report | Multiple illness reports linked to batch |
| Supplier notification | Supplier issues voluntary recall of ingredient | Supplier notifies of contaminated lot post-delivery |
| FDA notification | FDA inspection finding or import alert | FDA detects issue in routine surveillance |
| AGNT-29 (Network Intelligence) | Cross-tenant pattern | Multiple tenants sharing same supplier show correlated failures |

---

## 4. Recall Procedure — Step by Step

### Phase 1: Initiation (0–2 hours)

1. **Trigger detected** — AGNT-14 receives signal from triggering source
2. **Immediate escalation** — LynZ voice notification to Weston; Mission Control alert fired
3. **Lot identification** — AGNT-13 pulls all TLCs for affected batches from blockchain
4. **Hold placed** — AGNT-04 places all affected finished goods in ZONE-Q (quarantine); production halted on affected lines
5. **Distribution trace begun** — AGNT-14 queries shipping CTEs: where did every case go?

### Phase 2: Scope Assessment (2–4 hours)

6. **Distribution map generated** — Blockchain query returns complete customer-by-customer breakdown: facility, DC, retail, consumer-facing
7. **Quantity accounting** — Total units affected = units produced − units still in warehouse inventory − units already consumed (with confidence range)
8. **Risk classification** — AGNT-14 proposes recall class based on hazard type; human confirms
9. **FDA notification decision** — If Class I or II, 21-day voluntary recall reporting window. Autonomi generates FDA Form 3177 (Firm Recall Report) draft.
10. **Customer notification list** — AGNT-14 generates prioritized list of customers to contact

### Phase 3: Notification (4–24 hours)

11. **Customer alerts sent** — LynZ emails affected customers via `send_email` tool; letters of recall issued with lot numbers, best-by dates, return instructions
12. **Press release prepared** (if public notification warranted) — Draft prepared for Weston review
13. **FDA submission** — Recall report submitted if Class I or II
14. **Regulatory liaison** — AGNT-16 tracks FDA correspondence; logs all communications to blockchain

### Phase 4: Recovery (24 hours–30 days)

15. **Returned goods processing** — AGNT-04 receives returned lots; quarantines; routes to destruction or rework
16. **Root cause investigation** — AGNT-11 (CAPA Manager) opens formal CAPA; assigns root cause analysis
17. **Effectiveness check** — AGNT-14 verifies recall effectiveness (≥ 95% of affected product accounted for per FDA guidance)
18. **FDA recall termination request** — Submitted when effectiveness criteria met
19. **Post-recall review** — Management review of root cause findings; preventive actions implemented

---

## 5. Distribution Trace Capability

### 5.1 Sample Trace Query — NutSource Allergen Scenario

When AGNT-14 executes a distribution trace for TLC-BOM04-20260404-001:

```
Trace query: All shipments containing TLC-BOM04-20260404-001
Blockchain query time: 1.8 seconds
Results:

NorCal DC (Sacramento, CA):
  - Received: 18,400 cases (220,800 units)
  - Shipped to 14 retail DCs: 16,200 cases
  - Retail DCs: Whole Foods NorCal (4,800), Sprouts NorCal (3,200), Costco NorCal (5,400), Lucky Stores (2,800)
  - Still in DC: 2,200 cases — HOLD PLACED

Pacific NW DC (Portland, OR):
  - Received: 9,200 cases (110,400 units)
  - Shipped to 8 retail DCs: 8,100 cases
  - Retail DCs: New Seasons (2,400), Fred Meyer (3,100), PCC Markets (2,600)
  - Still in DC: 1,100 cases — HOLD PLACED

National 3PL (Dallas, TX):
  - Received: 24,600 cases (295,200 cases)
  - Cross-docked to 19 retail accounts: 22,800 cases
  - Still in 3PL: 1,800 cases — HOLD PLACED

TOTAL AFFECTED: 52,200 cases / 626,400 units
ACCOUNTED FOR (in warehouse/DC): 5,100 cases (9.8%)
AT RETAIL / CONSUMER LEVEL: 47,100 cases — NOTIFICATION REQUIRED
```

### 5.2 Why This Trace Ran in < 4 Hours

Traditional recall trace relies on paper records, Excel spreadsheets, email chains, and phone calls to trading partners. Average time to complete: 3–7 days. Autonomi's trace completes in 4 minutes because every shipping CTE was recorded to the blockchain in real time at the moment of dispatch. The query is a database lookup against cryptographically verified immutable records.

---

## 6. Mock Drill — Annual Requirement

AGNT-14 conducts a mock recall drill annually for each tenant:
- Randomly selects a production batch from the prior 6 months
- Executes distribution trace
- Generates customer notification list
- Measures time to complete (target: < 4 hours)
- Documents findings in recall plan effectiveness review

**Last drill result (PurePress):** 2 hours 14 minutes to full trace. 100% of distribution accounted for.

---

## 7. Recall Cost Estimation

AGNT-14 generates a recall cost estimate as part of the incident report:

| Cost Category | Estimation Method |
|---|---|
| Product value destroyed | Units × wholesale price |
| Return freight | Cases recalled × avg freight cost/case |
| Destruction/disposal | Contracted rate per pallet |
| Customer credit | Cases recalled × invoice price |
| Regulatory and legal (estimated) | Fixed provision: $250K for Class I, $75K for Class II |
| Brand impact (market withdrawal scenario) | Not modeled — escalate to management |

**Example Class I recall (626,400 units, wholesale $2.40):** Estimated direct cost: $1.85M–$2.4M
**Platform ROI argument:** One avoided Class I recall > Autonomi platform cost for the year.

---

## 8. Recall Page on Dashboard

Navigate to `quality-alerts` for the Recall & Trace page. This page shows:
- Active recalls (if any) with status and timeline
- Recall history log
- Distribution trace tool: enter lot/TLC → full trace result
- Mock drill scheduler
- FDA correspondence log

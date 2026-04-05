# Alert Rules Reference
**Skill:** iot-monitoring | **Domain:** alerts | **Version:** 1.0.0

---

## 1. Alert Architecture

All alerts flow through a four-tier escalation chain:
1. **IoT sensor** fires reading to AGNT-22
2. **AGNT-22** applies threshold logic → classifies severity → routes to relevant agent
3. **Relevant agent** takes automated action → escalates to LynZ if human needed
4. **LynZ** → Weston voice notification for Critical alerts

---

## 2. Temperature Alert Rules

### 2.1 Cold Storage — ZONE-R (Refrigerated)

| Condition | Severity | Automated Response |
|---|---|---|
| Temp 40–42°F | Advisory | Log; increase monitoring to every 1 min |
| Temp 42–45°F | Warning | AGNT-22 alerts AGNT-04; flag affected lots for review |
| Temp > 45°F for > 30 min | Alert | AGNT-04 places all lots in zone on Hold; AGNT-22 notifies maintenance; LynZ alert |
| Temp > 50°F at any time | Critical | Immediate Hold; product assessment required; LynZ voice notification to Weston |
| Temp > 40°F after door close event | Advisory | Verify door sealed; log event |
| Door open > 5 min | Warning | Alert receiving/warehouse staff |
| Door open > 10 min | Alert | AGNT-22 alerts supervisor; log excursion |

### 2.2 Cold Storage — ZONE-F (Frozen)

| Condition | Severity | Automated Response |
|---|---|---|
| Temp 0–5°F | Advisory | Log; monitor for trend |
| Temp 5–15°F | Warning | Alert maintenance; check compressor status |
| Temp > 15°F for > 30 min | Alert | AGNT-04 places lots on Hold; maintenance emergency call |
| Temp > 25°F | Critical | LynZ voice notification; immediate escalation; assess thaw damage |

### 2.3 CCP-3 — Pasteurizer (Highest Priority)

| Condition | Severity | Automated Response |
|---|---|---|
| Temp 159–161°F (approaching CL) | Warning | Alert line operator; check heat exchanger |
| Temp < 161°F for any reading | CCP DEVIATION — CRITICAL | Flow diversion valve activates; production halted; AGNT-09 notified; CAPA opened; LynZ immediate voice alert |
| Temp sensor failure (offline) | Critical | Production halted; backup sensor engaged; maintenance called |
| > 5°F variance between dual sensors | Alert | Investigate; do not use primary until resolved |

**CCP-3 is the highest-priority alert on the platform. Any reading below 161°F immediately halts production.**

### 2.4 CCP-4 — Hot Fill (LINE-01 and LINE-02)

| Condition | Severity | Automated Response |
|---|---|---|
| Temp 183–185°F (approaching CL) | Warning | Alert line operator; check heater |
| Temp < 185°F for any reading | CCP DEVIATION — CRITICAL | Halt fill; hold units back to last passing check; AGNT-09 notified; LynZ alert |

### 2.5 CCP-4 — Cold Fill (LINE-03 and LINE-04)

| Condition | Severity | Automated Response |
|---|---|---|
| Temp 40–42°F | Warning | Alert line operator |
| Temp > 42°F at fill | CCP DEVIATION — Alert | Evaluate: brief excursion (< 5 min): hold and recheck; sustained: halt line |

---

## 3. pH Alert Rules

### 3.1 Inline pH — Juice Products (CCP-2)

| Condition | Severity | Automated Response |
|---|---|---|
| pH within product spec | Normal | No action |
| pH 0.1–0.2 outside spec | Warning | Alert blending operator; adjust acid or dilution |
| pH > 4.0 for juice (approaching safety limit) | Alert | AGNT-09 notified; hold batch pending investigation |
| pH > 4.6 (acidified food safety limit) | CCP DEVIATION — CRITICAL | Halt; hold batch; processing authority consultation required; LynZ alert |
| pH probe offline / calibration drift > 0.3 | Alert | Switch to benchtop verification; flag for sensor calibration |

### 3.2 Kombucha pH (CCP-5)

| Condition | Severity | Automated Response |
|---|---|---|
| pH 3.0–3.2 (spec range) | Normal | No action |
| pH 3.2–3.4 | Warning | Continue fermentation; recheck in 4 hours |
| pH > 3.4 | Alert | Do not fill; continue fermentation; escalate to QA |
| pH < 2.8 | Warning | Evaluate blend adjustment; possible over-fermentation |
| pH < 2.6 | Alert | Product may be unacceptably tart; QA evaluation required |

---

## 4. Brix Alert Rules

### 4.1 Inline Brix — All Products (CCP-2)

| Condition | Severity | Automated Response |
|---|---|---|
| Brix within product spec | Normal | No action |
| Brix 0.3 °Bx outside spec | Warning | Alert operator; adjust |
| Brix 0.5+ °Bx outside spec | Alert | Hold batch; investigate formulation or concentrate strength |
| Brix sensor offline | Alert | Switch to benchtop verification; flag for calibration |

---

## 5. CIP Sensor Alert Rules

| Parameter | Alert Condition | Response |
|---|---|---|
| Caustic wash temp < 155°F | Warning: below min spec | Extend wash time; re-evaluate wash effectiveness |
| Caustic wash temp < 145°F | Alert: CIP invalid | Abort CIP; investigate; restart full CIP sequence |
| Caustic conductivity < 1.5% | Warning | Replenish detergent; check concentration |
| CIP spray pressure < 15 PSI | Alert | Check pump; verify spray pattern; do not release equipment until corrected |

---

## 6. Fermentation Tank Alert Rules

| Parameter | Alert Condition | Response |
|---|---|---|
| Temperature > 82°F (27.8°C) | Warning | Check cooling; adjust jacket |
| Temperature > 86°F (30°C) | Alert | Cooling failure; emergency check; culture viability at risk |
| Temperature < 68°F (20°C) | Warning | Check heating; may slow fermentation significantly |
| CO2 > 0.8% headspace | Warning | Check pressure relief; ventilation |

---

## 7. In-Transit Alert Rules (Outbound Cold Chain)

| Condition | Severity | Automated Response |
|---|---|---|
| Temp 40–42°F in transit (refrigerated) | Warning | AGNT-07 notifies driver; monitor closely |
| Temp > 42°F for 30–120 min | Alert | AGNT-07 contacts carrier ops; flag delivery for hold at DC |
| Temp > 42°F for > 2 hrs | Critical | Shipment quarantined at destination; customer notified; QA assessment |
| Logger communication dropout > 2 hrs | Alert | Attempt reconnect; notify carrier to check logger |
| Frozen load > -5°F | Alert | Carrier check immediately; customer may refuse delivery |

---

## 8. Alert Notification Matrix

| Severity | AGNT-22 Action | LynZ Role | Weston Notification |
|---|---|---|---|
| Advisory | Log; no external notification | None | No |
| Warning | Notify relevant operations agent | None (unless escalated) | No |
| Alert | Notify relevant agent + operations; create incident log | Voice notification if sustained | Dashboard notification |
| Critical | Immediate multi-agent cascade; CAPA opened; blockchain record | Immediate voice notification | Yes — voice + dashboard |
| CCP Deviation | HALT PRODUCTION; immediate escalation | Immediate voice: "We have a CCP deviation on [line]" | Yes — immediate |

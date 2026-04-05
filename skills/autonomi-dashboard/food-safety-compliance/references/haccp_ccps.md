# HACCP Critical Control Points Reference
**Skill:** food-safety-compliance | **Domain:** haccp | **Version:** 1.0.0

---

## 1. HACCP Plan Overview — PurePress Beverages

PurePress Beverages maintains a validated HACCP plan covering all 8 product lines. The plan was developed by a certified HACCP team, validated by an independent processing authority for thermal process products, and is reviewed annually and upon any significant process change. Under FSMA, the HACCP plan has been integrated into the broader Food Safety Plan (HARPC) per 21 CFR Part 117.

**Products covered:** OJ 500ml, Citrus 330ml, Apple 1L, Tropical 350ml, Berry 250ml, Mango 500ml, Kombucha 355ml, Oat Milk 1L

---

## 2. Process Flow Summary

```
Raw Ingredient Receipt
    ↓ CCP-1: Incoming Ingredient Temperature Verification
Storage (Refrigerated / Frozen / Ambient)
    ↓
Water Treatment
    ↓
Blending / Formulation
    ↓ CCP-2: Brix / pH Verification (pre-process)
Pasteurization / Thermal Treatment
    ↓ CCP-3: Pasteurization Temperature / Time
Hot Fill (Lines 1–2) / Cold Fill (Lines 3–4) / Aseptic Fill (Line 5)
    ↓ CCP-4: Fill Temperature / Seal Integrity
Cooling / Chilling
    ↓
Fermentation (Kombucha only)
    ↓ CCP-5: Final pH Verification (Kombucha)
Labeling
    ↓ CCP-6: Label Verification (allergen declaration)
Metal Detection
    ↓ CCP-7: Metal Detection
Distribution / Cold Chain
```

---

## 3. CCP-1 — Incoming Ingredient Temperature Verification

**Hazard:** Biological — pathogen growth in temperature-abused refrigerated/frozen ingredients
**Critical Limit:** Refrigerated ingredients ≤ 40°F (4.4°C) at receipt; frozen ingredients ≤ 0°F (-17.8°C)
**Monitoring:**
- Method: IoT temperature logger data from carrier + manual thermometer check at dock
- Frequency: Every delivery of temperature-sensitive ingredients
- Responsible: AGNT-22 (auto) + receiving technician (manual verification)
**Corrective Action:**
- If refrigerated > 40°F: Place lot on Hold; QA review; temperature excursion evaluation per written procedure
- If refrigerated > 45°F: Automatic rejection; return to supplier; root cause investigation
- If frozen > 10°F: Place on Hold; QA review; evaluate thaw/refreeze cycle risk
**Verification:**
- AGNT-22 reviews 100% of IoT temperature records daily
- Monthly calibration verification of dock thermometers
- Quarterly review of corrective actions taken
**Records:** IoT temperature log (on-chain), receiving log, corrective action records (AGNT-11)

---

## 4. CCP-2 — Pre-Process Brix / pH Verification

**Hazard:** Chemical — improper formulation leading to pH > 4.6 in acidified products; biological — insufficient water activity or pH to control pathogen growth
**Critical Limit:**
- Brix at blending: Product-specific (see table below)
- pH: ≤ 4.0 for juice products; ≤ 3.2 for kombucha; ≤ 4.6 (absolute) for acidified foods

| Product | Brix Spec | pH Spec |
|---|---|---|
| OJ 500ml | 11.0–12.5 °Bx | 3.6–3.9 |
| Citrus 330ml | 10.5–11.5 °Bx | 3.5–3.8 |
| Apple 1L | 11.5–12.5 °Bx | 3.7–4.0 |
| Tropical 350ml | 12.0–13.5 °Bx | 3.6–3.9 |
| Berry 250ml | 11.0–12.5 °Bx | 3.3–3.6 |
| Mango 500ml | 12.5–14.0 °Bx | 3.7–4.0 |
| Kombucha 355ml | 5.0–7.0 °Bx | 2.8–3.2 |
| Oat Milk 1L | 10.0–13.0 total solids | 6.5–7.2 |

**Monitoring:**
- Method: In-line refractometer (Brix) + calibrated pH meter
- Frequency: Every batch — beginning, middle, and end of blend
- Responsible: Line QA technician + AGNT-09 (automated result entry)
**Corrective Action:**
- Brix out of spec: Adjust formulation (add concentrate or dilution water); recheck before proceeding
- pH out of spec: Adjust acid addition; recheck; if pH > 4.6 on acidified product, hold batch pending processing authority review
**Verification:**
- AGNT-09 reviews all in-process check records each shift
- pH meter calibrated with buffer solutions at start of each shift (pH 4.0 and 7.0)
- Monthly correlation study: inline vs. benchtop pH meter
**Records:** In-process check log (QC Inspection page), meter calibration log, corrective action records

---

## 5. CCP-3 — Pasteurization Temperature / Time

**Hazard:** Biological — survival of pathogenic organisms (Salmonella, E. coli O157:H7, Listeria monocytogenes, Cryptosporidium in cider)
**Critical Limit:**
- HTST pasteurization: ≥ 161°F (71.7°C) for ≥ 15 seconds (21 CFR 179.30 reference)
- Ultra-pasteurization: ≥ 280°F (138°C) for ≥ 2 seconds
- Kombucha fermentation: Not thermally treated post-fill (live culture); CCP is pH (CCP-5)
- Oat milk (UHT): ≥ 280°F (138°C) for ≥ 2 seconds; hermetically sealed

**Monitoring:**
- Method: Calibrated thermocouples in pasteurizer holding tube + flow diversion valve
- Frequency: Continuous (every 1 second) via SCADA; chart recorded
- Responsible: AGNT-22 (continuous monitoring) + equipment operator
**Corrective Action:**
- Temperature drop below critical limit: Flow diversion valve activates automatically; product diverted back to raw tank; process engineer notified; root cause investigation; do not advance to fill until critical limit achieved and sustained for ≥ 5 minutes
**Verification:**
- AGNT-22 reviews all pasteurizer temperature records every 2 hours
- Weekly thermocouple calibration against NIST-traceable reference
- Annual pasteurization validation study (D-value test for target organisms)
- Flow diversion valve function test: weekly
**Records:** Pasteurizer chart recorder (retained 2 years), corrective action log, calibration records

---

## 6. CCP-4 — Fill Temperature / Seal Integrity

**Hazard:** Biological — pathogen recontamination post-pasteurization; chemical — inadequate seal allowing O2 ingress (shelf-life failure)
**Critical Limits:**
- Hot-fill products: Fill temperature ≥ 185°F (85°C) at point of fill (self-sterilizing)
- Cold-fill products: Fill temperature ≤ 40°F (4.4°C) (prevents thermophile growth)
- Aseptic fill: Container sterility confirmed; fill room class 100,000 (ISO 8) maintained
- Seal integrity: Pull tab torque ≥ 14 in-lbs (HDPE cap); leak test pass at 30 PSI

**Monitoring:**
- Method: Inline fill temperature sensor + torque tester + vacuum/pressure leak tester
- Frequency: Every 15 minutes during fill run + 1 unit per 500 torque check + 6 units/hour leak test
- Responsible: Line QA technician + AGNT-09 (automated data entry)
**Corrective Action:**
- Hot-fill temp < 185°F: Hold affected units (from last passing check); recheck fill temp; investigate heater failure
- Torque failure: Reject cap; re-apply; check capper settings; pull 10-unit test sequence
- Leak failure: Hold affected units; investigate sealer settings; check cap/bottle interface
**Records:** Fill temperature log, torque log, leak test log, corrective action records

---

## 7. CCP-5 — Final pH Verification (Kombucha)

**Hazard:** Biological — insufficient acidity to control pathogen survival; chemical — over-fermentation
**Critical Limit:** Final kombucha pH ≤ 3.2 at bottling; acetic acid ≥ 0.5% by titration
**Monitoring:**
- Method: Calibrated benchtop pH meter; titratable acidity test
- Frequency: Every fermentation tank at time of transfer to fill; once per 2 hours during fill
- Responsible: Kombucha QA specialist + AGNT-09
**Corrective Action:**
- pH > 3.2: Return to fermentation tank; continue fermentation; recheck every 4 hours
- pH < 2.8: Evaluate for blend adjustment; QA review (product may be too tart)
- Acetic acid < 0.5%: Continue fermentation; recheck
**Records:** Fermentation log, pH meter calibration records, AGNT-09 in-process records

---

## 8. CCP-6 — Label Verification (Allergen Declaration)

**Hazard:** Chemical/biological — undeclared allergen; mislabeling leading to consumer harm
**Critical Limit:** 100% of labeled containers must correctly declare all allergens present per 21 CFR 101.4 and FASTER Act (2023 — sesame added to Big-9)
**Monitoring:**
- Method: Vision system label inspection (camera + OCR) + manual check at start of each run + allergen line check form
- Frequency: 100% automated vision inspection; manual check every 30 min; 100% human check at product changeover
- Responsible: AGNT-10 (allergen sequence validation) + line QA technician
**Corrective Action:**
- Wrong label detected: Stop line immediately; quarantine all mislabeled units; identify exact extent of mislabeling by time/count; evaluate recall risk; notify QA manager
- Allergen added to product not declared on label: Class I recall risk — immediate escalation to food safety manager; AGNT-14 activated
**Records:** Vision system logs, manual label check records, AGNT-10 allergen clearance records

---

## 9. CCP-7 — Metal Detection

**Hazard:** Physical — metallic foreign material in finished product
**Critical Limit:** Reject any unit triggering metal detector at:
- Ferrous: ≥ 1.5 mm sphere
- Non-ferrous: ≥ 2.0 mm sphere
- Stainless steel: ≥ 2.5 mm sphere

**Monitoring:**
- Method: Online metal detector (Mettler-Toledo or equivalent); test samples at start, every 30 min, and end of each shift
- Frequency: 100% of finished units pass through detector; validation with test pieces 3x per shift
- Responsible: Line operator + QA technician
**Corrective Action:**
- Reject signal triggered: Stop conveyor; remove and quarantine rejected unit; identify cause (product effect, equipment, actual metal); if actual metal — quarantine all product back to last passing check; investigation + CAPA
- Test piece not detected: Shut down detector; do not run product; service call; re-validate before restart
**Records:** Metal detector test log, reject event log, calibration records, corrective action records

---

## 10. Monitoring Summary Table

| CCP | Critical Limit | Monitor Method | Frequency | Agent |
|---|---|---|---|---|
| CCP-1 | Temp ≤ 40°F/0°F at receipt | IoT + manual thermometer | Every delivery | AGNT-22 |
| CCP-2 | Brix and pH within spec | Refractometer + pH meter | Every batch, 3x | AGNT-09 |
| CCP-3 | Pasteurization ≥ 161°F/15s | SCADA thermocouple | Continuous | AGNT-22 |
| CCP-4 | Fill temp + seal integrity | Inline sensor + torque/leak | Every 15 min | AGNT-09 |
| CCP-5 | Kombucha pH ≤ 3.2 | Benchtop pH meter | Per tank + every 2 hrs | AGNT-09 |
| CCP-6 | Label allergen accuracy | Vision system + manual | 100% + every 30 min | AGNT-10 |
| CCP-7 | Metal ≥ 1.5 mm rejected | Online metal detector | 100% + 3x/shift test | Line operator |

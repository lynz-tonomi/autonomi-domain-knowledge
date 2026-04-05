# Environmental Compliance Reference
**Skill:** iot-monitoring | **Domain:** environmental | **Version:** 1.0.0

---

## 1. Regulatory Basis for Environmental Monitoring

### 1.1 FDA Requirements

| Regulation | Requirement | Relevance to IoT |
|---|---|---|
| 21 CFR 117.135 | Process preventive controls: monitoring, corrective actions | CCP sensors must monitor at defined frequency |
| 21 CFR 117.137 | Corrective actions and corrections | Automated response chain must be documented |
| 21 CFR 117.145 | Verification activities | Sensor calibration records = verification |
| 21 CFR 117.190 | Record retention: 2 years for monitoring records | All IoT records on blockchain + archive |
| 21 CFR 1.908 | Sanitary Transport of Human and Animal Food | Refrigerated transport ≤ 41°F; AGNT-07 monitors |
| FDA FSMA PC Rule for Human Food | EMP for Listeria recommended for facilities with high-care zones | EMP program in quality_systems.md |

### 1.2 HACCP Linkage

Every CCP has at least one dedicated IoT sensor:
- CCP-1: IOT-DOCK-TEMP-01/02/03 (receiving temperature)
- CCP-2: IOT-LINE-PH, IOT-LINE-BRIX (in-process Brix/pH)
- CCP-3: IOT-PAST-01/02/03 (pasteurizer temperature — CRITICAL)
- CCP-4: IOT-FILL-01 through 05 (fill temperature)
- CCP-5: IOT-FERM-PH-01 through 04 (kombucha pH)
- CCP-6: Vision system camera feed (label verification — not IoT sensor)
- CCP-7: Metal detector output (electronic, logged to AGNT-09)

---

## 2. Temperature Monitoring Requirements

### 2.1 Cold Storage — FDA and HACCP Requirements

| Standard | Requirement | PPB Implementation |
|---|---|---|
| FDA (21 CFR 117) | Maintain refrigerated foods at temperatures that minimize growth of pathogens | ZONE-R: 34–40°F; sensor every 5 min |
| FDA (21 CFR 1.908) | Refrigerated products in transport: ≤ 41°F (5°C) | IOT transit loggers; 15-min intervals |
| USDA (FSIS Guideline) | Frozen storage at ≤ 0°F (-17.8°C) | ZONE-F: -10–0°F; sensor every 5 min |
| SQF Chapter 11 (Beverages) | Temperature monitoring of all cold storage areas | 84 sensors in cold zones; continuous monitoring |
| BRC Chapter 4 | Temperature-controlled storage monitored continuously | Automated AGNT-22 monitoring; records on blockchain |

### 2.2 Processing Temperatures — 21 CFR 120 (Juice HACCP)

21 CFR Part 120 requires juice manufacturers to achieve a 5-log reduction of the most resistant pathogen. For PurePress pasteurized products:

| Product | Pathogen Target | Required 5-Log Reduction | CL Achieved |
|---|---|---|---|
| Orange Juice | Salmonella spp. | 161°F / 15 sec | Yes (CCP-3) |
| Apple Juice/Cider | E. coli O157:H7 | 161°F / 15 sec | Yes (CCP-3) |
| Berry products | Cryptosporidium | 161°F / 15 sec | Yes (CCP-3) |

**Note on Kombucha:** Kombucha is not a juice product and is not pasteurized post-fill. The safety control is the low pH (≤ 3.2) which inhibits pathogen growth. This is a chemical preventive control under FSMA, not a juice HACCP process control.

---

## 3. Humidity Monitoring

### 3.1 Specifications by Zone

| Zone | RH Spec | Alert Threshold | FDA/SQF Basis |
|---|---|---|---|
| ZONE-A (Ambient dry storage) | 45–65% RH | > 70% RH | Prevent moisture uptake in dry ingredients; mold growth risk |
| ZONE-R (Refrigerated) | 75–85% RH | > 90% RH | High RH in cold storage is normal; excess risks condensation/mold |
| ZONE-F (Frozen) | < 50% RH (defrost cycles manage) | N/A | Frozen humidity largely managed by refrigeration system |
| Processing area | 50–70% RH | > 80% RH | Condensation risk on surfaces near product |
| Aseptic fill room (LINE-05) | 40–60% RH | > 65% RH | Clean room integrity; condensation risk |
| Packaging room | 45–65% RH | > 75% RH | Label adhesion; packaging integrity |

### 3.2 High Humidity Consequences

| Scenario | Risk | Response |
|---|---|---|
| Processing area > 80% RH | Condensation on equipment → drip contamination of product | Alert maintenance; check HVAC dehumidification; inspect for drip sources |
| Dry ingredient storage > 70% RH | Clumping, microbial growth in hygroscopic powders (citric acid, xanthan, stevia) | Alert AGNT-04; flag affected lots for quality review; CAPA if recurring |
| Packaging area > 75% RH | Label lifting, seal failure, secondary packaging delamination | Alert operations; evaluate affected finished goods |

---

## 4. Pressure Monitoring

### 4.1 Aseptic Fill Room (LINE-05)

The aseptic fill line operates under positive pressure to prevent environmental contamination of the sterile fill zone.

| Parameter | Spec | Alert |
|---|---|---|
| Fill room positive pressure differential | +0.05–0.15 in H2O vs. adjacent areas | < +0.02 in H2O |
| HEPA filter differential pressure | Per filter specs (typically 0.3–1.0 in H2O) | > 1.5 in H2O (filter loading) |
| Air change rate | ≥ 20 ACH | < 18 ACH |

### 4.2 CIP System Pressure

| Parameter | Spec | Alert |
|---|---|---|
| CIP spray pressure | ≥ 20 PSI at spray header | < 15 PSI |
| CIP circuit pressure (return) | Positive flow confirmed | Any negative pressure (air ingress risk) |

### 4.3 Compressed Air (Food-Grade)

| Parameter | Spec | Standard |
|---|---|---|
| Oil content | ≤ 0.01 mg/m³ | ISO 8573-1 Class 1 |
| Particle content | ≤ 0.1 μm | ISO 8573-1 Class 1 |
| Dew point | ≤ -40°F (-40°C) | ISO 8573-1 Class 2 |
| Microbiological | ≤ 1 CFU/m³ | ISO 8573-7 Class 1 |

---

## 5. Water Quality Monitoring

### 5.1 Processing Water Specifications

All water used in product formulation and equipment rinsing must meet:

| Parameter | Limit | Test Frequency | Basis |
|---|---|---|---|
| Chlorine (free) | ≤ 4.0 mg/L (residual) | Daily | 40 CFR 141 (EPA NPDWR) |
| Total coliform | Zero detected | Weekly | 40 CFR 141 |
| E. coli | Zero detected | Weekly | 40 CFR 141 |
| pH | 6.5–8.5 | Daily | 40 CFR 141 |
| Total dissolved solids | ≤ 500 mg/L | Monthly | 40 CFR 141 |
| Hardness | ≤ 200 mg/L CaCO3 | Monthly | Process quality |

### 5.2 In-Line Water Quality Sensors

| Sensor ID | Location | Measurement |
|---|---|---|
| IOT-WATER-CL-01 | Post-RO / city water blend point | Chlorine residual (mg/L) |
| IOT-WATER-COND-01 | Process water supply | Conductivity (μS/cm) → TDS proxy |
| IOT-WATER-PH-01 | Process water supply | pH |
| IOT-WATER-FLOW-01 | Water metering to blend tanks | Flow (gal/min) |

---

## 6. Data Retention and Reporting

| Record Type | Retention | Format | Location |
|---|---|---|---|
| CCP monitoring records (pasteurizer, fill temp) | 2 years | Time-stamped digital records | Blockchain ledger + local SCADA |
| Cold storage temperature logs | 2 years | Automated IoT logs | Blockchain ledger + AGNT-22 database |
| Transit logger records | 2 years | Cellular upload → PDF report | AGNT-07 storage + blockchain for CTE |
| Calibration records | 2 years | PDF certificates | AGNT-15 document library |
| CIP monitoring records | 2 years | Digital logs | AGNT-09 + blockchain |
| EMP (environmental swab) results | 2 years | Lab reports | AGNT-12 + AGNT-15 document library |
| Water quality records | 2 years | Lab reports + daily logs | QA file + AGNT-12 |

All records are available for FDA inspection within 24 hours (blockchain query provides access in < 4 seconds).

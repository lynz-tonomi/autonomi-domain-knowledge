# Sensor Fleet Reference
**Skill:** iot-monitoring | **Domain:** sensor-fleet | **Version:** 1.0.0

---

## 1. Fleet Overview — PurePress Beverages (PPB)

| Category | Count | Protocol | Data Frequency |
|---|---|---|---|
| Temperature sensors (cold storage) | 84 | MQTT over WiFi | Every 5 min |
| Temperature sensors (production lines) | 62 | OPC-UA / 4–20mA | Every 1 second |
| Temperature sensors (transit/IoT loggers) | 48 | Cellular LTE (ThermaTrack T-Pro 4G) | Every 15 min |
| Humidity sensors | 38 | MQTT over WiFi | Every 10 min |
| pH inline sensors | 16 | Modbus TCP | Every 30 seconds |
| Brix refractometers (inline) | 12 | Modbus TCP | Every 30 seconds |
| Pressure sensors (CIP / aseptic) | 28 | 4–20mA | Every 5 seconds |
| Flow meters | 18 | Pulse output / HART | Every 1 second |
| Level sensors (tanks) | 22 | Ultrasonic / 4–20mA | Every 60 seconds |
| Door sensors (cold storage) | 14 | BLE / Zigbee | Event-driven |
| **Total** | **342** | | |

---

## 2. Temperature Sensors — Cold Storage Zones

### 2.1 ZONE-R (Refrigerated — 120 pallet capacity)

| Sensor ID | Location | Type | Spec Range | Current Reading |
|---|---|---|---|---|
| IOT-R-001 through IOT-R-024 | 24 sensors distributed across ZONE-R | Omega iTemp-200 RTD | 34–40°F | 37.2°F avg |
| IOT-DOOR-R-01 through R-06 | 6 cold room doors | Magnetic contact + temp | — | All closed |

### 2.2 ZONE-F (Frozen — 64 pallet capacity)

| Sensor ID | Location | Type | Spec Range | Current Reading |
|---|---|---|---|---|
| IOT-F-001 through IOT-F-016 | 16 sensors distributed across ZONE-F | Omega iTemp-400 RTD | -10–0°F | -4.8°F avg |
| IOT-DOOR-F-01 through F-04 | 4 blast freezer doors | Magnetic contact + temp | — | All closed |

### 2.3 ZONE-FG-C (Finished Goods Cold)

| Sensor ID | Location | Type | Spec Range |
|---|---|---|---|
| IOT-FG-001 through IOT-FG-032 | 32 sensors in finished goods cold room | Omega iTemp-200 RTD | 34–40°F |
| IOT-DOOR-FG-01 through FG-04 | 4 dock doors | Combined temp + contact | — |

---

## 3. Production Line Temperature Sensors

### 3.1 CCP-3 — Pasteurizer (Critical for HACCP)

| Sensor ID | Location | Type | Critical Limit |
|---|---|---|---|
| IOT-PAST-01 | HTST holding tube entrance | Calibrated RTD (NIST-traceable) | ≥ 161°F |
| IOT-PAST-02 | HTST holding tube exit | Calibrated RTD (NIST-traceable) | ≥ 161°F |
| IOT-PAST-03 | UHT chamber (LINE-05, LINE-07) | Calibrated thermocouple | ≥ 280°F |
| IOT-PAST-04 | Flow diversion valve temp probe | Calibrated RTD | Linked to valve |
| IOT-PAST-BKUP | Backup (redundant, alarm comparison) | RTD | Same as primary |

**Calibration:** Monthly, against NIST-traceable reference thermometer. Records retained 2 years.

### 3.2 CCP-4 — Fill Temperature

| Sensor ID | Location | Application |
|---|---|---|
| IOT-FILL-01 | Hot-fill filler bowl (LINE-01) | Critical limit: ≥ 185°F |
| IOT-FILL-02 | Hot-fill filler bowl (LINE-02) | Critical limit: ≥ 185°F |
| IOT-FILL-03 | Cold-fill surge tank (LINE-03) | Critical limit: ≤ 40°F |
| IOT-FILL-04 | Cold-fill surge tank (LINE-04) | Critical limit: ≤ 40°F |
| IOT-FILL-05 | Aseptic filler (LINE-05) | Sterile zone temp monitoring |

### 3.3 Fermentation Tanks — Kombucha (LINE-06)

| Sensor ID | Location | Parameter | Spec |
|---|---|---|---|
| IOT-FERM-01 through IOT-FERM-08 | 8 fermentation vessels | Temperature | 72–80°F (22–27°C) |
| IOT-FERM-PH-01 through 04 | Inline pH probes in 4 vessels | pH | Monitor 2.8–3.2; alert < 2.8 or > 3.4 |
| IOT-FERM-CO2-01 | CO2 level (headspace) | CO2 % | Monitor: 0.1–0.5% |

---

## 4. CIP System Sensors

| Sensor ID | Measurement | Location | Purpose |
|---|---|---|---|
| IOT-CIP-TEMP-01 through 06 | Temperature | CIP supply return lines | Verify caustic wash ≥ 160°F |
| IOT-CIP-COND-01 through 06 | Conductivity | CIP supply return | Verify detergent concentration |
| IOT-CIP-PRESS-01 through 08 | Pressure | CIP spray headers | Verify spray pressure ≥ 20 PSI |
| IOT-CIP-FLOW-01 through 04 | Flow rate | CIP supply lines | Verify flow velocity ≥ 5 ft/s |

---

## 5. Incoming Dock Sensors (Smart Contract Verification)

These sensors are specifically used to verify smart contract payment conditions on incoming deliveries.

| Sensor ID | Location | Measurement | Contract Role |
|---|---|---|---|
| IOT-DOCK-TEMP-01 | Dock door 1 — refrigerated receiving | Temperature at receipt | Contract condition: temp ≤ 40°F |
| IOT-DOCK-TEMP-02 | Dock door 2 — refrigerated receiving | Temperature at receipt | Contract condition: temp ≤ 40°F |
| IOT-DOCK-TEMP-03 | Dock door 3 — frozen receiving | Temperature at receipt | Contract condition: temp ≤ 10°F |
| IOT-DOCK-SCAN-01 | Dock door 1 — barcode / BOL scanner | BOL number match | Contract condition: delivery confirmed |
| IOT-DOCK-SCALE-01 | Receiving dock floor scale | Weight (lbs) | Contract condition: quantity ≥ 98% of PO |

---

## 6. Transit Temperature Loggers (48 units)

| Model | Coverage | Communication | Battery Life | Calibration |
|---|---|---|---|---|
| ThermaTrack T-Pro 4G | Refrigerated outbound shipments | Cellular LTE | 90 days | Annual NIST-traceable |
| ThermaTrack T-Frozen | Frozen inbound from suppliers | Cellular LTE | 90 days | Annual |
| ThermaTrack T-Express | Same-day local deliveries | BLE to driver tablet | 14 days | Semi-annual |

Each logger has a unique serial number linked to the shipment BOL and blockchain shipping record.

---

## 7. Sensor Health Monitoring

AGNT-22 monitors sensor health continuously:

| Health Status | Criteria | AGNT-22 Action |
|---|---|---|
| Normal | Reading within range; heartbeat received on schedule | No action |
| Warning | Reading approaching threshold; or missed heartbeat < 30 min | Log warning; increase check frequency |
| Alert | Reading outside threshold; or missed heartbeat 30–120 min | Fire alert; notify relevant agent |
| Critical | CCP sensor out of spec; or missed heartbeat > 2 hours | Immediate escalation; LynZ voice notification |
| Calibration Due | > 30 days from last calibration (CCP sensors) | Schedule service; alert operations |

**Current sensor health:**  
- Fully operational: 336 sensors (98.2%)  
- Warning: 4 sensors (2 transit loggers approaching battery replacement; 2 fermentation pH probes drift check due)  
- Offline: 2 sensors (scheduled maintenance)  
- Critical: 0

---

## 8. Calibration Schedule

| Sensor Type | Calibration Frequency | Method | Records |
|---|---|---|---|
| CCP pasteurizer RTDs | Monthly | NIST-traceable reference thermometer | 2-year retention |
| CCP fill temperature sensors | Monthly | NIST-traceable reference thermometer | 2-year retention |
| Cold storage temperature sensors | Quarterly | Digital calibrator | 1-year retention |
| Inline pH probes | Weekly (2-point buffer calibration) | pH 4.0 and 7.0 buffers | Per-use records |
| Inline Brix refractometers | Daily (1-point check with sucrose solution) | 11.5 °Bx reference | Per-use records |
| Transit loggers | Annual | NIST-traceable lab | Certificate retained |
| Dock scales | Annual (NTEP-certified) | Certified weights | Certificate retained |

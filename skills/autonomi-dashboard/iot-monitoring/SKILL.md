---
name: IoT Monitoring
description: Fleet management for 342 IoT sensors, environmental monitoring, alert thresholds, and FDA/HACCP compliance
domain: iot
version: 1.0.0
---

# IoT Monitoring

## Overview
PurePress Beverages operates 342 IoT sensors across its production facility, cold storage, and distribution fleet. The IoT Monitor Agent (AGNT-22) processes all sensor readings in real time, applies threshold logic, and fires alerts to the appropriate response chain. Sensor data is the bedrock of HACCP CCP monitoring, cold chain compliance, and smart contract payment verification. All sensor readings that trigger alerts or CCP violations are written to the blockchain ledger.

## Capabilities
- Real-time monitoring of all 342 sensors across 6 categories
- CCP-linked sensors: pasteurizer, fill line, cold chain — automatic HACCP monitoring
- Smart contract condition verification: IoT dock sensors confirm temperature and quantity for payment release
- Environmental monitoring: cold storage zones, processing areas, fermentation tanks
- Alert chain: sensor → AGNT-22 → relevant agent → LynZ → Weston (voice notification)
- Sensor health monitoring: calibration schedules, battery status, communication dropout detection
- Dashboard IoT page shows all sensors, live readings, alert status, and historical trends

## Reference Files
- `references/sensor_fleet.md` — Complete sensor inventory by type, location, protocol, calibration schedule
- `references/alert_rules.md` — All threshold configurations, severity levels, escalation chains
- `references/environmental_compliance.md` — Temperature, humidity, and pressure monitoring for FDA/HACCP requirements

## Usage
Load this skill when Weston asks about sensor data, temperature readings, IoT alerts, cold chain monitoring, or any question about the 342 sensors. Navigate to `iot` for the IoT Sensors dashboard. CCP-related sensor data may also appear on `qc-inspection` and `compliance`.

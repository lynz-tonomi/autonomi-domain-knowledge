# Logistics Reference
**Skill:** supply-chain-ops | **Domain:** logistics | **Version:** 1.0.0

---

## 1. Overview

Autonomi manages outbound logistics for PurePress Beverages and the broader tenant network. The Logistics Agent (AGNT-07) handles carrier selection, route optimization, cold chain compliance monitoring during transit, OTIF tracking, and dispute management. All shipment events are recorded to the blockchain. For cold chain shipments, IoT-tagged trailers report temperature readings every 15 minutes, and any excursion auto-triggers an alert chain.

---

## 2. Carrier Network

### 2.1 Primary Carriers

| Carrier ID | Carrier Name | Mode | Temp Capability | OTIF Score | Lanes |
|---|---|---|---|---|---|
| CAR-001 | FreshRoute Logistics | TL / LTL | Refrigerated | 97.1% | West Coast, Southwest |
| CAR-002 | ArcticFreight LLC | TL | Refrigerated + Frozen | 95.4% | National |
| CAR-003 | SunState Transport | LTL | Ambient | 93.8% | Southeast, Mid-Atlantic |
| CAR-004 | PacificHaul Inc | TL | Ambient | 94.6% | West Coast |
| CAR-005 | IceBox Carriers | Reefer TL | Refrigerated | 96.8% | National cold chain specialist |

### 2.2 Carrier Selection Logic

AGNT-07 selects the carrier at shipment release using this priority order:
1. Cold chain requirement (temp-capable carriers only for refrigerated / frozen loads)
2. Lane availability and transit time to delivery window
3. OTIF score (prefer ≥ 95%)
4. Spot rate vs. contract rate (minimize cost within service requirements)
5. Existing load tender response time (< 2 hrs preferred)

### 2.3 Carrier Score Thresholds

| OTIF Score | Status | Action |
|---|---|---|
| ≥ 96% | Preferred | First-tender priority |
| 90–95% | Approved | Standard rotation |
| 85–89% | Probationary | Limit to non-critical lanes |
| < 85% | Under Review | Escalate; evaluate replacement |

---

## 3. Distribution Network — Key Lanes

| Origin | Destination | Transit Days | Mode | Temp Req | Primary Carrier |
|---|---|---|---|---|---|
| PPB-WH-01 (Los Angeles) | NorCal DC (Sacramento) | 1 | LTL Reefer | 34–40°F | CAR-001 |
| PPB-WH-01 | Pacific NW DC (Portland) | 2 | TL Reefer | 34–40°F | CAR-001 |
| PPB-WH-01 | SW Regional DC (Phoenix) | 1 | TL Ambient | Ambient | CAR-004 |
| PPB-WH-01 | Mountain DC (Denver) | 2 | TL Ambient | Ambient | CAR-004 |
| PPB-WH-01 | Southeast DC (Atlanta) | 4 | TL Reefer | 34–40°F | CAR-002 |
| PPB-WH-01 | National 3PL (Dallas) | 3 | TL Mixed | Mixed | CAR-002 |
| PPB-WH-01 | Midwest DC (Chicago) | 3 | TL Reefer | 34–40°F | CAR-005 |

---

## 4. Cold Chain Transport Standards

### 4.1 Temperature Requirements by Product

| Product | In-Transit Temp | Max Deviation | Duration Tolerance |
|---|---|---|---|
| NFC juice (all flavors) | 34–40°F | ± 2°F transient | < 2 hrs above 42°F |
| Kombucha 355ml | 34–40°F | ± 2°F transient | < 1 hr above 42°F |
| Oat Milk 1L | 34–40°F | ± 2°F transient | < 2 hrs above 42°F |
| FCOJ (outbound to co-man) | 0–10°F | ± 5°F transient | < 30 min above 15°F |
| Shelf-stable hot-fill | Ambient | < 90°F | Not temp-sensitive |

### 4.2 IoT Trailer Monitoring

Every refrigerated shipment uses a cellular IoT temperature logger:
- **Logger model:** ThermaTrack T-Pro 4G
- **Reporting interval:** Every 15 min (adjustable to 5 min for sensitive loads)
- **Data pushed to:** Autonomi IoT platform → blockchain ledger
- **Alerts:** Temp deviation fires to AGNT-19 → AGNT-07 → LynZ voice notification

### 4.3 Cold Chain Excursion Response

| Scenario | Response |
|---|---|
| Temp above threshold < 30 min | Log event; notify driver to check reefer unit; monitor |
| Temp above threshold 30 min–2 hrs | AGNT-07 contacts carrier ops center; hold product at next DC for QA assessment |
| Temp above threshold > 2 hrs | Shipment quarantined at destination; QA review required; potential rejection |
| Frozen load above -5°F | Auto-escalate to human; customer notified; replacement evaluated |

---

## 5. OTIF Tracking

### 5.1 Definition

**On Time:** Delivery within ±2 hrs of committed delivery window  
**In Full:** ≥ 98% of ordered units delivered (by case count)

**OTIF = (On Time AND In Full deliveries) / Total Deliveries**

### 5.2 Current Performance

| Tenant | OTIF (last 30 days) | Target | Trend |
|---|---|---|---|
| PurePress Beverages | 96.8% | 97.0% | Improving |
| Cascade Drinks | 94.1% | 95.0% | Stable |
| VitaFlow | 97.3% | 95.0% | Exceeding |
| SunRise RTD | 93.6% | 95.0% | At Risk |

### 5.3 OTIF Miss Investigation

When a delivery misses OTIF:
1. AGNT-07 logs root cause category: carrier delay / production late / customer receiving closed / weather
2. If carrier-caused: AGNT-07 flags against carrier OTIF score; generates dispute if applicable
3. If production-caused: escalate to Production Scheduler; evaluate schedule adherence root cause
4. Customer credit evaluated per SLA terms

---

## 6. Route Optimization

### 6.1 LTL Consolidation

AGNT-07 evaluates LTL consolidation daily at 09:00 local time:
- Groups orders by lane and delivery window (same-day departure)
- Calculates cost per hundredweight (CWT) for consolidated vs. individual shipments
- Auto-consolidates if savings > $150 per move and delivery window unchanged
- Escalates to human if consolidation shifts delivery date by > 24 hrs

### 6.2 Backhaul Optimization

For TL lanes, AGNT-07 negotiates backhaul opportunities through the carrier network:
- Identifies empty-return carriers on outbound lanes
- Evaluates inbound raw material pickup on return leg
- Average backhaul savings: 18–24% vs. separate inbound freight

### 6.3 3PL Integration

PurePress uses a national 3PL partner (Dallas DC) for mid-continent distribution:
- 3PL receives orders via EDI 940
- AGNT-07 monitors 3PL fulfillment accuracy against Autonomi order data
- 3PL must acknowledge orders within 2 hrs; ship within 24 hrs of scheduled date
- 3PL performance reviewed monthly; current score: 91.4%

---

## 7. Freight Cost Management

### 7.1 Cost Allocation

Freight costs are allocated to each product in COGS using a weight-based allocation:

Freight Cost / Unit = (Total Shipment Freight Cost) / (Total Shipment Weight lbs) × (Unit Weight lbs)

### 7.2 Benchmark Rates (current)

| Lane | Mode | Rate per CWT | Contract vs. Spot |
|---|---|---|---|
| LA → NorCal (reefer) | LTL | $14.20 | Contract |
| LA → Portland (reefer) | TL | $1.85/mi | Contract |
| LA → Phoenix (ambient) | TL | $1.42/mi | Contract |
| LA → Chicago (reefer) | TL | $2.10/mi | Spot avg |
| LA → Atlanta (reefer) | TL | $2.35/mi | Contract |

### 7.3 Freight Accrual

AGNT-07 accrues freight costs at shipment tender, reconciles to carrier invoice within 5 business days of delivery. Discrepancies > 3% escalate to finance review.

---

## 8. Logistics KPIs

| KPI | Target | Current |
|---|---|---|
| Network OTIF | ≥ 96% | 95.5% |
| Cold Chain Compliance (in-transit) | 100% | 99.2% |
| Carrier OTIF (carrier-caused misses only) | < 3% | 2.8% |
| LTL Consolidation Rate | ≥ 35% of eligible loads | 41.2% |
| Freight Cost vs. Budget | ≤ ±5% | +0.9% |
| Dispute Resolution Time | ≤ 10 business days | 7.4 days avg |
| CO2 per ton-mile (fleet average) | Improve 5% YoY | On track |

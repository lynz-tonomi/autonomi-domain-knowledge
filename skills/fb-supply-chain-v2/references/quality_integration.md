# Quality Integration Touchpoints — Deep Reference

## 8.1 Incoming Inspection

```
INCOMING INSPECTION DECISION:

FOR EACH received lot:
  1. Verify COA received and all parameters within spec
  2. Visual inspection:
     - Packaging intact, no leaks, no tears
     - No pest evidence (droppings, gnaw marks, live insects)
     - Correct product / correct quantity vs PO
     - Code dates legible and within expected range
  3. Temperature check (if temp-sensitive):
     - Refrigerated: ≤40°F at receipt
     - Frozen: ≤0°F at receipt, no evidence of thaw
     - FLAG if out of range → HOLD lot, quality assessment
  4. Sample pull for lab (if required by quality plan):
     Micro:
       APC (aerobic plate count): ≤10,000 CFU/g (typical for concentrates)
       Yeast & mold: ≤100 CFU/g
       Coliforms: <10 CFU/g
       Pathogens: negative for Salmonella (25g), Listeria (25g), E. coli O157:H7 (25g)
     Chemistry:
       Brix, pH, titratable acidity, color, moisture — per ingredient spec
     Sensory:
       Flavor, odor, appearance vs reference standard
  5. IF all pass: release lot (hold_status = 'available')
  6. IF any fail: hold lot (hold_status = 'qa_hold'), notify quality

SKIP LOT PROGRAM (reduced inspection):
  Eligibility: supplier GFSI cert + 10 consecutive lots pass + scorecard > 90
  Reduced: inspect 1 in 3 lots (visual + COA only, skip lab)
  Revert to full inspection after ANY failure
```

## 8.2 In-Process Checks

### Check Frequency by Parameter

| Parameter | Frequency | Sample Size | Method |
|-----------|-----------|-------------|--------|
| Brix | Every 30 min during filling | 1 sample from filler | Digital refractometer |
| pH | Every 30 min during filling | 1 sample | pH meter (calibrated daily) |
| Fill weight | Every 15 min | 5 units per check | Checkweigher or scale |
| Cap torque | Every 30 min | 5 units per check | Torque meter |
| Headspace | Every 30 min | 3 units per check | Headspace gauge (critical for retort) |
| Metal detection | Continuous | Every unit | In-line metal detector |
| Visual inspection | Continuous | Every unit | Operator + camera (if available) |
| CO2 volumes | Every 30 min | 1 sample | Zahm & Nagel or equivalent |
| Dissolved O2 | Every hour | 1 sample | Orbisphere or equivalent |
| Temperature (fill) | Continuous | In-line sensor | Thermocouple at filler |
| Code date verification | Start of each run + every hour | 3 units | Visual check |
| Label verification | Start of each run | 3 units | Visual + barcode scan |
| Seal integrity | Every 30 min | 3 units | Dye test or vacuum check |

### Statistical Process Control (SPC) for Fill Weight

```
SPC RULES (Western Electric / Nelson rules):
  STOP LINE if any of:
    - 1 point beyond 3σ (action limits)
    - 2 of 3 consecutive points beyond 2σ (same side)
    - 4 of 5 consecutive points beyond 1σ (same side)
    - 8 consecutive points on same side of center line
    - 6 consecutive points trending in same direction

FILL WEIGHT CONTROL LIMITS:
  Target = declared fill weight + target overfill (typically +1–2%)
  UCL (upper control limit) = target + 3σ
  LCL (lower control limit) = declared fill weight (legal minimum)
  → Underfill below declared weight = NIST Handbook 133 violation
```

### Process Deviation Handling

```
IF any in-process check out of spec:
  1. HOLD all product since last passing check
  2. Adjust process parameter (filler speed, valve, temperature, etc.)
  3. Recheck — 3 consecutive passing results required to resume production
  4. Evaluate held product:
     - IF reworkable → see Batch Management rework decision tree
     - IF not reworkable → reject and dispose
  5. Log deviation with:
     - Parameter affected
     - Magnitude of deviation
     - Duration (how many units potentially affected)
     - Root cause
     - Corrective action taken
     - Preventive action to avoid recurrence
```

## 8.3 Hold / Release System

### Hold Types

| Hold Type | Trigger | Authority to Release |
|-----------|---------|---------------------|
| `QA_HOLD` | Quality parameter out of spec | Quality Manager or designee |
| `MICRO_HOLD` | Waiting for micro results (24–72 hrs) | Quality Manager after lab confirm pass |
| `SUPPLIER_HOLD` | COA missing or non-conforming ingredient | Quality + Procurement jointly |
| `REGULATORY_HOLD` | Labeling issue, allergen concern, regulatory inquiry | Quality + Regulatory jointly |
| `RECALL_HOLD` | Product linked to recall event | Quality VP + Legal (elevated authority) |
| `CUSTOMER_HOLD` | Customer complaint under investigation | Quality Manager |

### Hold Procedure

```
HOLD INITIATION:
  1. Change hold_status in inventory system
  2. Physically segregate product (move to hold area or apply hold tag)
  3. Notify: quality team, warehouse, customer service (if shipped product affected)
  4. Document: batch_id, quantity held, reason, date, initiated by

HOLD DISPOSITION (after investigation):
  RELEASE: all parameters confirmed within spec → change status to 'available'
  REWORK: can be corrected → route to rework (see Batch Management)
  REJECT: cannot be corrected → dispose or return to supplier
  USE-AS-IS: parameter out of spec but functional impact acceptable → requires
    documented risk assessment + quality manager + operations manager approval

HOLD AGING:
  FLAG if hold > 7 days without disposition decision
  FLAG if hold > 14 days → escalate to quality director
  → Extended holds consume shelf life and warehouse space
```

## 8.4 Specification Management

### Spec Types

| Spec Type | Covers | Owner |
|-----------|--------|-------|
| Raw material spec | Incoming ingredient requirements | Quality + R&D |
| In-process spec | Parameters during production | Quality + Operations |
| Finished product spec | Final product release criteria | Quality + R&D |
| Packaging spec | Packaging material requirements | Quality + Packaging Engineering |
| Customer spec | Customer-specific requirements (beyond standard) | Quality + Sales |

### Spec Change Management

```
IF spec change requested:
  1. Document reason for change (cost, quality, regulatory, customer)
  2. Assess impact:
     - Does it affect food safety? → requires HACCP team review
     - Does it affect label claims? → requires regulatory review
     - Does it affect customer specs? → requires customer notification/approval
     - Does it affect shelf life? → requires new shelf life study
  3. Approve via change control (quality + R&D + operations sign-off)
  4. Update all documents: specs, SOPs, batch records, labels
  5. Effective date: align with next production run or label print
  6. Communicate to: production, QC, procurement, warehouse, co-packers
```

## 8.5 Failure Modes

| Failure | Detection | Action |
|---------|-----------|--------|
| Incoming lot fails COA review | COA parameter out of spec | Hold lot, supplier NCR, assess reject/return |
| In-process check fails 3+ consecutive | SPC trending | Stop line, hold product, adjust process, root cause |
| Micro hold exceeds 72 hrs without result | Hold aging report | Escalate to lab, assess re-test or release risk |
| Customer complaint — illness | Customer service intake | Hold all related product, investigate, notify regulatory if needed |
| Customer complaint — foreign material | Customer service intake | Identify source, inspect production line, hold related batches |
| Metal detector rejects > 3 in 1 hour | Metal detector log | Stop line, inspect equipment upstream for wear/damage |
| Label mismatch (wrong label on product) | Visual check or customer report | STOP, hold all product since last verified correct label, assess recall |

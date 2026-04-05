# Google Sheets Integration Reference — Autonomi Agents

## Table of Contents
1. [Read Operations](#read-operations)
2. [Write & Append](#write--append)
3. [Batch Operations](#batch-operations)
4. [Template Sheets for Tenants](#template-sheets-for-tenants)
5. [Sync Patterns](#sync-patterns)
6. [Formula Patterns for F&B](#formula-patterns-for-fb)

## Read Operations

### Read Range
```bash
gws sheets spreadsheets values get \
  --params '{"spreadsheetId": "SHEET_ID", "range": "Inventory!A1:H100"}'
```

### Read Multiple Ranges (batch read)
```bash
gws sheets spreadsheets values batchGet \
  --params '{"spreadsheetId": "SHEET_ID", "ranges": ["Inventory!A:H", "Suppliers!A:G", "QC-Log!A:J"]}'
```

### Read with Value Render Options
```bash
# Get formatted values (dates as strings, currency formatted)
gws sheets spreadsheets values get \
  --params '{"spreadsheetId": "SHEET_ID", "range": "A1:H100", "valueRenderOption": "FORMATTED_VALUE"}'

# Get raw values (dates as serial numbers, no formatting)
gws sheets spreadsheets values get \
  --params '{"spreadsheetId": "SHEET_ID", "range": "A1:H100", "valueRenderOption": "UNFORMATTED_VALUE"}'
```

## Write & Append

### Append Row (add new record)
```bash
# Append to next empty row
gws sheets +append --spreadsheet SHEET_ID \
  --values "2026-03-20,Mango Puree,Lot-2847,1200,lbs,Received,QC-Pending,Supplier-A"
```

### Update Specific Cell Range
```bash
gws sheets spreadsheets values update \
  --params '{"spreadsheetId": "SHEET_ID", "range": "Inventory!F2", "valueInputOption": "USER_ENTERED"}' \
  --json '{"values": [["QC-Passed"]]}'
```

### Clear Range (before full refresh)
```bash
gws sheets spreadsheets values clear \
  --params '{"spreadsheetId": "SHEET_ID", "range": "Inventory!A2:H1000"}'
```

## Batch Operations

### Batch Update (full sync)
```bash
gws sheets spreadsheets values batchUpdate \
  --params '{"spreadsheetId": "SHEET_ID"}' \
  --json '{
    "valueInputOption": "USER_ENTERED",
    "data": [
      {"range": "Inventory!A2:H50", "values": [["2026-03-20", "Mango Puree", ...]]},
      {"range": "Summary!B2", "values": [["=COUNTA(Inventory!A2:A)"]]}
    ]
  }'
```

### Create New Spreadsheet
```bash
gws sheets spreadsheets create --json '{
  "properties": {"title": "Autonomi - Weekly Production Report - W12"},
  "sheets": [
    {"properties": {"title": "Production"}},
    {"properties": {"title": "Quality"}},
    {"properties": {"title": "Inventory"}},
    {"properties": {"title": "Agent Decisions"}}
  ]
}'
```

## Template Sheets for Tenants

### Inventory Dashboard Template
| Column | Header | Data Type | Source |
|--------|--------|-----------|--------|
| A | Date | Date | Autonomi timestamp |
| B | Ingredient | Text | ingredients.name |
| C | Lot Number | Text | batches.lot_number |
| D | Quantity | Number | Current stock |
| E | Unit | Text | ingredients.unit |
| F | Status | Text | Received/QC-Pending/QC-Passed/Hold/Depleted |
| G | Expiry Date | Date | lot_tracking.expiry |
| H | Supplier | Text | suppliers.name |

### Production Schedule Template
| Column | Header | Data Type | Source |
|--------|--------|-----------|--------|
| A | Date | Date | Schedule date |
| B | Product | Text | bom_recipes.name |
| C | Batch Size | Number | Gallons |
| D | Line | Text | Production line |
| E | Start Time | Time | Scheduled start |
| F | Status | Text | Scheduled/Running/Complete/Delayed |

### QC Log Template
| Column | Header | Data Type | Source |
|--------|--------|-----------|--------|
| A | Date | Date | quality_records.timestamp |
| B | Lot Number | Text | batches.lot_number |
| C | Product | Text | bom_recipes.name |
| D | Test Type | Text | pH/Brix/Micro/Sensory/etc. |
| E | Result | Number | Measured value |
| F | Spec Min | Number | Lower bound |
| G | Spec Max | Number | Upper bound |
| H | Pass/Fail | Text | quality_records.pass_fail |
| I | Tested By | Text | Operator or Agent ID |
| J | Notes | Text | Additional context |

### Agent Decision Log Template
| Column | Header | Data Type | Source |
|--------|--------|-----------|--------|
| A | Timestamp | DateTime | agent_decisions.timestamp |
| B | Agent | Text | Agent name |
| C | Decision Type | Text | reorder/hold/alert/schedule/payment |
| D | Description | Text | Human-readable summary |
| E | Confidence | Percent | agent_decisions.confidence |
| F | Inputs | Text | Key input data points |
| G | Action Taken | Text | What the agent did |
| H | BILL.com Ref | Text | bill_invoices.bill_invoice_id (if payment-related) |
| I | Audit Hash | Text | Blockchain anchor hash |

## Sync Patterns

### One-Way Push (Autonomi → Sheets)
Best for: inventory levels, QC results, agent decisions, production status.
```python
# scripts/sync_inventory_to_sheets.py pattern
1. Query Autonomi DB for current inventory state
2. Format as 2D array matching sheet template
3. Clear existing data range (A2:H1000)
4. Batch write new data
5. Update "Last Synced" cell with timestamp
```

### Bi-Directional Sync (Autonomi ↔ Sheets)
Best for: production schedules (ops team edits in Sheets, agents update status).
```python
# Pattern:
1. Read current Sheets data
2. Read current Autonomi DB state
3. Diff: find rows changed in Sheets vs. rows changed in Autonomi
4. Resolve conflicts (Sheets wins for human edits, Autonomi wins for agent updates)
5. Write merged state to both Sheets and DB
6. Log sync event with conflict resolution details
```

### Event-Driven Push
Best for: real-time alerts, quality holds, payment status changes.
```python
# Triggered by webhook (BILL.com payment.completed, agent decision, etc.)
1. Receive event
2. Format single row
3. Append to appropriate sheet
4. No full sync needed — just incremental append
```

## Formula Patterns for F&B

Useful formulas for tenant sheets that complement Autonomi data:

```
# Days until expiry
=DATEDIF(TODAY(), G2, "D")

# Inventory value
=D2 * VLOOKUP(B2, 'BOM-Costs'!A:C, 3, FALSE)

# QC pass rate (last 30 days)
=COUNTIFS(A:A, ">="&TODAY()-30, H:H, "Pass") / COUNTIFS(A:A, ">="&TODAY()-30, H:H, "<>")

# Supplier on-time delivery rate
=COUNTIFS(Supplier, B2, Status, "On-Time") / COUNTIF(Supplier, B2)

# Batch yield percentage
=Actual_Output / Theoretical_Output * 100
```

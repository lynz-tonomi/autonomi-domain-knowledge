# Excel Online Reference — Autonomi Agents

## Table of Contents
1. [Read Operations](#read-operations)
2. [Write & Append](#write--append)
3. [Table Operations](#table-operations)
4. [Batch Operations](#batch-operations)
5. [Template Workbooks for Tenants](#template-workbooks-for-tenants)
6. [Formula Patterns for F&B](#formula-patterns-for-fb)

## Read Operations

All Excel operations go through the Graph API against workbooks stored in SharePoint/OneDrive.

### Read a range

```python
def read_range(drive_id, workbook_path, sheet_name, range_addr, headers):
    """Read a cell range from an Excel workbook on SharePoint."""
    url = (
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/"
        f"root:{workbook_path}:/workbook/worksheets/{sheet_name}/"
        f"range(address='{range_addr}')"
    )
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["values"]
```

### Read used range (all data in sheet)

```python
def read_all_data(drive_id, workbook_path, sheet_name, headers):
    """Read all data from a worksheet."""
    url = (
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/"
        f"root:{workbook_path}:/workbook/worksheets/{sheet_name}/usedRange"
    )
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return {"values": data["values"], "address": data["address"]}
```

### Read multiple ranges

```python
# Use a session for multiple reads to avoid recalculation overhead
session = requests.post(
    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/"
    f"root:{workbook_path}:/workbook/createSession",
    headers=headers,
    json={"persistChanges": False}
).json()

session_headers = {**headers, "workbook-session-id": session["id"]}
# Now make multiple read calls using session_headers
# Close session when done
requests.post(
    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/"
    f"root:{workbook_path}:/workbook/closeSession",
    headers=session_headers
)
```

## Write & Append

### Update a specific range

```python
def write_range(drive_id, workbook_path, sheet_name, range_addr, values, headers):
    """Write values to a specific range."""
    url = (
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/"
        f"root:{workbook_path}:/workbook/worksheets/{sheet_name}/"
        f"range(address='{range_addr}')"
    )
    resp = requests.patch(url, headers=headers, json={"values": values})
    resp.raise_for_status()
```

### Update single cell

```python
write_range(drive_id, workbook_path, "Inventory", "F2", [["QC-Passed"]], headers)
```

## Table Operations

Excel tables are the best way to manage structured data — they auto-expand and support named columns.

### Add row to table

```python
def append_table_row(drive_id, workbook_path, table_name, values, headers):
    """Append a row to a named Excel table."""
    url = (
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/"
        f"root:{workbook_path}:/workbook/tables/{table_name}/rows/add"
    )
    resp = requests.post(url, headers=headers, json={"values": [values]})
    resp.raise_for_status()
    return resp.json()
```

### Read table data

```python
def read_table(drive_id, workbook_path, table_name, headers):
    """Read all rows from a named Excel table."""
    url = (
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/"
        f"root:{workbook_path}:/workbook/tables/{table_name}/rows"
    )
    rows = get_all_pages(url, headers)
    # Also get column names
    cols = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/"
        f"root:{workbook_path}:/workbook/tables/{table_name}/columns",
        headers=headers
    ).json()["value"]
    column_names = [c["name"] for c in cols]
    return column_names, [r["values"][0] for r in rows]
```

### List tables in a workbook

```python
tables = requests.get(
    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/"
    f"root:{workbook_path}:/workbook/tables",
    headers=headers
).json()["value"]
```

## Batch Operations

For syncing large datasets, use workbook sessions to batch writes:

```python
def batch_update(drive_id, workbook_path, sheet_name, start_row, data, headers):
    """Batch write many rows efficiently using a session."""
    # Create session
    session = requests.post(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/"
        f"root:{workbook_path}:/workbook/createSession",
        headers=headers,
        json={"persistChanges": True}
    ).json()
    sh = {**headers, "workbook-session-id": session["id"]}

    # Write in chunks of 500 rows
    chunk_size = 500
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        end_row = start_row + len(chunk) - 1
        num_cols = len(chunk[0])
        col_letter = chr(64 + num_cols)  # A=1, B=2, etc.
        range_addr = f"A{start_row}:{col_letter}{end_row}"
        write_range(drive_id, workbook_path, sheet_name, range_addr, chunk, sh)
        start_row = end_row + 1

    # Close session
    requests.post(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/"
        f"root:{workbook_path}:/workbook/closeSession",
        headers=sh
    )
```

## Template Workbooks for Tenants

### Inventory Tracker

| Column | Type | Description |
|--------|------|-------------|
| Date | Date | Transaction date |
| Product | Text | Product name |
| Lot Number | Text | Batch/lot identifier |
| Quantity | Number | Amount on hand |
| Unit | Text | UOM (lbs, gal, ea) |
| Status | Text | Received, QC-Pending, QC-Passed, QC-Hold, Released |
| Location | Text | Warehouse location |
| Supplier | Text | Supplier name |

### QC Log

| Column | Type | Description |
|--------|------|-------------|
| Date | Date | Test date |
| Lot Number | Text | Batch/lot identifier |
| Product | Text | Product name |
| Test | Text | Test name (pH, Brix, micro, etc.) |
| Result | Number | Measured value |
| Spec Min | Number | Minimum acceptable |
| Spec Max | Number | Maximum acceptable |
| Pass/Fail | Text | Calculated |
| Technician | Text | Who performed the test |
| Notes | Text | Additional observations |

### Agent Decision Log

| Column | Type | Description |
|--------|------|-------------|
| Timestamp | DateTime | When decision was made |
| Agent | Text | Which agent |
| Decision Type | Text | reorder, hold, release, alert, schedule |
| Subject | Text | What was decided on |
| Action Taken | Text | What happened |
| Confidence | Number | Agent confidence score |
| Overridden | Boolean | Was it overridden by human? |
| Override Reason | Text | Why it was overridden |
| Decision ID | Text | Autonomi internal ID |

## Formula Patterns for F&B

Useful formulas for tenant workbooks:

```
# Days of supply remaining
=[@[Current Stock]]/AVERAGEIFS(Usage!D:D, Usage!B:B, [@Product], Usage!A:A, ">="&TODAY()-30)

# Yield percentage
=[@[Output Quantity]]/[@[Input Quantity]]*100

# Cost per unit with yield adjustment
=[@[Ingredient Cost]]/([@[Yield %]]/100)

# Shelf life remaining (days)
=[@[Expiration Date]]-TODAY()

# Auto-flag low stock (conditional)
=IF([@[Days of Supply]]<[@[Reorder Point Days]], "REORDER", "OK")

# Supplier on-time delivery rate
=COUNTIFS(Deliveries!C:C, [@Supplier], Deliveries!F:F, "On-Time")/COUNTIF(Deliveries!C:C, [@Supplier])
```

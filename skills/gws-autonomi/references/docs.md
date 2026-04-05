# Google Docs Integration Reference — Autonomi Agents

## Table of Contents
1. [Create Documents](#create-documents)
2. [Write Content](#write-content)
3. [Read Documents](#read-documents)
4. [Document Templates](#document-templates)

## Create Documents

```bash
# Create empty doc
gws docs documents create --json '{"title": "QC Hold Notice - Lot 2847"}'

# Create from template (copy template doc, then populate)
gws drive files copy --params '{"fileId": "TEMPLATE_DOC_ID"}' \
  --json '{"name": "Batch Report - Lot 2847", "parents": ["FOLDER_ID"]}'
```

## Write Content

```bash
# Write text to document
gws docs +write --document DOC_ID --text "Content to insert"

# For structured content, use batch update with insertText requests
gws docs documents batchUpdate --params '{"documentId": "DOC_ID"}' --json '{
  "requests": [
    {"insertText": {"location": {"index": 1}, "text": "# Batch Report\n\nProduct: Mango Puree 500ml\n"}}
  ]
}'
```

## Read Documents

```bash
# Get full document content
gws docs documents get --params '{"documentId": "DOC_ID"}'

# Parse for agent processing — extract text from structural elements
```

## Document Templates

### Batch QC Report (Quality Agent)
```markdown
# Batch Quality Report

**Batch:** {lot_number}
**Product:** {product_name}
**Production Date:** {production_date}
**Report Generated:** {timestamp} by Quality Agent

## Test Results Summary

| Test | Result | Spec Range | Status |
|------|--------|-----------|--------|
| pH | {ph_value} | {ph_min}-{ph_max} | {pass_fail} |
| Brix | {brix_value} | {brix_min}-{brix_max} | {pass_fail} |
| Micro (TPC) | {tpc_value} CFU/mL | <{tpc_max} | {pass_fail} |
| Sensory | {sensory_score}/10 | ≥{sensory_min} | {pass_fail} |

## Ingredient Lot Traceability

| Ingredient | Lot # | Supplier | COA |
|-----------|-------|----------|-----|
| {ingredient_name} | {ingredient_lot} | {supplier_name} | {coa_link} |

## Disposition

**Decision:** {disposition} (Release / Hold / Reject)
**Decided By:** {agent_or_human}
**Rationale:** {reasoning}
```

### FSMA 204 Trace Report (Recall Agent)
```markdown
# FSMA 204 Traceability Report

**Report Type:** {trace_forward | trace_back}
**Initiated:** {timestamp}
**Response Time:** {duration} (requirement: <24 hours)

## Subject Lot

**Product:** {product_name}
**Lot:** {lot_number}
**Production Date:** {date}
**Facility:** {facility_name}

## Critical Tracking Events (CTEs)

### Growing/Harvesting
- Source: {farm_name}
- Location: {gps_coordinates}
- Harvest Date: {date}

### Receiving
- Received At: {facility}
- Date: {date}
- Lot Assigned: {lot_number}
- Supplier Lot: {supplier_lot}

### Transforming
- Process: {process_type}
- Date: {date}
- Input Lots: {input_lots}
- Output Lot: {output_lot}

### Shipping
- Shipped To: {destination}
- Date: {date}
- Carrier: {carrier}
- BOL: {bol_number}

## Distribution Chain

{trace_forward_or_back_results}

## Affected Volume

- Total Units: {unit_count}
- Total Weight: {weight} {unit}
- Customers Affected: {customer_count}
```

### Supplier Performance Summary (Procurement Agent)
```markdown
# Supplier Performance Report — {quarter}

**Supplier:** {supplier_name}
**Evaluated By:** Procurement Agent
**Period:** {start_date} to {end_date}

## Scorecard

| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| On-Time Delivery | {otd}% | ≥95% | {status} |
| Quality (COA pass rate) | {quality}% | ≥98% | {status} |
| Price Competitiveness | {price_index} | ≤1.05 | {status} |
| Responsiveness | {response_days} days | ≤2 days | {status} |
| FSMA Compliance | {compliant} | Required | {status} |

## Overall Rating: {rating}/5

## Recommendations
{agent_recommendations}
```

---
name: fb-supply-chain-v2
description: >
  F&B Production & Supply Chain Agent v2 — deep-domain reference for beverage manufacturing (juice, kombucha, oat milk, functional drinks, cold brew). Covers production scheduling, batch management, BOM/formulation, inventory (FEFO, safety stock), procurement, logistics, demand planning, quality, regulatory (FSMA 204), and cost management with numeric thresholds, decision rules, and formulas.
  ALWAYS trigger on: food/beverage production, brewery, dairy, bakery, CPG, ingredient, recipe, formulation, BOM, batch, lot tracking, shelf life, cold chain, FEFO, allergen, procurement, supplier, vendor, PO, inventory, warehouse, logistics, 3PL, co-packer, production schedule, yield, waste, Brix, pH, HACCP, FSMA, SQF, BRC, GMP, FDA, retort, aseptic, hot-fill, cold brew, kombucha, oat milk, OEE, changeover, CIP, COGS, landed cost, trade spend, OTIF, demand forecast, S&OP, MAPE, batch release, rework, or data with columns like batch_id, lot_number, shelf_life_days, brix, ph, yield_pct, cogs.
---

# F&B Production & Supply Chain — Agent Reference v2

This is a system-level reference document. Load the relevant reference file(s) from `references/` based on the operational domain the user is asking about.

## Reference File Index

Each reference file is a self-contained deep-domain document with data schemas, decision rules, numeric thresholds, formulas, and failure modes. Read the file(s) matching the user's query before responding.

| Domain | File | When to Load |
|--------|------|-------------|
| Production scheduling, run sequencing, changeovers, campaign runs, retort/aseptic/cold-brew scheduling | `references/production_scheduling.md` | User asks about schedules, sequencing, changeovers, line utilization, campaign optimization, OEE |
| Batch management, yield, rework, batch release | `references/batch_management.md` | User asks about batches, yield, rework, hold/release, batch records, deviations |
| BOM, formulation, density, scaling, substitutions | `references/bom_formulation.md` | User asks about recipes, BOMs, ingredient costs, scaling, Brix blending, allergen matrix |
| Inventory, FEFO, safety stock, shelf life, cycle counting | `references/inventory_management.md` | User asks about inventory levels, expiring stock, reorder points, lot tracking, warehouse |
| Procurement, POs, lead times, supplier qualification, COAs | `references/procurement.md` | User asks about purchasing, suppliers, POs, lead times, COAs, supplier scorecards |
| Logistics, cold chain, OTIF, freight, warehousing, 3PL | `references/logistics_warehousing.md` | User asks about shipping, freight, cold chain, OTIF, warehouse slotting, 3PL |
| Demand planning, forecasting, S&OP, seasonality, promos | `references/demand_planning.md` | User asks about forecasts, demand, S&OP, seasonality, promotions, MAPE |
| Quality integration, inspection, in-process checks, holds | `references/quality_integration.md` | User asks about QA/QC, incoming inspection, in-process checks, hold/release, deviations |
| Regulatory, FSMA 204, traceability, FDA registration | `references/regulatory.md` | User asks about traceability, FSMA, FDA, recalls, CTEs, KDEs, process filing |
| Cost management, COGS, yield loss costing, landed cost, trade spend | `references/cost_management.md` | User asks about costs, margins, COGS, freight allocation, trade spend, deductions |
| Appendices: beverage specs, unit conversions, alerting thresholds | `references/appendices.md` | Load alongside any other reference when agent needs specs, conversions, or alert thresholds |

## How to Use This Skill

1. **Identify the domain(s).** Read the user's question and determine which reference file(s) to load. Most questions touch 1-2 domains. Cross-domain questions (e.g., "will this ingredient arrive in time for the production run?") need both procurement and production scheduling references.

2. **Load the reference(s).** Use the Read tool on the appropriate file(s) in `references/`.

3. **Apply the data schemas.** The reference files define the exact field names, types, units, and ranges the agent should expect in operational data. Use these to validate and interpret user-provided data.

4. **Apply the decision rules.** Each reference contains explicit IF/THEN logic with numeric thresholds. Use these rules to generate recommendations, flag problems, and make operational decisions.

5. **Surface cross-domain connections.** The most valuable insights come from connecting domains:
   - Procurement + Production: Will ingredients arrive before the scheduled run?
   - Inventory + Demand: Does days-of-supply cover the forecast horizon?
   - Batch + Quality: Does the batch meet all release criteria?
   - Cost + Yield: What is the dollar impact of yield loss?
   - Logistics + Inventory: Is cold chain capacity sufficient for projected inventory?

## Scripts

The `scripts/` directory contains Python utilities for data analysis:

- **`scripts/fb_analyzer.py`** — Data loading, cleaning, KPI calculations, and chart generation
- **`scripts/forecast_engine.py`** — Demand forecasting with seasonality and promo lift
- **`scripts/recipe_calculator.py`** — BOM explosion, scaling, costing, nutritional calculations
- **`scripts/shelf_life_tracker.py`** — Shelf-life analysis, FEFO compliance, waste forecasting

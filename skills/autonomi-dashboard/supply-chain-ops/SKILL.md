---
name: Supply Chain Operations
description: Production scheduling, inventory management, procurement, and logistics for F&B manufacturing
domain: supply-chain
version: 1.0.0
---

# Supply Chain Operations

## Overview
The Supply Chain Operations skill covers all physical flow of materials through the Autonomi platform — from raw ingredient procurement through production scheduling, inventory control, and outbound logistics. It is grounded in the operational reality of beverage manufacturing, including juice, kombucha, oat milk, and functional RTD products. Autonomous agents handle the majority of routine decisions; human oversight is required only for exceptions above configured thresholds.

## Capabilities
- Line scheduling and batch sequencing across 842 production lines
- Campaign run optimization and allergen changeover sequencing
- FEFO (First Expired, First Out) inventory rotation enforcement
- Safety stock and reorder point calculation with dynamic lead time adjustment
- Supplier purchase order automation with approval thresholds
- Cold chain logistics monitoring and carrier management
- OTIF (On Time In Full) tracking and corrective escalation
- Cross-domain insight: procurement lead time vs. scheduled run start date
- 8 active BOM recipes with live costing and stock health indicators

## Reference Files
- `references/production_scheduling.md` — Line scheduling, batch sequencing, capacity planning, OEE, changeover protocols
- `references/inventory_management.md` — FEFO, safety stock, reorder points, cold chain storage, lot tracking
- `references/procurement.md` — Supplier scoring, PO automation, COA management, vendor qualification
- `references/logistics.md` — Route optimization, carrier management, cold chain transport, OTIF

## Usage
Load this skill for any question about production runs, ingredient availability, inventory levels, reorder triggers, supplier performance, shipping, cold chain, or COGS. Most supply chain questions touch 1–2 reference files; cross-domain questions (e.g., "will we have enough concentrate for next week's run?") require loading procurement + inventory + production scheduling together.

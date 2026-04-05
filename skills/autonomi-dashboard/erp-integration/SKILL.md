---
name: ERP Integration
description: Bidirectional sync with SAP, NetSuite, and QuickBooks Online — field mapping, entity models, conflict resolution
domain: integrations
version: 1.0.0
---

# ERP Integration

## Overview
Autonomi sits between existing ERP systems and connects them into a unified data layer. It does not replace SAP, NetSuite, or QBO — it enhances them by adding agentic intelligence, real-time visibility, and blockchain-verified records. The ERP Sync Agent (AGNT-24) handles bidirectional data synchronization. When Autonomi creates a production order, it pushes to the ERP. When the ERP has a new customer order, AGNT-24 pulls it into Autonomi's planning system.

## Capabilities
- Bidirectional sync: production orders, purchase orders, inventory, invoices, payments
- Conflict resolution: deterministic rules for handling simultaneous edits in both systems
- Field mapping: Autonomi entities mapped to SAP MM/PP/QM, NetSuite Manufacturing, and QBO
- Support for SAP S/4HANA (REST OData), NetSuite (SuiteScript REST), QBO (Intuit API v3)
- ERP page on dashboard shows sync status, last sync timestamp, error queue
- Data Pipeline Agent (AGNT-25) handles transformation and routing between formats

## Reference Files
- `references/erp_sync.md` — Sync patterns, frequency, conflict resolution rules, error handling
- `references/data_models.md` — Entity mapping between Autonomi and SAP/NetSuite/QBO field-by-field

## Usage
Load this skill when Weston asks about ERP connectivity, data sync, field mapping, why something isn't showing in SAP/NetSuite/QBO, or how Autonomi connects to legacy systems. Navigate to `erp` for the ERP Integrations dashboard.

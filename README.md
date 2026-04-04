# Autonomi Domain Knowledge

Deep industry knowledge base for **LynZ**, the Autonomi dashboard AI operations agent. This repository contains expert-level reference material across food & beverage science, regulatory compliance, supply chain operations, product development, and financial/productivity platform integrations.

## Purpose

LynZ fetches these reference files at runtime via the OpenAI Realtime API `fetch_reference` tool, keeping her system prompt lean (~1,400 tokens) while having access to deep domain expertise on demand.

## Skills

| Skill | Domain | References |
|-------|--------|------------|
| **fb-product-formulation** | Beverage formulation science | formulation_science, ingredient_interactions, shelf_life_engineering, flavor_systems |
| **fb-food-safety-compliance** | Food safety & regulatory | haccp_advanced, fsma_regulatory, allergen_management, audit_certification |
| **fb-supply-chain-v2** | F&B supply chain ops | commodity_procurement, cold_chain_logistics, demand_planning, supplier_qualification |
| **fb-product-dev** | Product development & NPD | npd_stage_gate, sensory_evaluation, scale_up_manufacturing, labeling_claims |
| **qbo-autonomi** | QuickBooks Online | fb_chart_of_accounts, cogs_batch_costing, qbo_api_patterns |
| **bill-com-autonomi** | Bill.com AP/AR | ap_ar_workflows, three_way_matching, payment_settlement |
| **m365-autonomi** | Microsoft 365 | document_control, compliance_workflows, batch_record_templates |
| **gws-autonomi** | Google Workspace | document_hierarchy, formulation_calculators, audit_checklists |

## Structure

```
autonomi-domain-knowledge/
├── manifest.json                    # Skill registry
├── prompts/
│   ├── system_prompt.md             # LynZ domain knowledge access prompt
│   └── tools.json                   # Tool definitions (if needed)
├── skills/
│   ├── fb-product-formulation/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── formulation_science.md
│   │       ├── ingredient_interactions.md
│   │       ├── shelf_life_engineering.md
│   │       └── flavor_systems.md
│   ├── fb-food-safety-compliance/
│   │   ├── SKILL.md
│   │   └── references/...
│   └── ... (8 skills total)
└── README.md
```

## Related Repositories

- **[autonomi-dashboard-knowledge](https://github.com/lynz-tonomi/autonomi-dashboard-knowledge)** — Platform/operational knowledge (navigation, agent fleet, blockchain, IoT, SaaS)
- **[formulation-knowledge](https://github.com/lynz-tonomi/formulation-knowledge)** — Formulation Lab assistant knowledge (separate AI)

## Access Pattern

```
https://raw.githubusercontent.com/lynz-tonomi/autonomi-domain-knowledge/main/skills/{skill-id}/references/{file}.md
```

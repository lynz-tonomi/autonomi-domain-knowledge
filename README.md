# Autonomi Domain Knowledge

Consolidated knowledge base for all Autonomi AI agents. Contains deep industry domain expertise, platform-specific skills, and lab workflows — all in one repo. Each agent fetches only what it needs.

## Agents

- **LynZ (Dashboard)** — Autonomi Operations AI, voice agent for the main dashboard
- **LynZ (Formulation Lab)** — R&D assistant for the Formulation Lab dashboard

## Domains

### Shared (used by all agents)
| Skill | Domain | Key References |
|-------|--------|----------------|
| **fb-product-formulation** | Beverage formulation science | ingredient_science, beverage_formulation, formulation_math, scale_up, shelf_life, sensory_evaluation, regulatory_formulation |
| **fb-food-safety-compliance** | Food safety & regulatory | haccp_advanced, fsma_regulatory, allergen_management, audit_certification |
| **fb-supply-chain-v2** | F&B supply chain ops | production_scheduling, inventory_management, procurement, logistics_warehousing, cost_management, demand_planning, + 5 more |
| **fb-product-dev** | Product development & NPD | stage_gate_process, formulation_scaleup, packaging_commercialization, regulatory_claims, timeline_templates |
| **qbo-autonomi** | QuickBooks Online | auth, qbo_api_entities, qbo_api_patterns, fb_chart_of_accounts, cogs_batch_costing, webhooks_and_sync, security |
| **bill-com-autonomi** | Bill.com AP/AR | ap_ar_workflows, bill_api_v3, three_way_matching, payment_settlement, security |
| **m365-autonomi** | Microsoft 365 | outlook, sharepoint, excel, teams, security |
| **gws-autonomi** | Google Workspace | gmail, drive, sheets, docs, calendar, security |

### autonomi-dashboard (LynZ Dashboard only)
| Skill | Description |
|-------|-------------|
| **ai-agent-orchestration** | 29 autonomous agents, fleet management, cascade demos |
| **blockchain-traceability** | FSMA 204, blockchain architecture, recall management |
| **agentic-wallet** | USDC settlement, payment flows, smart contracts |
| **investor-tours** | Live tour script, ecosystem tour, pitch talking points |
| **iot-monitoring** | 342 sensors, environmental compliance, alert rules |
| **erp-integration** | SAP/NetSuite/QBO sync, data models |
| **saas-platform** | Multi-tenant management, billing tiers, platform architecture |
| **supply-chain-ops** | Dashboard supply chain views |
| **food-safety-compliance** | Dashboard compliance views, HACCP CCPs |

### formulation-lab (LynZ Formulation Lab only)
| Skill | Description |
|-------|-------------|
| **formulation-lab** | Dashboard navigation, CRUD operations, portfolio (8 recipes), view knowledge |

## Structure

```
autonomi-domain-knowledge/
├── manifest.json
├── prompts/
│   └── system_prompt.md
├── skills/
│   ├── fb-product-formulation/        ← shared
│   ├── fb-product-dev/                ← shared
│   ├── fb-food-safety-compliance/     ← shared
│   ├── fb-supply-chain-v2/            ← shared
│   ├── m365-autonomi/                 ← shared
│   ├── gws-autonomi/                  ← shared
│   ├── bill-com-autonomi/             ← shared
│   ├── qbo-autonomi/                  ← shared
│   ├── autonomi-dashboard/            ← dashboard agent
│   │   ├── ai-agent-orchestration/
│   │   ├── blockchain-traceability/
│   │   ├── agentic-wallet/
│   │   ├── investor-tours/
│   │   ├── iot-monitoring/
│   │   ├── erp-integration/
│   │   ├── saas-platform/
│   │   ├── supply-chain-ops/
│   │   └── food-safety-compliance/
│   └── formulation-lab/               ← formulation lab agent
│       ├── SKILL.md
│       └── references/
│           ├── dashboard_navigation.md
│           ├── crud_operations.md
│           ├── portfolio.md
│           └── view_knowledge.md
└── README.md
```

## Access Pattern

```
https://raw.githubusercontent.com/lynz-tonomi/autonomi-domain-knowledge/main/skills/{skill-id}/references/{file}.md
```

For dashboard-specific skills:
```
https://raw.githubusercontent.com/lynz-tonomi/autonomi-domain-knowledge/main/skills/autonomi-dashboard/{skill-id}/references/{file}.md
```

For formulation lab skills:
```
https://raw.githubusercontent.com/lynz-tonomi/autonomi-domain-knowledge/main/skills/formulation-lab/references/{file}.md
```

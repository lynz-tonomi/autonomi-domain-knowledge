# Tenant Management Reference
**Skill:** saas-platform | **Domain:** tenants | **Version:** 1.0.0

---

## 1. Active Tenants

| Tenant ID | Name | Plan | Status | Live Since | MRR | Agents | Suppliers |
|---|---|---|---|---|---|---|---|
| TNT-001 | PurePress Beverages | Enterprise | Active | 2025-03-01 | $185,000 | 29 | 28 |
| TNT-002 | Cascade Drinks | Growth | Active | 2025-07-15 | $248,000 | 10 | 18 |
| TNT-003 | VitaFlow | Growth | Active | 2025-09-01 | $192,000 | 10 | 14 |
| TNT-004 | SunRise RTD | Starter | Active | 2025-11-12 | $160,000 | 5 | 9 |

---

## 2. Tenant Provisioning Workflow

### 2.1 New Tenant Onboarding Steps

**Week 1: Foundation**
1. Workspace creation: isolated tenant namespace, database schema, S3 bucket, blockchain channel
2. Admin user provisioning: tenant admin email, temp password, MFA enforcement
3. Plan module enablement: assign features per plan tier
4. Agent fleet deployment: instantiate agent sandboxes (5 / 10 / 29 per plan)
5. ERP connection setup: credentials, API keys, test connections

**Week 2: Data Integration**
6. Ingredient / item master import: from ERP or CSV template
7. BOM / recipe upload: template-guided import
8. Supplier master setup: vendors, contacts, payment info, USDC wallet setup (if applicable)
9. Warehouse and zone configuration: storage zones, IoT sensor mapping
10. User accounts: operations team, QA team, finance team per RBAC roles

**Week 3: Validation**
11. Test production order: end-to-end workflow run
12. Test PO and payment: mock procurement cycle
13. IoT sensor verification: confirm all sensors reporting
14. ERP sync validation: bidirectional test records
15. HACCP plan entry: CCP configuration in compliance module

**Week 4: Go-Live**
16. Training: LynZ voice agent orientation for all users
17. Soft launch: 2-week parallel run with existing systems
18. Full launch: Autonomi becomes primary operations platform
19. Hypercare: daily check-ins for first 30 days
20. Transition to standard support SLA

---

## 3. Tenant Module Access by Plan

| Module | Starter | Growth | Enterprise |
|---|---|---|---|
| Dashboard (overview) | Yes | Yes | Yes |
| Production & BOM | Yes | Yes | Yes |
| Inventory & Supply Chain | Yes | Yes | Yes |
| AI Agents (grid view) | Yes (5 agents) | Yes (10 agents) | Yes (29 agents) |
| AI Agents (neural map) | No | Yes | Yes |
| AI Agents (mission control) | No | Yes | Yes |
| IoT Sensors | Basic (up to 50 sensors) | Full (up to 500) | Full (unlimited) |
| Blockchain Explorer | Yes | Yes | Yes |
| Quality & Compliance | Yes | Yes | Yes |
| Recall & Trace | Yes | Yes | Yes |
| FSMA 204 | Yes | Yes | Yes |
| CAPA Management | No | Yes | Yes |
| Allergen Control | Yes | Yes | Yes |
| QC Inspection | Yes | Yes | Yes |
| ERP Integrations | 1 ERP connection | 2 ERP connections | Unlimited |
| Agentic Wallet | Yes (ACH only by default) | Yes (USDC enabled) | Yes (USDC + lending) |
| Settings | Yes | Yes | Yes |
| Network Intelligence | No | Read-only | Full access + API |
| Client Management | N/A | N/A | N/A (Admin only) |
| SaaS Billing | N/A | N/A | N/A (Admin only) |
| Participant Portal (white-label) | No | Yes (up to 5 participants) | Yes (unlimited) |

---

## 4. Agent Limits by Plan

| Plan | Agent Slots | Pre-configured Agents | Custom Agent Slots |
|---|---|---|---|
| Starter | 5 | 4 standard | 1 |
| Growth | 10 | 8 standard | 2 |
| Enterprise | 29 | All 29 | Custom agents on request |

**Standard agent pre-configurations by plan:**
- Starter (5): Inventory, Procurement, QA Inspector, FSMA Recorder, Settlement
- Growth (10): All Starter + Logistics, Supplier Scorer, Allergen Control, Certification Tracker, Invoice Processor
- Enterprise (29): Full fleet — all 29 agents listed in agent_fleet.md

---

## 5. Tenant Isolation Architecture

Each tenant is fully isolated at every layer:

| Layer | Isolation Method |
|---|---|
| Application | Separate tenant namespace in all API routes |
| Database | Separate PostgreSQL schema per tenant; row-level security as defense-in-depth |
| File storage | Separate S3 bucket prefix per tenant |
| Blockchain | Separate Hyperledger channel per tenant |
| AI agents | Separate OttoClaw sandbox instances per tenant per agent |
| Inference | Separate model session per tenant; no cross-tenant context |
| Payments | Separate Ampersend policy set and wallet per tenant |
| Monitoring | AGNT-22 processes only the tenant's registered sensor pool |

**What is shared (anonymized aggregates only):**
- Network Intelligence benchmarking (tenant identity masked)
- Platform health monitoring
- Commodity index trends (no individual transaction data)

---

## 6. Tenant Health Metrics (Current)

| Tenant | Login Frequency | Last Active | Agent Utilization | OTIF | Active Agents |
|---|---|---|---|---|---|
| PurePress Beverages | Daily (Weston) | Live session | 29/29 active | 96.8% | 29 |
| Cascade Drinks | Daily (ops team) | 2 hrs ago | 10/10 active | 94.1% | 10 |
| VitaFlow | Daily | 4 hrs ago | 9/10 active (1 in maintenance) | 97.3% | 9 |
| SunRise RTD | 3x/week | Yesterday | 5/5 active | 93.6% | 5 |

---

## 7. Tenant Support Tiers

| Plan | Support Response | Dedicated CSM | Onboarding |
|---|---|---|---|
| Starter | 8-hour response (business hours) | No | Self-service + guided |
| Growth | 4-hour response (business hours) | Shared CSM (1:8) | Assisted 4-week onboarding |
| Enterprise | 1-hour response (24/7) | Dedicated CSM | Full concierge 4-week onboarding + hypercare |

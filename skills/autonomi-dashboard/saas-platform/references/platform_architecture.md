# Platform Architecture Reference
**Skill:** saas-platform | **Domain:** architecture | **Version:** 1.0.0

---

## 1. Role-Based Access Control

### 1.1 Role Hierarchy

```
Autonomi Admin (Weston)
    ├── All pages and features
    ├── Tenant management
    ├── Platform analytics
    ├── SaaS billing
    └── System configuration

Tenant Admin
    ├── All tenant operational pages
    ├── User management (within tenant)
    ├── ERP connection management
    └── Agent configuration (within plan limits)

Tenant Operations
    ├── Dashboard, BOM, Production, Inventory
    ├── AI Agents (view + manual override)
    ├── IoT Sensors (view + acknowledge alerts)
    └── Quality & Compliance (view + data entry)

Tenant QA/Compliance
    ├── Quality & Compliance
    ├── Recall & Trace
    ├── CAPA Management
    ├── FSMA 204
    ├── Allergen Control
    └── QC Inspection

Tenant Finance
    ├── Agentic Wallet (view + approve payments)
    ├── ERP Integrations (view sync status)
    └── Dashboard (view only)

Participant (Supplier / Distributor)
    ├── participant-dashboard
    ├── participant-production (their own orders only)
    ├── participant-ai-agents (status of agents affecting them)
    ├── participant-products (their own products)
    ├── participant-portal (document upload, COA submission)
    ├── participant-wallet (their own USDC balance)
    └── participant-offramp (convert USDC to fiat)
```

### 1.2 Admin-Only Pages

| Page | Access | Purpose |
|---|---|---|
| `tenants` | Admin only | Client Management — all tenants, provisioning, health |
| `platform-analytics` | Admin + Enterprise tenants (read-only for tenant) | Network Intelligence — cross-tenant benchmarking |
| `saas-billing` | Admin only | Revenue dashboard — MRR, ARR, micro-transactions |

### 1.3 Page Access by Role

| Page | Admin | Tenant Admin | Operations | QA | Finance | Participant |
|---|---|---|---|---|---|---|
| dashboard | ✓ | ✓ | ✓ | ✓ | ✓ (view) | ✓ (limited) |
| bom | ✓ | ✓ | ✓ | ✓ (view) | ✗ | ✗ |
| production | ✓ | ✓ | ✓ | ✓ (view) | ✗ | ✗ |
| ai-agents | ✓ | ✓ | ✓ | ✓ (view) | ✗ | ✓ (limited) |
| iot | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| blockchain | ✓ | ✓ | ✓ | ✓ | ✓ (view) | ✓ (their records) |
| compliance | ✓ | ✓ | ✓ (view) | ✓ | ✗ | ✗ |
| quality-alerts | ✓ | ✓ | ✓ (view) | ✓ | ✗ | ✗ |
| qc-inspection | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| capa | ✓ | ✓ | ✓ (view) | ✓ | ✗ | ✗ |
| fsma | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| allergen | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| erp | ✓ | ✓ | ✓ (view) | ✗ | ✓ (view) | ✗ |
| billing | ✓ | ✓ | ✗ | ✗ | ✓ | ✓ (own wallet) |
| settings | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| tenants | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| platform-analytics | ✓ | ✓* (Enterprise) | ✗ | ✗ | ✗ | ✗ |
| saas-billing | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |

---

## 2. Participant Portal

### 2.1 Overview

The Participant Portal is a white-label web application accessible by suppliers and distributors invited by tenants. Each tenant can brand the portal with their own logo and color scheme.

**Participant Portal URL structure:** `https://{tenant-slug}.autonomi.llc/portal`  
**PurePress portal:** `https://purepress.autonomi.llc/portal`

### 2.2 Supplier Participant Capabilities

| Capability | Description |
|---|---|
| COA upload | Upload Certificate of Analysis for each delivered lot |
| Delivery confirmation | Confirm delivery details; view IoT receipt confirmation |
| PO view | See their open purchase orders from the tenant |
| Invoice submission | Submit invoices directly; linked to PO for 3-way match |
| USDC wallet | View their USDC balance; see settlement history |
| Off-ramp | Convert USDC to fiat via the participant off-ramp |
| Quality score | View their supplier score and contributing factors |
| Document library | Access their approved certifications and compliance documents |

### 2.3 Distributor/Customer Participant Capabilities

| Capability | Description |
|---|---|
| Order status | View shipment status and tracking |
| Traceability | View blockchain records for their received lots |
| Document access | Retrieve COAs, FSMA 204 records, quality certificates for their orders |
| Recall notifications | Receive automated alerts if their received product is subject to recall |

---

## 3. Technical Infrastructure

### 3.1 Application Stack

| Component | Technology | Hosting |
|---|---|---|
| Frontend (dashboard) | React 18 + TypeScript + Tailwind CSS | Vercel (global CDN) |
| Frontend (participant portal) | React 18 + white-label theming | Vercel |
| API Gateway | Node.js + Express | AWS us-west-2 |
| Agent runtime | OttoClaw OpenShell sandbox | NVIDIA Cloud / on-prem |
| Blockchain | Hyperledger Fabric 2.5 | Dedicated nodes (AWS + on-prem option) |
| Database | PostgreSQL 15 (multi-schema) | AWS RDS |
| File storage | AWS S3 (per-tenant bucket) | AWS us-west-2 |
| Message bus | Apache Kafka | AWS MSK |
| IoT ingestion | MQTT broker (HiveMQ) → Kafka | AWS |
| Payment gateway | Ampersend + Coinbase AgentKit | Base L2 |
| Voice agent | OpenAI Realtime API (gpt-4o-realtime-preview) | OpenAI |

### 3.2 Uptime SLA

| Plan | SLA | Measurement Window |
|---|---|---|
| Starter / Growth | 99.5% | Monthly |
| Enterprise | 99.9% | Monthly |

99.9% = maximum 43.8 minutes downtime per month  
Scheduled maintenance: Sundays 02:00–04:00 PT (excluded from SLA calculation)

### 3.3 Disaster Recovery

| Objective | Target |
|---|---|
| Recovery Time Objective (RTO) | < 4 hours |
| Recovery Point Objective (RPO) | < 15 minutes |
| Database backup frequency | Every 15 minutes (point-in-time recovery) |
| Blockchain backup | Distributed by design — no single point of failure |
| Backup retention | 30 days |
| DR test frequency | Quarterly |

---

## 4. Security Architecture

### 4.1 Data Security

| Layer | Control |
|---|---|
| Data in transit | TLS 1.3 minimum; certificate pinning for critical endpoints |
| Data at rest | AES-256 encryption (AWS KMS) |
| Database | Encrypted at rest; TDE enabled; separate encryption key per tenant |
| Formulation data | Never leaves on-prem (OttoClaw) for Enterprise on-prem deployments |
| API authentication | OAuth 2.0 + JWT (15-minute expiry); refresh token rotation |
| MFA | Enforced for all Admin and Tenant Admin roles |

### 4.2 Compliance Certifications (Platform)

| Standard | Status |
|---|---|
| SOC 2 Type II | In progress (audit scheduled Q3 2026) |
| ISO 27001 | Roadmap (Year 2) |
| GDPR | Compliant (EU tenant data segregated to EU region) |
| CCPA | Compliant |
| HIPAA | Not applicable (food, not healthcare) |

### 4.3 Penetration Testing

Annual penetration test by third-party firm (HackerOne VDP maintained between tests). Last pentest: 2025-11-01. No critical findings. 3 medium findings — all remediated within 30 days.

---

## 5. LynZ Voice Agent — Technical Integration

### 5.1 Session Architecture

LynZ operates as an OpenAI Realtime API session:
- Model: gpt-4o-realtime-preview
- Voice: shimmer
- Turn detection: server_vad (threshold: 0.5, silence: 700ms)
- System prompt: 328-line instruction set (system_prompt.md)
- Tools: 30 registered functions (tools.json)

### 5.2 Tool Dispatch

Tool calls from the Realtime API stream are handled by the dashboard host application:
- Navigation tools: update React router + dashboard state
- Demo tools: fire pre-built animation sequences via event bus
- Browser tools: route to OpenClaw CDP bridge (headed Chrome)
- Email tools: route to lynz@autonomi.llc mailbox integration
- Dashboard state tools: update UI directly (toast notifications)

### 5.3 Voice Agent Access Control

| Role | LynZ Access |
|---|---|
| Admin (Weston) | Full access — all pages, all tools |
| Tenant Admin | All tenant pages and tools |
| Operations | Operations pages; no billing/payment tools |
| QA | Quality pages only |
| Participant | Participant pages only; no admin tools |

LynZ automatically presents herself in the context of the logged-in user's role. An operations user asking about payment details will be told to escalate to the Finance role.

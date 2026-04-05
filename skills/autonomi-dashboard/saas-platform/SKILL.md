---
name: SaaS Platform
description: Multi-tenant SaaS management — tenant provisioning, plan tiers, billing, RBAC, and white-label participant portal
domain: platform
version: 1.0.0
---

# SaaS Platform

## Overview
Autonomi operates as a multi-tenant SaaS platform with three subscription tiers (Starter, Growth, Enterprise) plus usage-based billing via micro-transactions. The Admin role (Weston) has access to all pages including Tenants, Platform Analytics, and SaaS Billing. Each tenant gets their own isolated environment with role-based access control. Participants (suppliers, distributors) access a white-label participant portal with limited views.

## Capabilities
- Tenant provisioning: workspace creation, module assignment, agent limits, ERP connections
- Three-tier plan management: Starter ($7.5K/month), Growth ($12.5K/month), Enterprise (custom)
- Usage-based billing via micro-transactions (USDC per agent decision)
- Role-based access control: Admin, Tenant (ops), Participant (supplier/distributor)
- White-label participant portal with custom branding per tenant
- Network Intelligence page: cross-tenant benchmarking, aggregate KPIs
- SaaS Billing page: MRR, ARR, tenant billing, micro-transaction revenue dashboard

## Reference Files
- `references/tenant_management.md` — Tenant provisioning, module assignment, agent limits, workspace isolation
- `references/billing_model.md` — Plan tiers, usage pricing, micro-transaction rates, USDC billing
- `references/platform_architecture.md` — RBAC roles, white-label portal, multi-tenant data isolation, Admin capabilities

## Usage
Load this skill when Weston asks about platform management, tenant settings, billing, SaaS metrics, new tenant onboarding, or user roles. Navigate to `tenants` for Client Management, `saas-billing` for revenue dashboard, `platform-analytics` for Network Intelligence. Admin-only pages.

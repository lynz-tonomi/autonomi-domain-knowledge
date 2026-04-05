---
name: Agentic Wallet
description: USDC stablecoin payments, smart contract settlement on Base L2, and AP/AR workflow automation
domain: payments
version: 1.0.0
---

# Agentic Wallet

## Overview
The Agentic Wallet is Autonomi's payment infrastructure layer, built on Ampersend by Edge & Node using Coinbase's x402 protocol. Every financial decision made by an AI agent is governed by policy-based controls before any USDC moves. Smart contracts release payments automatically when IoT sensors confirm delivery to the correct location under the right conditions. Settlement occurs in 2.4 seconds on Base L2. The Agentic Wallet page shows each agent's virtual card, transaction history, escrow accounts, and off-ramp to fiat.

## Capabilities
- USDC smart contract payment execution with IoT-triggered release conditions
- Per-agent virtual card tracking (Agent Cards) via Ampersend
- Daily and per-transaction budget enforcement per tenant
- Bill.com AP/AR workflow integration (10-step PO → vendor invoice → QA → CFO → ACH/USDC)
- QuickBooks Online sync for all payment transactions
- Off-ramp: USDC → fiat conversion via Base L2 bridge
- Escrow management: hold, dispute, and release workflow
- Cross-tenant aggregate: $84.2M monthly USDC volume across all tenants

## Reference Files
- `references/usdc_settlement.md` — Base L2, Ampersend architecture, smart contract execution, 2.4s finality, Agent Cards
- `references/payment_flows.md` — AP/AR 10-step workflow, Bill.com integration, QBO sync, off-ramp to fiat

## Usage
Load this skill when Weston asks about payments, USDC, smart contracts, the agentic wallet, invoices, bill payments, the off-ramp, or agent spend. Navigate to `billing` for wallet view, or `billing` View 2 for off-ramp. Keywords: "wallet", "USDC", "contracts", "off-ramp", "payments".

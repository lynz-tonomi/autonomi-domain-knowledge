---
name: AI Agent Orchestration
description: Management and configuration of the 29 autonomous AI agents that run the Autonomi platform
domain: agent-ops
version: 1.0.0
---

# AI Agent Orchestration

## Overview
Autonomi deploys 29 specialized autonomous AI agents that collectively handle ~2.4 million decisions per day across the platform network. Each agent runs in its own NVIDIA OttoClaw sandboxed environment with kernel-level isolation. Agents are organized into functional domains: operations, quality, finance, logistics, compliance, and intelligence. LynZ refers to all agents as "we" — they are extensions of her across the network.

## Capabilities
- Real-time monitoring of all 29 agent statuses, decision counts, and confidence scores
- Opening agent detail drawers via the AI Agents page (grid, neural map, or mission control views)
- Triggering and narrating the cascade demo (8-agent response in 38.8 seconds)
- Explaining what each agent does, its decision domain, and its escalation rules
- Describing the three AI Agents views: grid (card overview), map (cerebro neural map), mission (mission control)
- Reporting daily decision volumes, auto-approve rates, and escalation counts

## Reference Files
- `references/agent_fleet.md` — All 29 agents with IDs, names, domains, decision types, daily volumes
- `references/agent_configuration.md` — Confidence thresholds, auto-approve limits, escalation rules, OttoClaw sandbox specs
- `references/cascade_demos.md` — Happy path, crisis, and scale demo scenarios with timing and narrative

## Usage
Load this skill when Weston or a guest asks about the agent fleet, what a specific agent does, how agents make decisions, agent confidence levels, the cascade demo, or the three agent views. Always navigate to the ai-agents page when this topic is raised. Use show_agent_view to switch between grid/map/mission as appropriate.

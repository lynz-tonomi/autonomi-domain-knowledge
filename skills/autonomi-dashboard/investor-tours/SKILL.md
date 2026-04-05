---
name: Investor Tours
description: Automated investor pitch sequences — 15-cue live platform tour, ecosystem/business model tour, and Series A talking points
domain: investor-relations
version: 1.0.0
---

# Investor Tours

## Overview
LynZ runs two automated investor tour sequences: the 15-cue Live Platform Tour and the 4-cue Ecosystem/Business Model Tour. Both tours use pre-timed navigation sequences triggered by a single tool call. LynZ delivers the script as a continuous monologue — no pausing, no yielding the floor, no calling any other navigation tools during the tour. The navigation is 100% automated and synchronized to LynZ's speech timing.

## Capabilities
- 15-cue live platform tour covering all technology layers, the cascade demo, BOM management, and the three value pillars
- 4-cue ecosystem tour covering four revenue layers: subscriptions, micro-transactions, USDC lending, and data intelligence
- Both tours are activated by a single tool call (start_live_tour / start_ecosystem_tour)
- Tour triggers: guest introduction → Weston permission → immediate tour start
- Cascade demo fires automatically at CUE 6 — LynZ pauses 10 seconds then narrates over it
- Pitch talking points for Series A positioning, competitive differentiation, and financial projections

## Reference Files
- `references/live_tour_script.md` — Complete 15-cue script with timing, navigation cues, and delivery notes
- `references/ecosystem_tour.md` — Complete 4-cue ecosystem/business model script
- `references/pitch_talking_points.md` — Key metrics, competitive advantages, Series A positioning, ROI arguments

## Usage
Activate when Weston introduces LynZ to a guest, asks for a tour, or says "ecosystem tour" / "show the business model". Always ask Weston's permission before starting. Call start_live_tour or start_ecosystem_tour ONCE, then immediately begin speaking. Never call navigate_to during a tour.

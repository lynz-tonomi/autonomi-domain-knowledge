# Scaling Formulations from Bench to Production

## Table of Contents

1. [Introduction](#introduction)
2. [The Three Stages](#the-three-stages)
   - [Bench Scale (1–5 kg)](#bench-scale-1–5-kg)
   - [Pilot Scale (50–500 kg)](#pilot-scale-50–500-kg)
   - [Production Scale (1,000–50,000+ kg)](#production-scale-1000–50000-kg)
3. [Common Scale-Up Failures](#common-scale-up-failures)
   - [Mixing Inadequacy](#mixing-inadequacy)
   - [Heat Transfer Rate Mismatch](#heat-transfer-rate-mismatch)
   - [Ingredient Addition Order Sensitivity](#ingredient-addition-order-sensitivity)
   - [Homogenization Differences](#homogenization-differences)
   - [Cooling Rate Effects](#cooling-rate-effects)
   - [Foam and Air Incorporation](#foam-and-air-incorporation)
   - [pH Drift at Scale](#ph-drift-at-scale)
   - [Viscosity Development Shifts](#viscosity-development-shifts)
   - [Equipment Dead Volume and Concentration Gradients](#equipment-dead-volume-and-concentration-gradients)
4. [Scale-Up Decision Framework](#scale-up-decision-framework)
5. [Scale-Up Documentation Requirements](#scale-up-documentation-requirements)
6. [Equipment Considerations](#equipment-considerations)
7. [First Production Run Protocol](#first-production-run-protocol)
8. [Co-Packer Considerations](#co-packer-considerations)
9. [Troubleshooting at Scale](#troubleshooting-at-scale)
10. [References and Further Reading](#references-and-further-reading)

---

## Introduction

Scaling a food formulation is not multiplication—it is translation. A formula that performs flawlessly at 2 kg in a beaker will frequently fail at 500 kg in a pilot vessel, and fail again at 5,000 kg in production. This is not because the formula is wrong; it is because the physics, chemistry, and engineering change with scale. Heat does not distribute evenly. Mixing is not instantaneous. Shear is not uniform. Air gets trapped. Time slows everything down.

This document captures three decades of learning—much of it painful—about moving formulations from concept to manufacture. It is written for food scientists, process engineers, and product developers who must translate a bench success into a commercial reality.

---

## The Three Stages

### Bench Scale (1–5 kg)

**Equipment and Methods:**
Bench work uses hand mixing, beakers, magnetic stir bars, small rotor-stator homogenizers, and precision hotplates. You control temperature by eye and thermometer. You add ingredients in the order you decide, waiting exactly as long as you choose. Mixing is vigorous, uniform, and fast.

**What You Learn:**
At bench scale, you learn the formula works—ingredients dissolve, emulsions form, gels set, flavors integrate. You optimize ingredient ratios, identify the functional minimums and maximums of each component, and prove the concept. You can iterate rapidly: brew a batch every 2 hours, adjust, repeat.

**The Fatal Assumption:**
Bench results do NOT scale. Almost nothing behaves the same at 2 kg and 200 kg. The surface-area-to-volume ratio is dramatically different. Mixing intensity (watts per unit volume) is orders of magnitude higher at bench. Temperature uniformity at bench is artificial—everything is close to the heating source. Shear is local, not distributed. Residence times are seconds, not minutes.

When a bench formula fails at pilot, the formula is not wrong—the parameters are. You have discovered that your bench process was over-specified for a particular condition (e.g., your guar gum required vigorous local mixing that a production mixer cannot provide uniformly). Bench scale found a working point; scale-up finds the constraints.

**Typical Bench Equipment:**
- Magnetic stir bar (300–1,000 RPM, ~0.5–2 W/L tip speed)
- Electric hotplate or heating mantle (1–5 kW)
- Small rotor-stator homogenizer (1–3 kW, Silverson, IKA, or similar; tip speeds 5,000–11,000 RPM)
- Beakers, graduated cylinders, thermometers, hydrometers, viscometers
- Gravity dispensing or pipettes for ingredient addition

---

### Pilot Scale (50–500 kg)

**Equipment and Methods:**
Pilot plants use scaled-down versions of production equipment. A 100 kg pilot kettle resembles the 5,000 kg production kettle in geometry and mechanical principle. Agitation is overhead-drive, not magnetic. Heating is jacketed or via heat exchanger. Homogenization is rotor-stator at pilot scale or a small high-pressure homogenizer. Cooling is controlled via chiller. You measure with instruments: thermocouples, pressure gauges, flow meters.

**What You Discover:**
This is where the formula meets reality. Pilot scale reveals every process assumption you made unconsciously at bench:

- **Mixing adequacy:** Your stir bar was fast and local; the pilot agitator is slower and distributed. Dry powders that pre-dispersed in 30 seconds now need 2 minutes and gentle initial blending to avoid fish-eyes. You discover hydrocolloids need different addition sequences.

- **Heat transfer:** Your 1 kg batch reached 80 °C in 90 seconds on the hotplate. Your 100 kg pilot batch takes 8 minutes to come to temperature. Longer heating = color loss in caramel systems, over-gelatinization of starch, nutrient degradation, flavor volatilization.

- **Mixing-heating interaction:** At bench, you can stir and heat simultaneously without issue. At pilot, you may need to heat first (with no mixing, risking scorching) or mix and heat separately (adding time and complexity). The sequence matters.

- **Homogenization differences:** The rotor-stator at bench runs at 10,000 RPM; the pilot version also runs at 10,000 RPM but with a larger rotor and higher throughput. Residence time is shorter. Shear is higher locally but distribution is different. Droplet size in emulsions may differ.

- **Foaming:** The larger surface area and longer mixing time mean more air incorporation. Deaeration becomes necessary. A formula that never foamed at bench may foam in the pilot, affecting fill accuracy and shelf life (oxidation via entrapped air).

- **Ingredient compatibility with equipment:** Abrasive fillers (sand, pumice) that were fine at bench now damage the rotor seals on the pilot homogenizer. Sticky doughs that were manageable with a stir bar now foul the pilot agitator.

- **Scaling rules don't work:** You cannot scale by volume alone. A 50× scale-up requires different RPM, different heating rates, different addition sequences. What worked at 2 kg does not work at 100 kg, even with proportional adjustments.

**Pilot is Go/No-Go:**
Pilot scale is where you decide if the formula is viable at production scale. A successful pilot run means:
- The formula can be mixed uniformly at production-feasible agitation speeds
- Heating and cooling happen within tolerable times and temperature ranges
- Ingredient addition sequences are forgiving (not knife-edge)
- Shelf life and sensory stability match bench expectations
- Equipment does not degrade with the formula (no corrosion, no wear, no fouling)

A failed pilot run does not kill the formula; it identifies what must change. Common fixes:
- Slow the addition of hydrocolloids; pre-disperse them in a separate step
- Reduce target temperature by 5 °C; use longer mixing time instead
- Change the homogenization method (e.g., single-pass high-pressure instead of multi-pass rotor-stator)
- Reformulate slightly: use a different stabilizer, lower oil content to reduce foaming, add defoamer

Expect 2–4 pilot runs to dial in the process. This is not failure; it is expected learning.

---

### Production Scale (1,000–50,000+ kg)

**Equipment and Methods:**
Full-scale equipment is optimized for speed, volume, and consistency. Mixing is tank agitation via anchor, pitched-blade, or high-shear impellers. Heating is plate heat exchangers or scraped-surface heat exchangers (for high-viscosity or heat-sensitive products). Homogenization is high-pressure (200–1,000 bar), running at fixed pressures and passes. Cooling is via industrial chiller. Filling is automated: volumetric, piston, or net-weight fillers. Every step is logged: time, temperature, pressure, speed.

**The First Production Run is Not Guaranteed:**
You have a successful pilot formula and a production process specification. You know intellectually that the batch will scale, and you know empirically that it worked at 100 kg. Confidence is high. Then the first production run happens, and something is different.

The production mixer is faster but wider—mixing patterns are different. The heat exchanger comes up to temperature instantly (unlike the jacket), and cooling is brutal (5 °C overshoot on your target). The high-pressure homogenizer runs at 400 bar and two passes, creating much finer droplets than your pilot rotor-stator. The fill line drops product at a different temperature than your pilot run was handed off at. None of these are catastrophic individually; together, they mean your product is slightly thinner, more transparent (finer emulsion), and fills 2% slower than target.

Is it acceptable? Maybe. Maybe not. But you will not know until you run it.

**Commissioning Runs (3–5 batches minimum):**
Plan for 3–5 commissioning runs before commercial release. These are:
- Full-scale batches with full sampling and testing
- Documented carefully: every parameter logged, every sample tested in real-time
- Treated as go/no-go gates: can we adjust within spec, or must we stop and reformulate?

Expect to adjust minor parameters: agitation speed (±20 RPM), heating ramp rate (±5 °C/min), homogenization pressure (±25 bar), addition timing (±30 sec). These small changes keep the formula in spec without re-piloting.

Also expect equipment-specific fixes: the production kettle may have a dead zone near the bottom (material doesn't flow); you may need to pre-mix certain ingredients offline and add them as a pre-blend. The fill line may need the product warmed to 35 °C (not 30 °C) to run at target speed; this may require an additional holding tank.

**Production Means Constraints:**
Production formulations must be forgiving:
- Ingredient specs vary batch-to-batch (soy lecithin is never perfectly consistent); your formula must tolerate ±10% viscosity, ±5 pH units, ±15% water content in inputs
- Equipment is not perfect (heat exchangers have ±3 °C deviation, homogenizers have ±2% pressure variation); your formula must be robust to these deviations
- Operator variability is real (even with written procedures, addition timing varies ±1 minute, temperature readings vary ±1 °C); your formula must not be knife-edge
- Environmental factors matter (seasonal ambient temperature changes affect incoming water temperature, cooling times, viscosity at fill); your formula must adapt

A bench formula with zero margin becomes a production nightmare. A pilot formula that is forgiving and over-specified at bench becomes a production win.

---

## Common Scale-Up Failures

### Mixing Inadequacy

**The Problem:**
You formulated with vigorous local mixing (a magnetic stir bar at 800 RPM in a 2 L beaker). The stir bar creates laminar flow in the immediate vicinity and intense shear at the blade surface. Hydrocolloids, starches, and protein powders dissolve or disperse in seconds because the local environment is hostile: high shear, high turbulence, constant renewal of fresh water.

At pilot scale, the agitator may run at 150 RPM (on a 100 L kettle). The absolute agitation is faster, but the local intensity is much lower. Instead of intense localized shear everywhere, you have moderate bulk mixing with occasional high-shear pockets.

When you add your hydrocolloid (guar gum, xanthan) directly to the pilot kettle without pre-dispersion, it hits water, absorbs water, and forms a gel film on the surface. The low local shear cannot break this film. The gel film prevents fresh water from reaching the interior of the particles. The particles never fully hydrate. You get fish-eyes: tiny balls of unhydrated gum that persist through cooking, through homogenization, and into the finished product.

**Why It Happens:**
- Bench equipment has higher mixing intensity (W/L) than production equipment by 10–100×
- Local shear is not distributed; production equipment creates bulk mixing with pockets of high shear, not uniformity
- Dry powders need wetting (requires localized shear) before dispersion (requires bulk mixing)
- Hydrocolloids, if not pre-dispersed, form gel films that prevent hydration

**Mechanism at Each Scale:**
- **Bench (2 kg, stir bar at 800 RPM):** Guar gum added directly to water. Local shear prevents gel film formation. Hydration complete in 30 seconds. No fish-eyes.
- **Pilot (100 kg, agitator at 150 RPM):** Guar gum added directly to water. Local shear is insufficient. Gel film forms. Particles aggregate. Hydration incomplete. Fish-eyes present.
- **Production (5,000 kg, agitator at 80 RPM):** Guar gum added directly to water. Minimal local shear. Severe gel film formation. Massive fish-eye problem. May not disperse even with cooking.

**Mitigation:**
1. **Pre-disperse hydrocolloids in oil or a non-water phase** (if the formula permits). Guar gum dispersed in vegetable oil does not hydrate; it remains as dry particles. When added to water, the oil prevents gel film formation, and the gum hydrates uniformly.

2. **Pre-disperse hydrocolloids in sugar or salt solution** (if the formula permits). Higher solute concentration (e.g., 30% sugar solution instead of water) slows gel film formation, allowing more time for particle wetting.

3. **Add hydrocolloids as a dry blend with other dry ingredients.** Mix them dry first (ensuring uniform distribution), then add the dry blend to water slowly, with vigorous agitation. The mixing action of the bulk blend prevents localized gel formation.

4. **Use a hydrocolloid that is more shear-tolerant.** Some gums (e.g., low-acyl gellan) are less prone to fish-eye formation than others (xanthan, guar). Test in pilot to determine robustness.

5. **Adjust agitation speed and type.** Use a high-shear agitator (e.g., pitched-blade turbine) for the hydration step, then switch to a gentler agitator (e.g., anchor or ribbon) for gentle mixing during cooking. This requires planning the sequence.

6. **Slow the addition rate.** Adding guar gum at 0.5 kg/min to pilot (vs. 5 g/min at bench) ensures better wetting and prevents localized saturation. Use a dry-powder induction system (Silverson, Primix, etc.) if available.

7. **Accept minor reformulation.** Reduce gum level slightly (from 0.5% to 0.4%); the product may be thinner but will be fish-eye-free. The thinner product may acceptable for your application.

**Red Flag:**
If fish-eyes persist after pilot 2 or 3, the hydrocolloid choice is wrong for your process. Switch to a different gum or reformulate the structure (e.g., replace gum with starch or gelatin).

---

### Heat Transfer Rate Mismatch

**The Problem:**
At bench, you heat 2 kg on a hotplate. The entire mass reaches 80 °C in 90 seconds. The heating is intense, uniform, and fast. You pull the batch off heat immediately, and it cools to 25 °C in 2 minutes on the countertop (high surface-area-to-volume ratio).

At production scale, you are heating 5,000 kg in a jacketed kettle (or via heat exchanger). The batch takes 20–40 minutes to reach target temperature, depending on the jacket temperature and agitation. While the batch is slowly heating, chemical reactions continue: color precursors are oxidizing, flavor volatiles are escaping, starch is over-gelatinizing, proteins are denaturing.

A caramel sauce formulation that develops perfect color in 4 minutes at bench becomes dark brown (almost burnt) after 30 minutes of slow heating at production scale. A custard that sets at bench (15 min to cool) begins to break (syneresis, whey separation) during the long cooling phase at production scale.

**Why It Happens:**
- Surface-area-to-volume ratio is dramatically different. At bench, SA:V ≈ 6:1 (rough sphere); at production, SA:V ≈ 0.2:1.
- Heating source is diffuse at production (through a jacket or heat exchanger); at bench, it is direct and intense (hotplate coil immersed in liquid).
- Agitation is necessary at production to prevent scorching, but it also causes turbulence and air incorporation, affecting chemistry (oxidation of fats, flavor loss to vapor).
- Long residence time at elevated temperature accelerates degradation reactions, off-flavor formation, and nutrient loss.

**Mechanism at Each Scale:**
- **Bench (2 kg, hotplate, come-up time ~90 sec to 80 °C):** Brief heating window. Color develops in target range. Starch gelatinizes gently. Proteins remain native. Flavor intact. Pulled off heat; cools quickly; set is clean.

- **Pilot (100 kg, jacketed kettle, come-up time ~6 min to 80 °C):** Longer heating window. Color develops slightly past target. Starch is slightly over-gelatinized. Flavor slightly muted. Slower cooling (takes 8–10 min to reach 25 °C). Texture is softer; gelatin set is incomplete.

- **Production (5,000 kg, plate heat exchanger, come-up time ~25 min to 80 °C):** Very long heating window. Color is dark (caramelization proceeds past target). Starch is significantly over-gelatinized (paste becomes loose). Flavor is muted (volatiles lost). Cooling takes 30+ min; gelatin set is partial. Product may break or weep.

**Mitigation:**
1. **Lower target temperature slightly (2–5 °C lower than bench).** Instead of 80 °C, use 75 °C. The longer residence time at slightly lower temperature may reach the same degree of cook-out without over-processing.

2. **Use a faster heating method.** Plate heat exchangers heat much faster than jacketed kettles. A 5,000 kg batch can come to temperature in 8–12 minutes via PHE, vs. 30 minutes via jacket. This significantly reduces degradation.

3. **Reduce residence time at temperature.** If the batch must reach 80 °C, do so quickly (via PHE), hold for only the minimum time required (determined in pilot testing), then cool immediately. An inline holding tube (if needed for pasteurization) should be kept as short as possible.

4. **Reformulate for longer heating.** Use color precursors that are stable at elevated temperature longer (e.g., cocoa vs. caramel color; cocoa is more stable). Use a different starch (modified, cross-linked) that doesn't over-gelatinize. Use flavor compounds that are heat-stable (e.g., synthetic vanillin instead of real vanilla, which volatilizes).

5. **Add protective ingredients.** Antioxidants (vitamin C, vitamin E, rosemary extract) slow oxidation during long heating. Chelating agents (EDTA, citric acid) protect against metal-catalyzed color changes.

6. **Cool faster.** Use a scraped-surface heat exchanger (if product is thick) or a plate heat exchanger with chilled water on the other side. Cool from 80 °C to 40 °C in 5 minutes, not 30. This preserves texture and prevents gelatin-break or fat-grain formation.

7. **Simplify the process.** Can you pre-cook and hold, then add at fill? For example, if a chocolate-hazelnut spread requires long heating, pre-cook the chocolate and hazelnut components separately in smaller batches (faster), then blend at fill. This is common in contract manufacturing.

**Red Flag:**
If color or texture cannot be matched at production scale despite these adjustments, the formulation may be too process-sensitive for high-volume manufacturing. Consider reformulating with more stable ingredients or switching to a co-packer with better equipment (faster heat exchanger, smaller target scale).

---

### Ingredient Addition Order Sensitivity

**The Problem:**
You developed the formula by adding ingredients in a specific order: oil first, then water, then gum, then salt, then flavor. This order worked perfectly at bench. Why? Because at bench, you have tight control and instant feedback. If you deviate, you see it immediately (a bloom forms if you add gum to dry oil; a clump forms if you add salt without water; the mixture appears grainy if you add flavor last without mixing time).

At production scale, the order becomes critical because the mixing environment is less intense. A deviation that would resolve in 30 seconds at bench might persist for minutes at production, by which time other reactions have started. The gel-phase formation, hydration, and integration must happen in sequence.

Common example: You add guar gum to oil first (to pre-disperse), then add water while mixing. At bench, the oil-gum blend immediately hydrates and disappears into the bulk solution in 20 seconds. At pilot, the same procedure results in small oil droplets with trapped gum particles; the oil doesn't integrate smoothly. The reason: at bench, the vigorous mixing breaks apart the oil droplets and shears them into the water phase rapidly. At pilot, the lower mixing intensity means oil droplets coalesce slightly before integrating. The gum particles remain trapped at the oil-water interface, never fully hydrating.

Another example: You add salt after cooking at bench (to avoid over-salting via evaporation). At production, the salt is added after heat exchanger cooling. But the heat exchanger outlet is 65 °C, not ambient. The salt dissolves instantly at bench (room-temperature solution is saturation at ~36% NaCl). At 65 °C, saturation is higher; the salt may not fully dissolve during the brief residence in the holding tank. Undissolved salt crystals make it to filling and appear as grittiness in the finished product.

**Why It Happens:**
- Mixing intensity is lower at production; phase separation and integration are slower
- Residence time is distributed, not instantaneous; reactions that complete in seconds at bench may not finish during the flow-path residence
- Temperature changes affect solubility, viscosity, and kinetics; adding salt to 65 °C product is not equivalent to adding salt to 25 °C product
- Ingredient interactions are more sensitive at larger scale because dilution is slower; if you accidentally create a localized high-gum or high-salt pocket, it takes longer to homogenize out

**Mechanism at Each Scale:**
- **Bench (2 kg, guar added to oil, then water added while stirring at 800 RPM):** Oil droplets sheared instantly. Guar fully hydrates. No fish-eyes. Texture smooth. Time: 30 seconds.

- **Pilot (100 kg, same procedure, agitation at 150 RPM):** Oil droplets coalesce slightly. Guar particles remain at oil-water interface. Slight gumminess in texture. Time: 2 minutes to achieve similar texture to bench 30-second result. Still acceptable, but narrower margin.

- **Production (5,000 kg, same procedure, agitation at 80 RPM):** Oil pools in the bottom region. Guar particles aggregate at interfaces. Texture is noticeably gummy, slimy. Time: 5+ minutes to distribute oil and break apart oil pools. May not fully integrate. Fish-eyes may form from guar particles at oil-water interface.

**Mitigation:**
1. **Pre-disperse oil-based ingredients offline.** If guar must be added to oil, do this in a small side tank (5–10 kg batch) with high-speed mixing (rotor-stator, high-shear mixer). Create a pre-blend of oil + gum fully hydrated. Add this pre-blend to the production batch slowly. This decouples the oil wetting step (high-shear, offline) from the bulk mixing step (lower intensity, acceptable for integration).

2. **Add salts and pH-adjusters as solutions, not dry.** Dissolve salt in a portion of the recipe water (heat gently if needed to ensure full dissolution). Add this solution to the batch rather than dry salt. This ensures uniform distribution and prevents local super-saturation.

3. **Add temperature-sensitive ingredients at the correct temperature.** If flavor volatilizes above 50 °C, add it below 50 °C. If salt has different solubility at different temperatures, add it at the temperature where solubility is highest (or add as a solution). Do not assume the bench sequence will work if temperatures are different.

4. **Test ingredient addition sequences in pilot.** Never assume bench sequence will work. Run two pilot batches: one with your bench sequence, one with a revised sequence (e.g., dry premix, slower addition, later addition time, solution form). Determine which sequence gives better results at pilot scale. Lock in the winning sequence for production.

5. **Document the addition sequence with tolerances.** Do not write "add guar gum"; write "add guar gum at 30 seconds after water is added, as a dry powder at a rate of 2 kg/min, while maintaining agitation at 150 RPM, with the batch temperature between 35–40 °C." This removes ambiguity.

6. **Build in buffer steps.** If you must add guar, use a separate high-shear addition step before the bulk of the water is added. Example: (1) Add 10% of recipe water, (2) Add guar gum slowly at high shear (rotor-stator), (3) Once guar is fully dispersed, add remaining water and ingredients at normal agitation. This ensures guar is fully hydrated before the rest of the process can interfere.

**Red Flag:**
If bench and pilot require dramatically different addition sequences (e.g., bench requires adding guar to oil first; pilot requires adding guar to water first), the formulation is ingredient-limited and process-sensitive. Consider ingredient switching (a different gum, a different oil, a different type of starch) or reformulation.

---

### Homogenization Differences

**The Problem:**
At bench, you use a rotor-stator homogenizer (Silverson, IKA) at 8,000 RPM for 5 minutes. The rotor is typically 25 mm diameter, and the stator is a precision-machined cup with slots or chambers. The rotor spins inside the stator, creating violent shear and turbulence in the 0.5 mm gap between rotor and stator. Droplets are broken apart, and you achieve a target emulsion droplet size of 2–5 microns (as measured by laser diffraction or Zetasizer).

At production, the formula is run through a high-pressure homogenizer operating at 400 bar, 2 passes. This is a different animal. The homogenizer forces the liquid through a small orifice (0.15–0.5 mm) under pressure. The droplets are sheared by the sudden pressure drop and turbulence, not by a spinning rotor. The pressure and number of passes are what define the output. Running at 400 bar for 2 passes produces very fine droplets (1–2 microns, possibly finer).

The emulsion produced at production scale is finer than the emulsion produced at bench. Finer droplets mean:
- Lower viscosity (smaller interfacial area per unit oil, less resistance to flow)
- Higher transparency (light scattering is reduced with smaller droplets)
- Slower creaming and separation (smaller droplets rise more slowly)
- Different sensory perception (finer emulsion feels smoother, less grainy)
- Different behavior in downstream processing (faster draining, different flow at fill)

A bench formula that was a pourable cream (3% oil, 2 micron droplets, viscosity 200 cP) becomes thinner at production (same 3% oil, 1.5 micron droplets, viscosity 150 cP) because the finer emulsion has less viscosity.

**Why It Happens:**
- Rotor-stator homogenizers create shear via mechanical rotor rotation; the shear is intense but localized in the gap
- High-pressure homogenizers create shear via pressure drop; the shear is less intense but distributed across a small orifice
- Higher pressure = smaller droplets, but also = finer total size distribution (fewer large droplets)
- Residence time in a rotor-stator is longer (5 minutes with continuous flow, or 5 minutes batch); in a high-pressure homogenizer, residence time is very brief (seconds), but the intensity is very high
- Multiple passes through high-pressure homogenizer further reduce droplet size; a bench formula homogenized once at 8,000 RPM is equivalent to 0.5–1 pass through production homogenizer, not 2 passes

**Mechanism at Each Scale:**
- **Bench (2 kg, rotor-stator at 8,000 RPM, 5 min, 0.5% emulsifier):** Droplet size ~3 microns. Viscosity ~200 cP. Color opaque cream. Texture smooth, slight friction-feel.

- **Pilot (100 kg, rotor-stator at 8,000 RPM, 5 min, 0.5% emulsifier):** Droplet size ~2 microns. Viscosity ~180 cP. Color light cream. Texture smoother, less friction. (Rotor-stator at pilot scale is still rotor-stator; droplet size is similar.)

- **Production (5,000 kg, high-pressure homogenizer at 400 bar, 2 passes, 0.5% emulsifier):** Droplet size ~1.5 microns. Viscosity ~140 cP. Color light tan (more transparent). Texture very smooth, silky. Much lower viscosity than bench. (Finer droplets, reduced interfacial area, lower viscosity.)

**Mitigation:**
1. **Match homogenization method in pilot to production method.** If production will use a high-pressure homogenizer, use a high-pressure homogenizer in pilot (even at a smaller scale: Microfluidics M-110EH instead of rotor-stator). This ensures emulsion droplet size in pilot matches emulsion in production, so downstream viscosity and sensory match.

2. **Account for droplet size differences if methods must differ.** If pilot uses rotor-stator (because that is what you have) and production uses high-pressure (because that is the contract manufacturer's equipment), plan for slightly lower viscosity at production. Increase emulsifier or oil slightly in the formula to compensate. For example, if bench is 3% oil with rotor-stator, pilot may run 3% oil with rotor-stator (similar result), but production with high-pressure may need 3.2% oil to reach the same viscosity.

3. **Optimize pressure and passes for production.** Work with the contract manufacturer or equipment vendor to determine the right pressure and number of passes. Typical starting points:
   - Light emulsions (low oil, thin): 200 bar, 1 pass
   - Medium emulsions (moderate oil, medium viscosity): 300–400 bar, 1–2 passes
   - Heavy emulsions (high oil, thick): 400–600 bar, 2–3 passes
   Too much pressure or too many passes may over-process (breaking down emulsion stability, causing phase separation) or creating a paste-like product. Too little pressure or too few passes may leave coarse droplets.

4. **Test homogenization effect in bench/pilot.** Before committing to production, run a small batch at bench through different homogenization conditions:
   - Rotor-stator: 5,000 RPM, 5 min
   - Rotor-stator: 8,000 RPM, 5 min
   - Rotor-stator: 12,000 RPM, 5 min
   - High-pressure homogenizer (if available): 250 bar, 1 pass
   - High-pressure homogenizer: 400 bar, 1 pass
   - High-pressure homogenizer: 400 bar, 2 passes
   Measure droplet size, viscosity, and sensory for each. Identify which condition matches your target. Lock that into your production spec.

5. **Account for emulsion stability changes.** Finer emulsions (from high-pressure homogenization) may be more stable during storage (smaller droplets rise more slowly) but may be less stable during thawing or temperature cycling (different crystallization behavior in fats). Test stability at your target storage temperature and duration in each homogenization method.

6. **Consider re-formulation if sensitivity is high.** If the product must have very specific viscosity or appearance, and homogenization method differences are causing problems, consider reformulating:
   - Increase emulsifier level (helps stabilize finer droplets and increases viscosity)
   - Increase oil level slightly (increases viscosity)
   - Add a thickening agent (starch, gum) to increase viscosity independent of droplet size
   - Change the oil type (different oils have different interfacial tension, affecting ease of emulsification and final droplet size)

**Red Flag:**
If production homogenizer is high-pressure and pilot homogenizer is rotor-stator, always test production conditions in pilot or in a small-scale high-pressure homogenizer before full production run. The viscosity difference alone can cause filling issues, shelf-stability issues, or sensory problems.

---

### Cooling Rate Effects

**The Problem:**
At bench, you heat 2 kg on a hotplate to 80 °C, pull it off heat, and it cools to 30 °C on the countertop in 2–3 minutes. The cooling is rapid and allows quick set-up (for gelatin) or crystallization (for fats). A gelatin dessert that sets firmly in 2 hours at bench-cooled conditions may set only partially in 4 hours at production-cooled conditions, where cooling from 80 °C to 30 °C takes 25 minutes.

Why? Because gelatin sets via a phase transition (protein-water bonds form as temperature drops). The faster the cooling, the more uniform the gel network. Slower cooling allows more time for water to move, leading to syneresis (whey separation) at the margins and a weaker gel network overall. For emulsions with fat (e.g., mayonnaise, hollandaise), slow cooling allows fat crystals to grow too large, resulting in visible grain or oil leakage.

Another example: A dark chocolate ganache formula requires cooling to 28 °C to allow cocoa butter to crystallize in the desired polymorph (Form V, the glossy, snap-prone form). At bench, you cool rapidly, and Form V crystallizes. At production, cooling is slow via a jacketed kettle with chilled water flowing through the jacket. By the time the batch reaches 28 °C, it has been in the 35–28 °C range for 10+ minutes, allowing Form IV (dull, soft) or Form VI (soft, matte) to crystallize. The final product is dull and soft instead of glossy and snappy.

**Why It Happens:**
- Surface-area-to-volume ratio is much higher at bench; heat dissipates faster from a 2 L mass than from a 500 L mass
- Agitation at production helps with heat transfer but also allows more time for undesired crystal forms to nucleate and grow
- Gelatin hydration is slower at higher temperatures; slow cooling means more time for water to migrate away from gel network margins
- Fat polymorph formation is temperature-dependent and time-dependent; slow cooling through the crystallization range (35–25 °C) favors certain polymorphs over others
- Cooling rate also affects mousse foams (slow cooling allows bubble coalescence, resulting in coarse foam instead of fine); and protein gels (slow cooling allows protein aggregates to coalesce, resulting in weaker gel)

**Mechanism at Each Scale:**
- **Bench (2 kg, cooling on countertop to 25 °C in 2 min):** Gelatin sets firmly, no whey separation. Chocolate crystals in desired polymorph. Mousse foam remains fine. Protein gel is strong.

- **Pilot (100 kg, cooling via jacket with water at 15 °C, come-down time ~8 min):** Gelatin sets adequately; minimal whey separation. Chocolate crystals slightly less glossy. Mousse foam slightly coarse. Protein gel slightly softer.

- **Production (5,000 kg, cooling via jacketed kettle with chilled water, come-down time ~25 min):** Gelatin sets slowly; significant whey separation evident. Chocolate crystals dull, soft. Mousse foam coarse, unstable. Protein gel soft, weak, weeps readily.

**Mitigation:**
1. **Use a faster cooling method.** Plate heat exchangers cool much faster than jacketed kettles. For 5,000 kg, a PHE can cool from 80 °C to 30 °C in 8–12 minutes vs. 25 minutes for a jacket. Scraped-surface heat exchangers (for higher-viscosity products) are also fast.

2. **Increase cooling rate by stirring.** More vigorous agitation during cooling improves heat transfer coefficient. However, for foams or gels, vigorous agitation during cooling may break structure. Balance between cooling speed and structure preservation.

3. **Reformulate for slow cooling.** If production cooling is unavoidably slow (e.g., only jacketed kettle available), reformulate:
   - **For gelatin products:** Increase gelatin level (stronger gel network tolerates syneresis better). Add anti-syneresis agents (sodium citrate, carrageenan). Reduce water slightly (less water available to weep).
   - **For chocolate products:** Use cocoa butter alternatives or tempering agents that favor desired crystal form even with slow cooling. Or, skip traditional tempering and use confectionery coating instead of chocolate.
   - **For foams/mousses:** Use additional stabilizer (xanthan, gelatin) to prevent bubble coalescence. Increase air incorporation during mixing so final foam has target air content even if some coalescence occurs during cooling.

4. **Cool in stages.** If the batch must spend time in the 35–28 °C range for crystallization, cool rapidly to 35 °C (5 min), hold at 35 °C for short time (5 min) with minimal agitation (to allow crystal formation), then cool rapidly from 35 °C to 20 °C (5 min). This separates the cooling phases and controls which crystals form.

5. **Add crystallization nuclei.** For chocolate and fats, add a small amount of the desired crystal form (e.g., tiny seeds of chocolate in Form V polymorph) to a cooling batch. This encourages crystallization in the desired form even with slow cooling. (This is a specialty technique; requires working with chocolate specialists.)

6. **Hold temperature before cooling.** For some products (custards, sabayon), a brief hold at 65 °C before cooling allows proteins to set without cooling. Then cool rapidly. This avoids extended time in the 35–50 °C range where undesired structure forms.

7. **Test cooling rates in pilot.** Before production, run pilot batches with different cooling rates:
   - Fast: Jacketed kettle with water at 2 °C, high agitation (come-down time ~5 min)
   - Medium: Jacketed kettle with water at 10 °C, moderate agitation (come-down time ~10 min)
   - Slow: Jacketed kettle with water at 15 °C, minimal agitation (come-down time ~20 min)
   Measure gel strength, syneresis, crystal form, foam texture, for each. Identify which rate matches your target. If production cooling rate is unavoidably slow, use the reformulation data from the slow-cooling pilot batch.

**Red Flag:**
If the product requires very fast cooling to set (< 5 min) and production equipment can only provide slow cooling (> 20 min), the formulation may not be feasible at production scale. Consider re-formulation or equipment upgrade.

---

### Foam and Air Incorporation

**The Problem:**
At bench, you mix a recipe in a beaker with a magnetic stir bar at 800 RPM. The recipe is 2 kg. You mix for 8 minutes. At the end, the product is smooth, with no visible foam. The batch is ready for evaluation.

At production, you mix a 5,000 kg batch in a tank with an anchor agitator at 80 RPM for 20 minutes (proportional mixing time). You expect a similar result: smooth, no foam. Instead, you observe significant foam: 5–10% of the batch volume is foam. The foam is white (air-filled), and it persists even after removing from the agitator. What happened?

The issue is air incorporation rate. At bench, the stir bar is submerged and rotates at 800 RPM. It draws some air into the liquid (a little), but the residence time is brief (liquid is well-mixed in seconds) and the bubble coalescence is fast (small bubbles merge in the viscous liquid). The net air incorporation is low.

At production, the anchor agitator is in a large tank with a 3 m2 surface area. The tank is not closed; it is open to atmosphere. The agitator paddles move at low speed (80 RPM) but cover a large surface area. Each paddle pass incorporates a small amount of air, but 80 RPM × many passes over the surface area = significant cumulative air incorporation. The large surface area also means large bubble residence time (a bubble at the center of the tank takes minutes to rise to the surface, giving plenty of time for merging but also allowing new air to be incorporated elsewhere). The net air incorporation is high.

Foam affects:
- **Fill accuracy:** Volumetric fillers measure by volume, not weight. Foam is low-density; a 500 mL container filled with foam-laden product contains less actual product mass than a 500 mL container filled with foam-free product. Scales downstream reject it.
- **Shelf stability:** Entrapped air is oxidative. Fats oxidize, flavor compounds oxidize, color drifts. Product shelf life is reduced.
- **Appearance:** If foam is visible in the finished package (bubbles under the lid, foam on the surface), it looks defective.
- **Processing:** Foam affects homogenization, filling, and capping. Foam may cause the high-pressure homogenizer to cavitate (bubbles expanding/collapsing, damaging the pump).

**Why It Happens:**
- Production mixing with open vessel introduces air naturally over the large surface area and long mixing time
- Lower agitation speed at production (needed to avoid over-mixing) means longer mixing time, more air incorporation
- Larger batch volume and longer residence times for bubbles mean more coalescence opportunity, but also more time for fresh air to be incorporated
- Foaming tendency increases with certain ingredients: proteins (egg white foam easily), hydrocolloids (xanthan creates stable foam), emulsifiers (they stabilize air-water interface as well as oil-water interface)
- Surface-active ingredients (lecithin, mono- and diglycerides) that stabilize emulsions also stabilize foam

**Mechanism at Each Scale:**
- **Bench (2 kg, stir bar at 800 RPM, 8 min mixing):** Minimal air incorporation. Air that is incorporated quickly coalesces in the bulk liquid. Final product ~0.1% air content (not visually evident).

- **Pilot (100 kg, overhead agitator at 250 RPM, 15 min mixing):** Moderate air incorporation. Larger surface area means more air entry. Longer mixing time means more cumulative incorporation. Final product ~1–2% air content. Slight foam is visible on surface; mostly resolves if allowed to stand.

- **Production (5,000 kg, tank agitator at 80 RPM, 25 min mixing):** Significant air incorporation. Large surface area, long mixing time, open vessel. Final product ~5–10% air content. Visible foam layer; requires defoaming.

**Mitigation:**
1. **Add defoamer** (the most common solution in industrial food manufacturing). Defoamers (typically silicone-based, e.g., simethicone, or fatty acid-based emulsifiers) destabilize air-water interfaces, causing foam to collapse. Add 0.05–0.2% defoamer (depending on foaming tendency and formula type). Add defoamer at the end of mixing, after the batch is homogenized, and mix for 1–2 minutes. The batch is typically held in a holding tank for 10–30 minutes before filling, allowing residual bubbles to rise and coalesce.

2. **Vacuum deaeration** (used in high-end products where any defoamer residue is unacceptable). After mixing and homogenization, the batch is fed into a vacuum chamber (10–100 mbar absolute pressure). Air comes out of solution (Henry's Law), and foam collapses. The deaerated product is then transferred to filling. This is common in gelato, ice cream, and premium chocolate.

3. **Manage surface area during mixing.** Use a closed tank with a baffled lid (small opening for ingredient addition and thermometer). This reduces air incorporation from the start. However, this requires controlling heat and cooling through the jacket, which may slow heat transfer.

4. **Optimize agitation speed and time.** Pilot testing should identify the minimum mixing time needed to achieve uniformity without excessive agitation. Reduce mixing time if possible. Reduce agitation speed if uniformity permits. Example: if 150 RPM for 20 minutes achieves target uniformity, do not increase to 200 RPM (more air incorporation) or extend to 30 minutes (more air incorporation).

5. **Reformulate to reduce foam stability.** Certain ingredients stabilize foam unwantingly:
   - If possible, reduce egg white content (egg proteins foam readily)
   - Reduce xanthan gum level (high xanthan stabilizes foam; use a different gum if possible, or lower total gum level)
   - Use defoaming emulsifiers (e.g., switch from mono- and diglycerides to a non-foaming emulsifier)
   - Add anti-foam ingredients naturally: alcohol (10–15% in a formulation may reduce foam; check if feasible), salt (increases liquid density, slows bubble rise, promotes coalescence; 1–3% may help)

6. **Use an anti-foam surfactant that is part of the formulation.** Some formulations use a low level of a second emulsifier that is anti-foaming. For example, a mayonnaise might use lecithin (foaming) at 0.4% and simethicone (anti-foaming) at 0.01%. The net result is a stable emulsion with minimal foam.

7. **Post-foam deaeration.** If defoamer is used, the batch still contains some entrapped bubbles. Hold the batch in a tall, narrow holding tank for 15–30 minutes after mixing and defoaming. Allow bubbles to rise to the surface and merge. Skim off remaining foam. This is labor-intensive but ensures foam-free product at filling.

**Red Flag:**
If foam persists after adding reasonable levels of defoamer (0.1–0.2%), or if defoamer-free deaeration is required for product claims ("naturally defoamed" or "no additives"), the formulation may be too foaming for production. Consider reformulation or specialist deaeration equipment (vacuum deaeration system).

---

### pH Drift at Scale

**The Problem:**
You formulate at bench with a target pH of 3.5 (acidic salad dressing). You measure pH at bench (using a calibrated pH meter on a small sample), and it is 3.5. You document the result.

At pilot, you prepare the same formulation scaled up to 100 kg. You measure pH after mixing: 3.7 (higher than bench, less acidic than target). You measure pH after homogenization: 3.8 (even higher). The pH drifts upward by 0.3 units during processing. At production, the same formula yields pH 4.1 (significantly higher).

Why? The reasons are multiple:

1. **Acid dissolution rate:** At bench, you add vinegar (acetic acid) and it disperses throughout 2 kg in seconds. The acid quickly protonates water molecules (lowering pH). At production, you add vinegar to 5,000 kg. It disperses throughout the batch in minutes. During those minutes, some of the acid is being buffered by proteins, gums, and other ingredients that have partial pH-sensitive functional groups. The final equilibrium pH is higher than expected.

2. **Mixing uniformity affects pH measurement:** At bench, when you measure pH, you are sampling fully-equilibrated liquid. At production, the batch is being actively mixed. Unmixed regions (e.g., near the jacket wall, in dead zones) may have slightly different pH than the bulk. Measurement location matters. If you measure near the acid addition point, pH is lower (more acid concentrated). If you measure in a dead zone, pH is higher (acid never reached it fully).

3. **CO2 absorption:** Larger batches have more surface area and longer processing time. If the vessel is open or vented, CO2 from air dissolves into the liquid, forming carbonic acid (H2CO3), which lowers pH slightly. However, if deaeration occurs (vacuum or foam removal), CO2 may escape from the solution, raising pH slightly. The direction depends on initial CO2 saturation.

4. **Ingredient variability:** Individual ingredient lots have pH variation. Vinegar pH may vary from 2.5 to 3.0 depending on the source and storage. Soy sauce pH may vary from 4.2 to 4.5. At bench, you use one lot and get one result. At production, with 5,000 kg, you may use multiple lots of vinegar (if one 20 L jug runs out mid-batch). If lots have different pH, the final batch pH is the weighted average of the lots, which may differ from your bench pH.

5. **Yeast and bacterial fermentation (inadvertent):** This is rare but possible if the batch sits for hours before processing. Microbes in the formulation (if not adequately preserved or pasteurized) may produce acid (lactic, acetic) or consume acid, shifting pH. This is more common in pilot batches that sit in ambient temperature before homogenization vs. bench batches that are processed immediately.

**Why It Happens:**
- pH equilibration is kinetically limited; at bench, fast mixing means fast equilibration. At production, slow mixing means slow equilibration, and you measure pH before equilibration is complete.
- Larger batches have more complex buffering due to ingredient interactions; the effective buffering capacity may differ from bench.
- Larger batches have longer processing time; during that time, pH-altering reactions (acid dissociation, CO2 absorption/loss, fermentation) continue.
- Measurement location and timing matter more at production; a pH reading taken 5 minutes after acid addition (before full mixing) is not representative of the equilibrated batch pH.

**Mechanism at Each Scale:**
- **Bench (2 kg, vinegar added at time 0, mixed 30 sec, measured at 1 min):** All vinegar has dispersed and equilibrated. pH 3.5 (as intended).

- **Pilot (100 kg, vinegar added at time 0, mixed 5 min, measured at 10 min):** Vinegar has dispersed, but some pH buffering by ingredients is ongoing. pH measurement at 10 min: 3.6. If measured at 30 min (after full equilibration): 3.7.

- **Production (5,000 kg, vinegar added at time 0, mixed 20 min, measured at 30 min):** Vinegar has dispersed, full buffering equilibration reached. Ingredient interaction with acid is complete. pH at equilibrium: 4.1.

**Mitigation:**
1. **Use acid as a solution, not direct addition.** Instead of adding vinegar (or liquid acid) directly to the batch, dissolve the acid in a small amount of water offline first, then add this pre-mixed solution. This ensures the acid concentration is consistent and the acid-water interaction is complete before adding to the batch. Example: dilute 100 mL of acetic acid in 500 mL of water offline, then add this solution to the 5,000 kg batch. The batch pH will be more predictable.

2. **Account for buffering in the formulation.** Some ingredients buffer pH strongly (proteins, some gums, citrates). When formulating, use a test formulation at pilot scale to determine the buffering effect. If your bench formula required pH 3.5 and pilot requires pH 3.2 acid addition (to reach pH 3.5 after buffering), use the pilot-determined acid level at production. Document this: "Production formulation requires 0.8% citric acid (vs. 0.6% at bench) to achieve target pH 3.5 after equilibration."

3. **Allow adequate equilibration time before measurement.** Do not measure pH 2 minutes after adding acid. Allow 30 minutes after final mixing for full equilibration, then measure. This gives pH-sensitive species time to reach equilibrium. Document measurement timing: "Measure pH 30 minutes after completion of mixing, with batch at 25 °C, using calibrated pH meter."

4. **Measure pH in multiple locations.** At production, measure pH at several points: near the acid addition point, in the bulk (mid-tank), and in a cooler dead zone (if present). If variation is > 0.2 pH units, mixing is inadequate or pH equilibration is incomplete. Extend mixing time or increase agitation speed.

5. **Use a targeted acid level determined from pilot testing.** Do not assume bench acid level will work. Run a pilot formulation, document the actual acid requirement to reach target pH, and use that level at production. Example: bench required 0.6% citric acid; pilot required 0.7% citric acid (due to buffering by soy sauce and gum); production uses 0.7% citric acid.

6. **Control ingredient source if pH-sensitive.** For vinegar, soy sauce, or other pH-variable ingredients, specify supplier and lot in your sourcing. If possible, source from a single supplier's lot that you have pre-tested. This reduces lot-to-lot variability in the finished product pH.

7. **Use pH buffers if tight control is needed.** If your product requires pH 3.5 ± 0.1, use a buffer system (citric acid + sodium citrate, or acetic acid + sodium acetate). Buffers resist pH drift. For example, a 0.5% citric acid + 0.3% sodium citrate buffer system will maintain pH 3.2–3.4 across a range of ingredient and processing variations.

**Red Flag:**
If pH drifts > 0.3 units between bench and production despite using the same formulation and acid source, the formulation may be ingredient-limited (excessive buffering by proteins, gums, or other ingredients). Consider reducing the amount of high-buffering ingredients, or reformulate with different pH control strategy.

---

### Viscosity Development Shifts

**The Problem:**
You formulate a ketchup at bench. The formula includes tomato paste, corn starch, xanthan gum, and spices. At bench, you mix for 10 minutes, homogenize for 5 minutes at 8,000 RPM, and measure viscosity: 2,500 cP at 20 RPM (a shear rate typical of slow pouring). The viscosity is target.

At production, you repeat the same process: mixing for 10 minutes, homogenization for 5 minutes (now via high-pressure homogenizer at 400 bar, 2 passes instead of rotor-stator). You measure viscosity immediately after: 1,800 cP. The product is thinner than bench. Why?

The issue is shear history. Viscosity is not a fixed property; it is a function of shear rate and the material's shear history (especially for thixotropic and shear-thinning systems).

Xanthan gum is a shear-thinning polymer. When subjected to high shear (during homogenization), the polymer chains align and stretch, reducing viscosity. When shear is removed, the polymer relaxes and viscosity recovers—but not instantaneously. Recovery depends on time, temperature, and the degree of shear applied.

At bench, homogenization is at 8,000 RPM for 5 minutes. This is intense shear, but the batch is only 2 kg. The high-pressure homogenizer exits at a lower viscosity than the input (due to shear). But the batch then sits in a beaker on the bench for 5–10 minutes before viscosity measurement. During this rest time, the xanthan polymer partially recovers, and viscosity rises back up.

At production, homogenization is at 400 bar, 2 passes. This is intense shear over a short residence time (seconds). The batch exits the homogenizer and goes directly into a holding tank for filling. The batch is measured immediately (within 1 minute of exiting homogenizer) before polymer recovery is complete. The viscosity is measured at a lower value than bench because recovery was incomplete.

Another factor: the shear profile is different between rotor-stator and high-pressure homogenizer. A rotor-stator applies intense localized shear in the gap, but the residence time is long (batch circulates multiple times). A high-pressure homogenizer applies intense shear as pressure drops, but the residence time is brief. The distribution and intensity of shear are different, resulting in different degrees of polymer chain damage or alignment.

For starch-based systems, the issue is gelatinization and viscosity development. At bench, you cook to 95 °C and hold for 10 minutes. Starch gelatinizes and swells, developing viscosity. At production, you cook to 95 °C via a rapid plate heat exchanger (come-up time 5 minutes) and hold in a holding tube (residence time 2 minutes). The total heat exposure is much shorter (7 minutes vs. 15 minutes for bench come-up + hold). Starch gelatinization is incomplete, and viscosity is lower.

**Why It Happens:**
- Shear-thinning polymers (xanthan, guar, locust bean gum) show reduced viscosity immediately after high shear; recovery is gradual and may take minutes to hours, depending on the polymer and shear intensity
- High-pressure homogenization applies a different shear profile than rotor-stator; the resulting viscosity immediately post-homogenization may differ even if the polymers are identical
- Residence time at elevated temperature affects starch gelatinization, protein denaturation, and other time-temperature-dependent reactions
- Cooling rate affects starch retrogradation and gel formation; slow cooling may result in higher final viscosity (more complete starch swelling) than rapid cooling

**Mechanism at Each Scale:**
- **Bench (2 kg, homogenized 5 min at 8,000 RPM, measured 10 min post-homogenization):** Xanthan partially recovered during 10 min rest. Viscosity at 20 RPM: 2,500 cP.

- **Pilot (100 kg, homogenized 5 min at 8,000 RPM, measured 10 min post-homogenization):** Similar to bench (same homogenizer method). Viscosity at 20 RPM: 2,400 cP (slightly lower due to slightly larger scale, longer processing time, but similar recovery time).

- **Production (5,000 kg, homogenized 2 passes at 400 bar, measured 1 min post-homogenization):** Different homogenizer method, minimal recovery time. Viscosity at 20 RPM: 1,800 cP (25% lower than bench due to different shear profile and incomplete recovery).

**Mitigation:**
1. **Standardize homogenization method and recovery time between bench and pilot/production.** If bench uses rotor-stator, use rotor-stator in pilot. If production uses high-pressure, use high-pressure in pilot to see the actual viscosity result. Measure viscosity at a consistent time post-homogenization (e.g., 30 minutes after homogenization, allowing partial polymer recovery).

2. **Allow recovery time in production.** If shear-thinning polymers are part of your formula, allow the batch to rest for 20–30 minutes in a holding tank after homogenization before measurement or filling. This allows polymer recovery and gives more predictable viscosity. Document this: "After homogenization, allow batch to rest for 30 minutes at 25 °C before measuring viscosity or transferring to fill."

3. **Increase polymer or thickening agent to compensate for shear-thinning.** If production homogenization results in lower immediate viscosity, increase xanthan or guar slightly (from 0.3% to 0.35%) or add a non-shear-thinning thickener (modified starch, gelatin). The finished product viscosity will then match target.

4. **Optimize holding temperature and time.** For starch-based systems, the length and temperature of the holding step affect viscosity development. If you heat to 95 °C and want full starch gelatinization, hold at 95 °C for 5–10 minutes. If heating via high-speed plate heat exchanger (come-up time 5 minutes), the total thermal time may be sufficient. If heating via slow jacket (come-up time 20 minutes), total thermal time is automatically long enough. Test in pilot to determine if holding time is adequate for target viscosity.

5. **Use a cooler to control post-homogenization viscosity.** For some products, immediate post-homogenization viscosity is too low, and recovery is too slow. Cool the batch to a lower temperature (e.g., 15 °C) immediately after homogenization. Lower temperature speeds polymer relaxation and increases viscosity. The batch is then held at cool temperature for 15 minutes, achieving higher viscosity, before warming back to fill temperature (if needed).

6. **Test the full production process in pilot.** Do not assume bench homogenization data will match production. Run a full-scale pilot with the homogenization method, cooling, and holding steps you plan to use at production. Measure viscosity at the same time post-homogenization as production will measure it. Adjust formulation (thickener level) based on pilot result.

7. **Reformulate with less shear-sensitive components.** If viscosity control is critical and shear-thinning polymers are causing problems, reformulate using less shear-sensitive thickeners:
   - Replace xanthan (very shear-thinning) with gellan (less shear-thinning)
   - Replace guar (moderate shear-thinning) with starch or modified starch (largely shear-stable)
   - Use a combination of thickeners (e.g., 0.2% xanthan + 0.3% modified starch) to achieve target viscosity with less shear-sensitivity

**Red Flag:**
If production viscosity is consistently lower than bench/pilot despite using the same formulation and process conditions, and if increasing polymer levels causes other problems (taste, mouthfeel, stability), the formulation may be too shear-sensitive. Consider reformulation or a different thickening strategy.

---

### Equipment Dead Volume and Concentration Gradients

**The Problem:**
You plan a production batch: 5,000 kg of mayonnaise. You specify 4.0% salt. At bench, you make 2 kg with 80 grams of salt, mix, and the product is uniformly salty. At production, you add 200 kg of salt (4% of 5,000 kg) and expect uniform saltiness. Instead, portions of the batch are over-salted (5–6% salt) and portions are under-salted (2–3% salt).

Why? The batch does not enter the production vessel all at once. A typical production sequence:
1. Water (2,500 kg) is added to the tank and heated/cooled
2. Oil (1,750 kg) is added slowly while mixing
3. Emulsifier (25 kg) is added
4. Egg yolk (500 kg) is added
5. Vinegar (100 kg) is added
6. Salt (80 kg) is added
7. Spices (45 kg) are added
8. Batch is homogenized

The salt is added at step 6, after oil and egg yolk. But the batch does not reach uniformity instantly. The salt dissolves in the water phase, but the water phase is dispersed as droplets within the oil (this is an inverted emulsion during the assembly process, before homogenization). The salt concentration in the water droplets is high; the bulk oil phase has no salt. Even after homogenization, which breaks the oil droplets and disperses the water, local concentration differences persist because some oil-water interface regions were not fully sheared.

Additionally, certain regions of the tank have dead volume: areas where the agitator doesn't reach (corners, near the jacket wall, below the agitator). Salt that enters these dead zones has a very low mixing rate with the bulk batch. If a portion of the batch (e.g., 200 kg) sits in a dead zone for 30 minutes before the agitator's slow circulation brings it back to the bulk, the local concentration in that region may be very different from target.

Another issue: losses to equipment. The production vessel has pipes, pumps, heat exchangers, and a filling machine. Total equipment volume may be 300–500 kg of product. When you hand off the 5,000 kg batch to the filling machine, the first 300 kg to go through the equipment is not representative of the bulk batch—it has a different composition and concentration because it is being pumped from the tank bottom. The last 300 kg is also not representative—it is the remainder left in the equipment, often more concentrated or diluted depending on the ingredient.

**Why It Happens:**
- Batch assembly is sequential, not simultaneous; early ingredients (water) are well-mixed into the batch, but later ingredients (salt added step 6) start in a localized zone
- Dead volume in the tank means some of the batch has very low circulation rate; if an ingredient is added near a dead zone, local concentration is high until circulation brings it to the bulk
- Equipment dead volume (pipes, heat exchanger, pump) concentrates or dilutes the batch; the first pass through contains one concentration, bulk contains target, final pass contains remainder
- Homogenization is not instantaneous; it is a continuous process. Early portions of the batch passing through the homogenizer may have different composition than later portions (if assembly and mixing are still ongoing when homogenization starts)

**Mechanism at Each Scale:**
- **Bench (2 kg, salt added to bulk, mixed 30 sec):** Salt fully dissolved and uniformly distributed. Measured saltiness: 4.0% throughout.

- **Pilot (100 kg, salt added to assembled batch, mixed 5 min before homogenization):** Salt mostly distributed but some local pockets remain (near the salt addition point, in any dead zone). Measured saltiness: 4.0% in bulk, 4.5% near dead zone. Homogenization distributes most of this, final salt ranges 3.9–4.1%.

- **Production (5,000 kg, salt added to assembled batch, mixed 10 min before homogenization):** Salt is in process of distribution. Dead zones hold local high-concentration pockets. Equipment (pipes, heat exchanger, pump, filling machine) has 400 kg dead volume. First 400 kg through filling machine: salt ~5.5% (concentrated from pipes). Middle 4,200 kg through filling machine: salt ~4.0% (target). Last 400 kg: salt ~2.5% (dilute remainder from tank bottom).

**Mitigation:**
1. **Minimize dead volume.** When setting up production, request equipment with minimal dead volume. Use tilting kettles (no bottom sumps), sloped-bottom tanks, and pumps with low internal volumes. Each 100 kg of dead volume is 2% of a 5,000 kg batch—that product may not meet spec.

2. **Optimize ingredient addition sequence.** Add early-stage ingredients (water, base oil) first, allow them to mix thoroughly (5+ minutes), then add critical ingredients (salt, pH adjusters) after the bulk is mixed. This reduces local concentration pockets. Example: instead of adding salt at step 6 (after oil and emulsifier are in), add salt at step 2 (after water is in, before oil is added). The salt will dissolve in the water fully before oil interferes.

3. **Pre-dissolve critical ingredients.** Instead of adding salt as dry crystals, dissolve it in a small amount of water offline first (0.5–1.0 L). Add this salt solution to the batch as a solution, not as dry salt. A solution distributes much faster than dry crystals and avoids local over-saturation.

4. **Standardize mixing time before homogenization.** Allow at least 10 minutes of bulk mixing after the last ingredient is added, before homogenization begins. Document this: "After final ingredient addition, mix batch for 10 minutes at [agitation speed] before transferring to homogenizer." This ensures ingredients are mostly distributed before homogenization starts.

5. **Purge equipment after every batch.** After the batch has exited the equipment (pipes, heat exchanger, filling machine), flush the equipment with water or the next batch's product to clear dead volume. This prevents one batch's remainder from contaminating the next batch. For some products, a 5–10 minute flush with water (or next batch product) at standard flow rate is sufficient.

6. **Sample throughout the batch at filling.** Do not assume the middle 80% of the batch (which likely meets spec) is representative of the entire batch. Sample at the start of fill (first 5 containers), middle (containers 500–510), and end (last 5 containers). Measure salt content for each sampling point. If variation is > 0.3%, investigate equipment dead volume or mixing issues.

7. **Adjust the first and last portions separately.** If equipment dead volume is unavoidable, accept that the first 200–300 kg and last 200–300 kg of the batch will be out of spec. Do not package these portions for sale; recycle them into the next batch. This is expensive but common in contract manufacturing. Document this requirement: "First 300 kg and last 300 kg of each batch are recycled to the next batch; only middle 4,400 kg of each batch is packaged for sale."

**Red Flag:**
If you cannot reduce salt variation to ±0.2% despite these measures, the formulation may require tighter process control than the production facility can provide. Request tighter specification from the supplier, or use a co-packer with better equipment.

---

## Scale-Up Decision Framework

A systematic approach to deciding if a bench formula is ready for pilot, and if a pilot is ready for production.

### Gate 1: Bench to Pilot

**Before proceeding to pilot, a bench formula must meet these criteria:**

1. **Proof of concept:** The formula works as intended. Sensory quality, shelf stability, and functional properties meet or exceed target.

2. **Ingredient consistency:** All ingredients are sourced from the planned production supplier. Do not use lab-grade or specialty-source ingredients at bench if production will use commodity ingredients. (Lecithin from one supplier may perform very differently than lecithin from another.)

3. **Process reproducibility:** The formula can be repeated at bench scale 3 times with ±5% variation in key sensory/functional attributes. If bench results are not reproducible, pilot will be worse.

4. **Shelf stability:** The formula is stable at room temperature for at least 30 days (or your target shelf life). Bench stability does not guarantee production stability, but instability at bench certainly means instability at production.

5. **Ingredient quantities specified with tolerances:** The formula is not just "add some guar gum"—it is "add 0.5% guar gum (by weight of total batch)." Tolerances are documented (e.g., 0.48–0.52% guar gum is acceptable).

6. **Process steps are written with detail:** Not "mix well"; write "mix with magnetic stir bar at 800 RPM for 5 minutes, then add ingredient B slowly over 2 minutes." If you cannot specify the bench process clearly, scaling will be impossible.

7. **No magic:** The formula does not rely on anything that only works at bench (e.g., a specific brand of hotplate, a specific rotor-stator that is not available at pilot scale, or a manual process that cannot be automated). If the formula does, modify it before piloting.

**Go/No-Go Decision:**
- **Go:** Formula is ready for pilot if all 7 criteria are met.
- **No-Go:** Formula needs reformulation or further bench work if any criteria are not met. Do not proceed to pilot.
- **Conditional Go:** Formula is ready for pilot IF certain issues are addressed in the first pilot run (e.g., "We will test two different gums in pilot to determine which one is more forgiving at scale").

### Gate 2: Pilot to Production

**Before proceeding to production, a pilot formula must meet these criteria:**

1. **Successful pilot run(s):** At least one pilot run produced a product that met all sensory, functional, and quality specifications. Ideally, two pilot runs were consistent (±3% variation in key attributes), demonstrating reproducibility.

2. **Scale-up parameters identified:** You have documented the exact process parameters for pilot scale:
   - Mixing speeds (RPM), times (minutes)
   - Heating rate (°C/min), target temperature, come-up time
   - Cooling rate (°C/min), target temperature
   - Addition order and rates (kg/min)
   - Homogenization pressure (bar), passes, and residence time
   - Filling temperature and rate

3. **Key differences from bench identified and understood:** You have documented how pilot differs from bench and why:
   - "Bench guar gum is added dry; pilot guar gum is added as a pre-disperse in oil because [reason: fish-eye problem at pilot scale]"
   - "Bench cooling takes 2 min; pilot cooling takes 8 min due to [reason: surface-area-to-volume difference], and this results in [consequence: softer gel, acceptable]"

4. **Variability is acceptable:** The pilot batch has natural variation from batch to batch (ingredients vary, temperature varies slightly, operator timing varies). This variation is ±5% in key attributes, and the formula is robust to these deviations. If variation is > ±10%, the formula is too knife-edge.

5. **No unresolved scale-up issues:** You have addressed (or have a plan to address) any issues that arose in pilot:
   - Issue: Fish-eyes formed with direct guar addition. Plan: Pre-disperse guar in oil at production.
   - Issue: Foam was visible. Plan: Add defoamer at 0.1% at production.
   - Issue: Cooling was slow, gelatin did not set. Plan: Use faster cooling (plate heat exchanger) at production instead of jacket cooling.

6. **Co-packer is identified and equipment is confirmed:** If using a co-packer, their equipment has been specified and visited. You have confirmed that their equipment can match pilot process conditions. Do not assume a co-packer can match your pilot without visiting and reviewing their equipment.

7. **First production run protocol is written:** You have detailed what will be measured, when, and what constitutes a successful run. (See "First Production Run Protocol" section below.)

**Go/No-Go Decision:**
- **Go:** Formula is ready for production if all 7 criteria are met.
- **No-Go:** Formula needs additional pilot runs, reformulation, or equipment changes if any criteria are not met.
- **Conditional Go:** Formula is ready for first production run IF certain adjustments are made (e.g., "We will use faster cooling as planned").

---

## Scale-Up Documentation Requirements

### Process Specification Sheet

A single document that specifies every parameter of the production process with tolerances.

**Example (Mayonnaise):**

```
MAYONNAISE PRODUCTION PROCESS SPECIFICATION
Product Code: MAY-0001
Batch Size: 5,000 kg
Target pH: 3.8 ± 0.2
Target Viscosity: 2,400 cP (at 20 RPM, after 30 min rest)

ASSEMBLY PHASE
Step 1: Water Addition
  - Temperature: 25 ± 2 °C
  - Amount: 2,500 kg (calculated as [total batch - oil - emulsifier - yolk - vinegar - salt - spices])
  - Addition method: Gravity fed from supply tank
  - Mixing: Agitate at 150 RPM (anchor agitator) during water addition
  - Duration: 5 minutes

Step 2: Oil Addition
  - Temperature: 20 ± 3 °C (oil must be at room temperature or cooler)
  - Amount: 1,750 kg
  - Addition rate: 350 kg/min (controlled via peristaltic pump)
  - Mixing: Maintain agitation at 150 RPM during oil addition
  - Duration: 5 minutes (oil addition time)
  - Note: Oil must be added slowly. Do not exceed 350 kg/min or emulsion will break.

Step 3: Emulsifier Addition
  - Amount: 25 kg (soy lecithin, SUPPLIER: Cargill, LOT: as specified)
  - Addition method: Dry powder via powder induction system (Silverson Pulley system)
  - Pre-dispersion: Lecithin is pre-wetted in 2.5 kg of oil before powder addition
  - Mixing: Maintain agitation at 150 RPM during addition
  - Duration: 3 minutes
  - Note: Lecithin must be pre-wetted or fish-eyes will form.

Step 4: Egg Yolk Addition
  - Amount: 500 kg (pasteurized liquid egg yolk, SUPPLIER: Egg Products Inc, LOT: as specified)
  - Temperature: 20 ± 3 °C
  - Addition rate: 100 kg/min (controlled via peristaltic pump)
  - Mixing: Maintain agitation at 150 RPM during addition
  - Duration: 5 minutes
  - Note: Yolk must be added slowly to avoid over-shearing and emulsion breaking.

Step 5: Vinegar Addition
  - Amount: 100 kg (5% acetic acid distilled vinegar)
  - Temperature: 25 ± 2 °C
  - Addition rate: 50 kg/min (controlled via peristaltic pump)
  - Mixing: Maintain agitation at 150 RPM during addition
  - Duration: 2 minutes
  - Note: Vinegar is added after emulsion is formed to avoid breaking.

Step 6: Salt & Preservative Addition
  - Salt: 80 kg (sodium chloride, food grade)
  - Preservative: 5 kg (sodium benzoate, 1% of batch)
  - Pre-dissolution: Both are dissolved in 100 kg of water (heated to 40 °C) offline, mixed, and cooled to 25 °C
  - Addition: The salt/preservative solution is added to the batch via gravity
  - Addition rate: 100 kg/min
  - Mixing: Maintain agitation at 150 RPM during addition
  - Duration: 1 minute
  - Note: Salt must be pre-dissolved to ensure uniform distribution.

Step 7: Spices
  - Amount: 45 kg (spice blend: [itemize each spice and % of blend])
  - Pre-mixing: Spices are dry-blended offline before addition
  - Addition: Added as a dry blend via funnel with gentle agitation
  - Mixing: Maintain agitation at 150 RPM for 2 minutes after spice addition
  - Duration: 0.5 minutes addition + 2 minutes mixing
  - Note: Spices must be dry-blended to ensure even distribution.

POST-ASSEMBLY MIXING
  - Duration: 10 minutes minimum
  - Agitation: 150 RPM (anchor agitator)
  - Purpose: Ensure all ingredients are uniformly distributed before homogenization
  - Quality check: Sample the batch at 5 minutes and again at 10 minutes for visual inspection (no streaks, uniform color)

HOMOGENIZATION
  - Equipment: High-pressure homogenizer (Rannie Panda, 5 kW)
  - Pressure: 400 bar
  - Number of passes: 2
  - Flow rate: 100 kg/min (5,000 kg batch requires ~50 minutes of homogenization)
  - Inlet temperature: 25 ± 2 °C
  - Outlet temperature: Expected 28 ± 2 °C (rise due to adiabatic compression)
  - Target droplet size: 2–4 microns (measured via laser diffraction on sample)

HOLDING
  - Post-homogenization: Batch goes to holding tank (temperature controlled to 20 °C via jacketed cooling)
  - Duration: 30 minutes minimum before measurement or filling
  - Purpose: Allow viscosity recovery in shear-thinned system

QUALITY CHECKS (During assembly and holding)
  - pH: Measured at 30 minutes post-assembly, target 3.8 ± 0.2 (calibrated pH meter, 3-point calibration)
  - Viscosity: Measured at 30 minutes post-homogenization, target 2,400 cP ± 200 cP (Brookfield viscometer, 20 RPM, T-spindle)
  - Droplet size: Measured from homogenized sample via laser diffraction, target 2–4 microns
  - Appearance: Visual inspection, target: uniform color, no streaks, no visible foam, no grittiness
  - Microbial: Post-production grab sample sent to QC lab for plate count and pathogen testing (results required before release)

FILLING
  - Temperature at fill: 20 ± 2 °C (chilled holding tank maintains this)
  - Fill method: Volumetric filler (Serac, 1.0 L cups)
  - Fill speed: 200 containers/min
  - Net weight check: Random inspection of filled containers on check-weigher, target ±2% of target fill weight
  - Batch tracking: Each filled container is labeled with batch number, production date, and expiration date
```

This level of detail is typical for a production specification sheet. It ensures every operator, every time, follows the same process.

### Critical-to-Quality (CTQ) Parameters

List the parameters that must be controlled precisely vs. parameters that can vary within tolerance.

**Example (Mayonnaise):**

| Parameter | CTQ? | Target | Tolerance | Reason |
|-----------|------|--------|-----------|--------|
| Oil addition rate | YES | 350 kg/min | ±50 kg/min (300–400 kg/min) | If too fast, emulsion breaks |
| Agitation RPM (during assembly) | YES | 150 | ±20 RPM (130–170 RPM) | If too slow, mixing is inadequate; if too fast, emulsion over-shears |
| Salt pre-dissolution | YES | Required | Must be done | If added dry, local over-salting occurs |
| Homogenization pressure | YES | 400 bar | ±25 bar (375–425 bar) | Controls droplet size; if too low, droplets are large; if too high, over-processing |
| Post-homogenization holding time | YES | 30 min | ±10 min (20–40 min) | Viscosity recovery requires time; if too short, viscosity is low |
| Vinegar addition rate | YES | 50 kg/min | ±20 kg/min (30–70 kg/min) | If too fast, local pH shock may cause emulsion break |
| Spice blend uniformity | YES | Required | Dry blend before addition | If added individually, risk of uneven distribution |
| Water temperature (initial) | NO | 25 °C | ±5 °C (20–30 °C) | Small effect on final viscosity; not critical |
| Spice amount | NO | 45 kg | ±0.5 kg (44.5–45.5 kg) | Flavor variation is minimal at this tolerance; not critical |
| Filling temperature | NO | 20 °C | ±3 °C (17–23 °C) | Small effect on fill accuracy; not critical |

The CTQ parameters (YES) are the ones you monitor closely. The non-CTQ parameters (NO) can vary without triggering intervention.

### Process Flow Diagram

A visual step-by-step representation of the process with equipment, temperatures, times, and decision points.

A simple text-based flow diagram for mayonnaise might be:

```
[Water Tank (25°C)]
  |
  ↓ Gravity feed
[Production Kettle] → Agitate at 150 RPM
  |
  ↓ (5 min)
[Oil Pump (20°C)]
  |
  ↓ Peristaltic, 350 kg/min
[Production Kettle] → Agitate at 150 RPM, oil integrates (5 min)
  |
  ↓ (Oil is added)
[Silverson Powder Induction] → Lecithin (pre-wetted in oil)
  |
  ↓ (3 min)
[Production Kettle] → Agitate at 150 RPM (3 min)
  |
  ↓ (Lecithin integrated)
[Egg Yolk Pump (20°C)]
  |
  ↓ Peristaltic, 100 kg/min
[Production Kettle] → Agitate at 150 RPM, yolk integrates (5 min)
  |
  ↓ (Yolk is added)
[Vinegar Pump (25°C)]
  |
  ↓ Peristaltic, 50 kg/min
[Production Kettle] → Agitate at 150 RPM, vinegar integrates (2 min)
  |
  ↓ (Vinegar added)
[Salt/Preservative Solution Tank (25°C)]
  |
  ↓ Gravity feed
[Production Kettle] → Agitate at 150 RPM, solution integrates (1 min)
  |
  ↓ (Salt/pres. added)
[Spice Blend (dry)]
  |
  ↓ Funnel + gravity
[Production Kettle] → Agitate at 150 RPM (2 min)
  |
  ↓ (Spices integrated)
[Post-Assembly Mixing] → Agitate at 150 RPM for 10 min (quality check at 5 min and 10 min)
  |
  ↓ (All ingredients integrated)
[High-Pressure Homogenizer (Rannie Panda)] → 400 bar, 2 passes, 100 kg/min, inlet 25°C
  |
  ↓ (~50 min total homogenization time)
[Holding Tank (chilled to 20°C)]
  |
  ↓ (30 min hold, quality checks: pH, viscosity, droplet size, appearance, microbial sample)
[Volumetric Filler (Serac)]
  |
  ↓ (200 containers/min, target 1.0 L, ±2%)
[Check-Weigher]
  |
  ↓ (Pass/Fail inspection)
[Capping Machine]
  |
  ↓
[Labeling]
  |
  ↓
[Case Packing & Shipping]
```

A formal flow diagram (PFD) would include equipment symbols, temperature/pressure annotations, and hold points.

### First Production Run Protocol

A detailed plan for the first production run and how to determine if it was successful.

---

## First Production Run Protocol

**Objective:** Produce a batch of [Product Name] at production scale and determine if the formula and process are ready for commercial release, or if adjustments are needed before commercial manufacture.

**Batch Details:**
- Product: [Product Name]
- Batch Size: [XX] kg
- Target: [Sensory Description, Functional Performance]
- Success Criteria: [Listed below]
- Date: [Date of Run]
- Team: [Names and roles of personnel present]

**Pre-Run Preparation:**

1. **Equipment Check:** All equipment is calibrated and functioning. Thermometers, pH meter, viscometer, balances are all calibrated within the past 30 days. Documentation is provided.

2. **Ingredient Staging:** All ingredients are staged at the production facility, in their specified storage conditions, with certificates of analysis provided. No substitutions without approval from Product Development.

3. **Procedure Review:** All personnel review the Process Specification Sheet (above) and understand their role.

4. **Sampling Plan:** Sample bottles and labels are prepared. Sampling times and locations are identified on the Process Flow Diagram.

**Run Protocol:**

**Phase 1: Setup and Assembly (T = 0 to T = 25 minutes)**
- T = 0: Production kettle is charged with water (2,500 kg, 25 °C). Agitation starts at 150 RPM.
- T = 5: Oil addition begins at 350 kg/min. Temperature and RPM are continuously monitored.
- T = 10: Oil addition is complete. Batch is mixed for 5 minutes.
- T = 15: Lecithin (pre-wetted) is added via powder induction. Mixing continues at 150 RPM.
- T = 18: Egg yolk addition begins at 100 kg/min.
- T = 23: Egg yolk addition is complete. Batch is mixed for 2 minutes.
- T = 25: Vinegar addition begins.

**Quality Check 1 (T = 15, oil integration phase):**
- Sample 200 mL from the production kettle.
- Visual inspection: Is the mixture uniform in color and consistency? Any streaks or unmixed zones? Record observations.
- Measurement: Temperature (should be ~25–26 °C). Record.

**Phase 2: Vinegar to Salt Addition (T = 25 to T = 30 minutes)**
- T = 25: Vinegar addition at 50 kg/min. Temperature monitored.
- T = 27: Vinegar addition complete.
- T = 27 to T = 29: Batch is mixed at 150 RPM.
- T = 29: Salt/preservative solution is added at 100 kg/min.
- T = 30: Salt/preservative addition is complete.

**Quality Check 2 (T = 30, post-salt addition):**
- Sample 200 mL from the production kettle.
- Visual inspection: Color and uniformity? Grittiness (indicating undissolved salt)?
- Measurement: pH (using calibrated pH meter, 3-point calibration, should be 3.8 ± 0.2). Record.
- Measurement: Temperature (should be ~25–26 °C).

**Phase 3: Spices to Post-Assembly Mixing (T = 30 to T = 40 minutes)**
- T = 30: Spice blend addition.
- T = 30.5: Spice addition complete.
- T = 30.5 to T = 40: Post-assembly mixing at 150 RPM (10 minutes).

**Quality Check 3 (T = 35, mid-mix point):**
- Sample 200 mL from the production kettle.
- Visual inspection: Spices uniformly distributed? No streaks?
- Record observations.

**Quality Check 4 (T = 40, post-assembly mixing):**
- Sample 300 mL from the production kettle.
- Visual inspection: Color uniform, texture smooth, no foam, no grittiness.
- pH: Target 3.8 ± 0.2. If pH is out of range, investigate (ingredient lot change? pH meter calibration?). Decision point: Is pH acceptable? If no, stop batch and investigate. If yes, proceed to homogenization.
- Temperature: Should be ~25–26 °C.

**Phase 4: Homogenization (T = 40 to T = 90 minutes)**
- T = 40: Batch is transferred to the high-pressure homogenizer (Rannie Panda).
- Homogenization parameters: 400 bar, 2 passes, 100 kg/min flow rate, inlet temperature 25 °C (monitored continuously).
- Outlet temperature monitored: Expected rise to 28 ± 2 °C (adiabatic compression).
- Duration: ~50 minutes (5,000 kg ÷ 100 kg/min).

**Quality Check 5 (T = 60, mid-homogenization):**
- Sample 50 mL from homogenizer outlet (allow to cool to room temperature before measurement).
- Droplet size (laser diffraction): Target 2–4 microns. If droplet size is outside range, note the deviation. Do not stop unless size is >10 microns (over-processing) or <1 micron (likely measurement error). Proceed to holding.
- Record observations.

**Quality Check 6 (T = 90, post-homogenization):**
- Homogenization is complete. Batch is transferred to holding tank (jacketed, chilled to 20 °C).
- Sample 500 mL is collected in a sterile container and immediately transferred to the QC lab for microbial testing (plate count, pathogen screen). This sample will not be packaged.
- Sample 300 mL is collected for viscosity and droplet size measurement 30 minutes later (see below).

**Phase 5: Holding and Final Quality Check (T = 90 to T = 120 minutes)**
- T = 90 to T = 120: Batch remains in holding tank at 20 ± 1 °C. Agitation is off (quiescent hold).

**Quality Check 7 (T = 120, post-holding):**
- Batch has now been held for 30 minutes (recovery period for viscosity development).
- Sample 300 mL collected earlier is now measured.
- Viscosity (Brookfield, 20 RPM, T-spindle): Target 2,400 cP ± 200 cP (i.e., 2,200–2,600 cP).
  - If viscosity is in range, note and proceed to filling.
  - If viscosity is low (< 2,200 cP), investigate: Was homogenization too intense? Was holding time too short? Is the batch temperature above 20 °C? Make note for future runs.
  - If viscosity is high (> 2,600 cP), investigate: Was homogenization insufficient? Is the batch temperature below 20 °C? Make note.
  - Decision point: Is viscosity in acceptable range ±5% (i.e., 2,280–2,600 cP, allowing for some variation)? If yes, proceed. If no, hold batch pending review by Product Development.
- pH (re-check): Target 3.8 ± 0.2. If pH has drifted since Quality Check 4, note the drift and investigate.
- Appearance: Visual inspection of the 300 mL sample. Is the product uniform in color? Any foam, grittiness, or separation? Record observations.
- Droplet size (re-check, if available): Target 2–4 microns. Record.

**Phase 6: Filling (T = 120 onward)**
- T = 120: Batch is transferred to the volumetric filler (Serac).
- Fill parameters: Target 1.0 L per container, ±2% (i.e., 980–1,020 mL per container).
- Fill speed: 200 containers/min.
- Duration: 5,000 kg ÷ 1.0 kg per container = 5,000 containers, ÷ 200 containers/min = 25 minutes.

**Quality Check 8 (Start of filling, containers 1–5):**
- Collect the first 5 containers filled.
- Measure net weight of each container: Target [XX] grams ± 2%. Expected range: [XX–XX] grams.
- Visual inspection: Headspace, color, appearance. Record any issues.

**Quality Check 9 (Mid-filling, containers 2,500–2,505):**
- Collect 5 containers from the middle of the fill run.
- Measure net weight: Target ± 2%.
- Visual inspection: Consistent with check 8? Any drift in color or appearance?

**Quality Check 10 (End of filling, containers 4,995–5,000):**
- Collect the last 5 containers filled.
- Measure net weight: Target ± 2%.
- Visual inspection: Consistent with earlier checks? Any change in headspace or color?

**Phase 7: Cooling and Storage (Post-filling)**
- Filled containers are transferred to a cool storage area (20–25 °C ambient).
- No accelerated shelf-life testing is performed during the first run (shelf stability is assumed based on bench and pilot data).

**Success Criteria & Go/No-Go Decision:**

The production run is deemed **SUCCESSFUL** and commercial manufacture can proceed if ALL of the following criteria are met:

1. **pH:** Target 3.8 ± 0.2. Range 3.6–4.0.
2. **Viscosity:** Target 2,400 cP ± 200 cP. Range 2,200–2,600 cP.
3. **Droplet size:** Target 2–4 microns. Range 1.5–5.0 microns.
4. **Appearance:** Uniform color, no foam, no grittiness, no separation. Consistent across all quality checks.
5. **Fill weight accuracy:** All filled containers within ±3% of target (allowing for some check-weigher variation).
6. **Microbial:** Grab sample submitted for testing; results pending (release on approval of lab results).
7. **Batch assembly time:** Total time from water addition to post-assembly mixing (T = 40 minutes) is within expectations. If longer than 50 minutes, investigate causes and document for future runs.
8. **Homogenization time:** Total time is ~50 minutes (5,000 kg ÷ 100 kg/min). If significantly longer, pressure may be dropping; inspect equipment post-run.
9. **No unplanned stops or equipment issues:** The entire run proceeds without unplanned stops, equipment failures, or safety incidents.

The production run is deemed **CONDITIONAL** if:
- One parameter is slightly out of target (e.g., viscosity 2,150 cP, pH 4.1) but within ±10% tolerance
- An unplanned stop occurred, but the batch recovered normally
- A minor equipment adjustment was needed (e.g., agitator RPM was reduced slightly to 145 RPM)

In a CONDITIONAL case, the batch may be commercially released but is flagged for close monitoring (enhanced QC sampling in the next 1–2 batches).

The production run is deemed **UNSUCCESSFUL** and commercial manufacture must be held if:
- Any parameter is out of specification by > ±10% (e.g., pH < 3.5 or > 4.2, viscosity < 2,100 cP or > 2,800 cP)
- Appearance is unacceptable (visible foam, grittiness, or separation that cannot be explained)
- An unplanned equipment failure occurred
- Microbial results show contamination above acceptable limits
- A process parameter deviated significantly from specification and could not be corrected (e.g., agitator failed, temperature control failed, homogenizer pressure dropped to 300 bar and could not be recovered)

In an UNSUCCESSFUL case, the batch is held pending investigation. Product Development reviews all data and determines:
- Is the process specification correct, or must it be revised?
- Is the equipment suitable, or must a different co-packer be used?
- Is the formula sound, or must it be reformulated?

A second production run is scheduled after adjustments are made.

---

## Co-Packer Considerations

If manufacturing is outsourced to a contract manufacturer (co-packer), additional considerations arise.

### What to Provide to the Co-Packer

1. **Process Specification Sheet:** Provide the detailed specification (as above) with every parameter and tolerance.

2. **Ingredient Specifications:** For each ingredient, provide:
   - Supplier name and part number
   - Particle size (if relevant), color, moisture content, and any other key specs
   - Certificate of analysis from the supplier (if available)
   - Any restrictions (non-GMO, organic, allergen-free, etc.)

3. **Quality Control Parameters:** Specify what you will test and what you expect the co-packer to test:
   - You will test: pH, viscosity, droplet size, sensory, shelf stability (accelerated or real-time)
   - Co-packer will test: Fill weight, appearance, microbial (if required by regulation)

4. **Regulatory Documentation (if applicable):**
   - Food Safety Modernization Act (FSMA) compliance (if U.S. product)
   - S-Letter (written statement) from the co-packer confirming equipment is appropriate for your product type (e.g., allergen-free, no cross-contamination with prior products)
   - Cleaning procedure and validation (to ensure no contamination from prior products)

5. **First Production Run Protocol:** Provide the detailed protocol (above) so the co-packer knows exactly what you expect to measure and what constitutes success.

6. **Shelf Life & Stability Testing Plan:** Specify:
   - Target shelf life (e.g., 12 months at room temperature, 2 years frozen)
   - Stability testing plan (e.g., monthly pH and viscosity checks for 3 months; quarterly sensory checks for 12 months)
   - Who performs testing (you or co-packer)

### What to Expect from the Co-Packer

1. **Equipment Availability:** The co-packer confirms they have equipment that matches your process specification. Do not assume. Visit their facility, see the equipment, confirm they can achieve the required mixing speeds, heating/cooling rates, and homogenization pressures.

2. **Changeover Time:** Understand the co-packer's changeover procedure. If they previously made peanut butter, how do they clean the equipment to ensure no peanut contamination in your product? How long does changeover take (this affects your batch scheduling and cost)?

3. **Minimum Batch Size:** Co-packers often have a minimum batch size (e.g., they cannot make batches smaller than 500 kg). Confirm their minimum matches your needs. If you want to make 100 kg batches and they have a 500 kg minimum, either adjust your batch size or change co-packers.

4. **First Run Yield:** Expect the first production run to have some losses:
   - Dead volume in pipes and equipment (~300–400 kg for a 5,000 kg batch)
   - Startup sampling (first 100 kg may be used for quality checks and discarded)
   - Cleanup and line conditioning (product used to stabilize the fill line before commercial containers are filled)
   - Total loss: ~10–15% of the batch. Plan for this. If you need 5,000 kg of finished product, order a 5,750 kg production run.

5. **Ingredient Shelf Life:** Confirm the co-packer can store your ingredients under the correct conditions (refrigerated, frozen, dry, cool, dark). If you require 25 kg of soy lecithin and the co-packer's supplier ships 500 kg drums, you need to discuss shared storage or accept that you are paying for more ingredient than you need.

6. **Schedule and Lead Time:** Co-packers often have lead times of 4–8 weeks depending on their schedule. Plan accordingly. Do not expect to schedule a production run on short notice.

7. **Cost and Minimum Commitment:** Confirm the cost per kilogram and any minimum monthly or annual commitment. Some co-packers require a minimum annual order (e.g., minimum 50,000 kg per year).

### Common Co-Packer Issues and Mitigation

1. **Equipment Differences:** The co-packer's equipment differs from your pilot equipment (e.g., they use a rotor-stator instead of high-pressure homogenizer). This affects your product (different droplet size, different viscosity).
   - *Mitigation:* Visit the facility before signing. Run a trial batch if possible. Adjust your formulation for their equipment.

2. **Ingredient Substitution:** The co-packer substitutes an ingredient (e.g., soy lecithin from a different supplier) without informing you.
   - *Mitigation:* Include a clause in the contract: "No ingredient substitutions without written approval from [Your Company]. Any substitution requires re-testing and approval before production."

3. **Batch-to-Batch Inconsistency:** Successive batches vary significantly (one batch is pH 3.8, the next is pH 4.2).
   - *Mitigation:* Ensure the co-packer is following your process specification exactly. Request a facility audit if inconsistency persists. Consider changing co-packers if the issue cannot be resolved.

4. **Communication Delays:** You submit a corrective action request (e.g., "Next batch, add 0.1% defoamer at the end of mixing"), but the co-packer doesn't implement it until 3 batches later.
   - *Mitigation:* Establish a clear communication protocol. All process changes must be submitted in writing and confirmed in writing before the next batch.

5. **Microbial or Safety Issues:** The co-packer's facility or process allows contamination (e.g., pathogen detected in a batch). This is a serious issue.
   - *Mitigation:* Contract with a co-packer that has FSMA compliance or SQF certification. Conduct facility audits at least annually. If contamination occurs, halt production, conduct a full investigation, and consider changing co-packers.

6. **Payment and Ordering:** You place an order for 10,000 kg, and the co-packer produces 10,000 kg, but invoices you for 10,500 kg (claiming 5% waste).
   - *Mitigation:* Establish clear terms in the contract: "You will be invoiced for actual product delivered, plus agreed-upon waste allowance (e.g., 3%, included in price)."

---

## Troubleshooting at Scale

### Quick Reference: Common Problems and Solutions

| Problem | Bench Behavior | Pilot/Production Behavior | Probable Cause | First Check | Solution |
|---------|---|---|---|---|---|
| Fish-eyes in final product | None | Visible small gelled particles | Hydrocolloid not fully dispersed due to low local shear | Pre-disperse hydrocolloid in oil or other phase before adding to batch | Add hydrocolloid as pre-mix; use high-shear step; pre-disperse before bulk mixing |
| Dark color (over-browned) | Light brown, target color | Dark brown, almost burnt | Long heating time at elevated temperature | Heating time at production; did it exceed bench by 2× or more? | Lower target temp by 2–5 °C; use faster heating method (plate HX) |
| Foam visible in filled container | No foam | Significant foam layer | Air incorporation during mixing and during long process residence time | Was the batch mixed for longer than bench? Was defoamer used? | Add defoamer (0.1–0.2%); use post-defoaming hold to allow bubbles to rise |
| Product too thin (low viscosity) | Target viscosity | 20% lower viscosity | Shear-thinning polymer (xanthan, guar) not recovering; or finer emulsion from different homogenization method | Homogenization method different from bench? Post-homogenization hold time adequate (30 min)? | Increase thickener level; allow longer post-homogenization hold; use faster cooling |
| Grittiness (salt crystals visible) | Smooth texture | Sandy, gritty texture | Undissolved salt crystals; salt added dry and not fully dissolving at production temperature | Was salt added as dry crystals or as solution? | Always add salt as pre-dissolved solution (not dry); allow adequate mixing time |
| Separation or syneresis (whey/oil leakage) | Stable (no separation) | Visible liquid weeping from product | Slow cooling allows water migration and coalescence; or gelatin gel network too weak | Did cooling take much longer at production? Is cooling via slow jacket (vs. plate HX)? | Use faster cooling (plate HX); increase gelatin level; reformulate |
| pH different from bench | pH 3.8 | pH 4.2 (higher, less acidic) | Longer mixing time means longer time for acid to be buffered by ingredients; or CO2 loss via deaeration | Did mixing time extend? Did defoaming/vacuum deaeration occur? | Use pre-dissolved acid; account for buffering in formulation; measure pH after full equilibration (30 min post-mixing) |
| Emulsion breaking / curdling | Stable emulsion | Separated into oil and water layers | Oil added too fast; over-mixing after emulsifier; or temperature drop during cooling breaking emulsion | Was oil addition rate too high (> target rate)? | Slow oil addition; reduce agitation speed during assembly; maintain temperature during cooling; re-homogenize if broken |
| Non-uniform color (streaks, patches) | Uniform color | Color variation in batch | Uneven ingredient distribution due to dead zones or inadequate mixing time | Was mixing time adequate after final ingredient addition? Are there dead zones visible in the tank? | Extend post-assembly mixing time; increase agitation speed; consider redesigning tank (sloped bottom) |
| Filling line running slow | Fills at target speed | Filling speed 30% slower than target | Product viscosity lower than expected, or fill line conditions different (temperature) | Was viscosity measured? Is fill line temperature lower at production (product is thicker when cold)? | Re-evaluate viscosity; warm product slightly before filling (if feasible); increase thickener level |

---

## References and Further Reading

### Books
- **Moran, B.** (2008). *Food Chemistry Reference Series: Volume 1 — Formulation Essentials*. Practical approaches to scaling food formulations.
- **Singh, R. P., & Heldman, D. R.** (2014). *Introduction to Food Engineering* (5th ed.). Academic Press. Covers heat transfer, mixing, and unit operations at various scales.
- **Toledo, R. T.** (2007). *Fundamentals of Food Process Engineering* (3rd ed.). Springer Science+Business Media. Detailed treatment of process equipment and scale-up.

### Articles & Standards
- **FDA FSMA** (Food Safety Modernization Act). Guidance on process validation and verification for food manufacturers.
- **NFPA** (National Fluid Power Association). Standards for equipment reliability and maintenance.
- **ISO 9001:2015**. Quality Management Systems — relevant for documenting and controlling formulation changes.

### Industry Organizations
- **Institute of Food Technologists (IFT)**. Publishes technical papers on food formulation, scale-up, and processing.
- **American Society of Agricultural and Biological Engineers (ASABE)**. Standards and research on food process equipment.

### Online Resources
- **SQF Code** (Safe Quality Food). Certification standard for food safety management; many co-packers use this.
- **HACCP Principles**. Hazard Analysis Critical Control Points; framework for identifying and controlling critical process steps.

---

## Appendix: Example Scale-Up Adjustment Log

| Date | Batch # | Scale | Parameter | Change | Reason | Result |
|------|---------|-------|-----------|--------|--------|--------|
| Jan 15 | MAY-001 | Bench | Guar gum form | Dry powder | Control experiment | Fish-eyes formed; not acceptable |
| Jan 15 | MAY-002 | Bench | Guar gum form | Pre-dispersed in oil | Test mitigation | No fish-eyes; texture smooth |
| Jan 22 | MAY-P-001 | Pilot | Guar gum form | Pre-dispersed in oil | Bench result worked | No fish-eyes; texture smooth; viscosity 2,400 cP |
| Jan 22 | MAY-P-001 | Pilot | Cooling method | Jacket cooling (slow) | Default | Gelatin set incomplete; slight weeping |
| Jan 29 | MAY-P-002 | Pilot | Cooling method | Plate HX (fast) | Address weeping | Gelatin set firm; no weeping; product acceptable |
| Feb 5 | MAY-Prod-001 | Production | Guar gum form | Pre-dispersed in oil | Successful pilot | No fish-eyes; texture smooth |
| Feb 5 | MAY-Prod-001 | Production | Cooling method | Plate HX | Successful pilot | Gelatin set firm; product acceptable |
| Feb 5 | MAY-Prod-001 | Production | Defoamer | 0.1% silicone defoamer added after mixing | Foam observed in assembly | Foam reduced; acceptable level |
| Feb 12 | MAY-Prod-002 | Production | Defoamer | 0.1% silicone defoamer | Confirmed from run 1 | Foam minimal; consistent with run 1 |
| Feb 12 | MAY-Prod-002 | Production | Salt addition | Changed to pre-dissolved solution | Improve uniformity | No grittiness; pH uniform across batch |

---

## Final Notes

Scaling a food formulation is a process of translation, learning, and controlled risk-taking. The bench formula is a proof of concept. The pilot formula is a test of feasibility at near-production conditions. The first production run is the true test—and it will surprise you.

Plan for 3–5 pilot runs and 3–5 commissioning production runs before commercial release. Document every deviation, every observation, and every adjustment. Build that data into your process specification and quality control procedures. Treat it as institutional memory.

When something fails at scale, ask not "What went wrong?" but "What was different?" The answer usually lies in heat transfer, mixing, residence time, shear, or ingredient interaction—all of which change with scale.

Finally, remember that your co-packer is your partner. Provide them with clear specifications, reasonable expectations, and regular communication. A good relationship with a reliable co-packer is worth far more than the savings from shopping around to the cheapest supplier.

Good luck.

---

**Document Version:** 1.0
**Last Updated:** [Date]
**Author:** [Name, Title]
**Approved By:** [Name, Title]

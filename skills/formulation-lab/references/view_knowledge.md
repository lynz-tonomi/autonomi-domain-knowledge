# Formulation Lab — View Knowledge (What Each Tab Does)

## INTEGRATIONS (M365/GWS)
Dual-platform integration hub with toggle switch. M365 has 8 tabs (Outlook, SharePoint, OneDrive, Teams, Excel Online, Calendar, Entra ID, Graph API). GWS has 8 tabs (Gmail, Drive, Sheets, Docs, Calendar, Meet, Chat, OAuth). Each tab shows connection cards with status, stats bar, quick actions, activity log. Full CRUD: add/edit/test/delete connections per service.

## CLIENTS (Workspace)
Multi-client project management. 4 clients: Sunburst Beverages, Kultcha Wellness, Tidewater Naturals, Meadow Gold Dairy Alt. Drill down: Client → Projects → Recipes. Full CRUD: create/edit/delete clients and projects.

## INGREDIENTS & SUPPLIERS
25 ingredients, 10 suppliers across 5 sub-tabs. Full CRUD on all tabs. Ingredients: searchable table with add/edit/delete/view. Suppliers: directory with add/edit/delete/view. Pricing: add price entries. Allergen Matrix: Top 9 overview. Specs Database: quality parameters per ingredient.

## FORMULA BUILDER
Core formulation view with ingredient %, lbs/batch, $/unit, run cost. KPI row, allergen strip, spec strip. CRUD: add/remove ingredients, edit recipe details.

## TRIAL LOG
Bench trial history with spec validation (Brix, pH, Visc, Temp) + 5-axis sensory (sweet, acid, mouthfeel, aroma, color). Quick-entry bar. CRUD: log/edit/delete trials.

## ANALYTICS
4 auto-generated charts from trial data — Brix trend, pH trend, Viscosity trend, Sensory radar.

## SCALE-UP
Bench → Pilot → Production calculator. Expand cards for BOM at scale, process params, equipment, specs. CRUD: edit scale params, set custom batch size via openCustomScale().

## VERSIONS
Formula change log with version #, date, author, diffs. CRUD: log version (openAddVersion), edit version, delete version.

## ALLERGENS
Full Top 9 allergen matrix for current recipe ingredients.

## SPEC TARGETS
Brix/pH/Visc/Temp windows vs last trial. IN SPEC/OUT badges. CRUD: edit all spec windows via openEditSpecs().

## STAGE-GATE
Gate 0-4 pipeline with deliverable checklists, kill criteria, status. CRUD: advance gate (advanceGate), toggle deliverables, add custom deliverables.

## TIMELINE
Project phases with week ranges, FTE, descriptions. Varies by project type. CRUD: toggle phases, add/delete custom milestones.

## RISK REGISTER
Risk entries with probability, impact, timeline, mitigation. CRUD: add/edit/delete risks.

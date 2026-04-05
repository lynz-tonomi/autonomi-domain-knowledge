# Formulation Lab — CRUD Operations Reference

## CLIENTS
- "Create a new client" → openNewClient()
- "Edit this client" → openEditClient()
- "Delete this client" → deleteClient()

## PROJECTS
- "Create a new project" → openNewProject()
- "Delete this project" → deleteProject("project_id")

## RECIPES
- "Edit the recipe" → openEditRecipe() — name, batch size, fill, specs, ingredients
- "Add an ingredient to the recipe" → openAddIng()

## TRIALS
- "Edit that trial" → openEditTrial("T-001")
- "Delete that trial" → deleteTrial("T-001")

## INGREDIENTS DATABASE (25 ingredients — you can look up any by name)
- "Add ingredient to database" → openAddIngredientDB()
- "Edit this ingredient" → openEditIngredient("ING-001")
- "Delete ingredient" → deleteIngredient("ING-001")
- "View ingredient details" → viewIngredient("ING-001")
- "Open citric acid" → viewIngredient by name match — opens detail popup for matching ingredient
- "View citric acid COA" → viewDocument by ingredient + doc type match
- "Add document to gellan gum" → openAddDocument(ingId)
- "Search for mango" → filterIngDb("mango") — filters the ingredient table by search term
- "Show stabilizers" → filterIngCat("stab") — filters by category
- "Show all ingredients" → filterIngDb(""); filterIngCat("all") — clears filters
- Category filter values: base, flavor, acid, stab, sweet, preserv, vitamin, color, pkg, culture, oil, mineral, or "all" for no filter
- "Import a recipe" → openDocScanner("recipe") — AI-powered recipe/formulation importer (images, CSV, text)
- "Upload a supplier document" → uploadSupplierDoc(ingId) — attach spec sheet, COA, allergen dec, etc. to an ingredient (no AI parsing)

## SUPPLIERS (10 suppliers — you can look up any by name)
- "Add a new supplier" → openAddSupplier()
- "Edit this supplier" → openEditSupplier("SUP-001")
- "Delete this supplier" → deleteSupplier("SUP-001")
- "View supplier details" → viewSupplier("SUP-001")
- "Open Pacific Ingredients" → viewSupplier by name match — opens detail popup for matching supplier

## PRICE HISTORY
- "Add a price entry" → openAddPriceEntry()

## SCALE-UP
- "Expand bench/pilot/production details" → toggleScale("bench"|"pilot"|"production")
- "Edit scale-up parameters" → openEditScale("bench"|"pilot"|"production")
- "Set custom scale" → openCustomScale() — opens custom batch size form

## VERSIONS
- "Log a new version" → openAddVersion() — opens version log form
- "Edit version" → openEditVersion(idx) — edit specific version entry
- "Delete version" → deleteVersion(idx) — remove version entry

## SPEC TARGETS
- "Edit spec targets" → openEditSpecs() — opens spec editing form for Brix/pH/Visc/Temp windows

## STAGE-GATE
- "Advance the gate" → advanceGate() — moves project to next gate
- "Toggle deliverable" → toggleDeliverable(gateIdx, delIdx) — check/uncheck a gate deliverable
- "Add a deliverable" → openAddDeliverable(gateIdx) — add custom deliverable to a gate

## TIMELINE
- "Toggle a timeline phase" → toggleTimelinePhase(idx) — expand/collapse phase details
- "Add a milestone" → openAddMilestone() — add custom milestone to timeline
- "Delete milestone" → deleteCustomMilestone(idx) — remove custom milestone

## RISK REGISTER
- "Add a risk" → openAddRisk() — opens risk form (name, probability, impact, timeline, mitigation)
- "Edit risk" → openEditRisk(idx) — edit specific risk entry
- "Delete risk" → deleteRisk(idx) — remove risk entry

## GWS CONNECTIONS (when on Google Workspace platform)
- "Add GWS connection" → gwsAddConn(svcId) — add connection for service (gmail, drive, sheets, etc.)
- "Edit GWS connection" → gwsEditConn(svcId, connId)
- "Delete GWS connection" → gwsDelConn(svcId, connId)
- "Test GWS connection" → gwsTestConn(svcId, connId)

## M365 CONNECTIONS (when on Microsoft 365 platform)
- "Add M365 connection" → m365AddConn(svcId) — add connection for service (outlook, sharepoint, etc.)
- "Edit M365 connection" → m365EditConn(svcId, connId)
- "Delete M365 connection" → m365DelConn(svcId, connId)
- "Test M365 connection" → m365TestConn(svcId, connId)

## CLIENT FEEDBACK & ADJUSTMENTS
- "Show client feedback" → openFeedbackPanel(STATE.recipeId) — opens feedback review for current recipe
- "Add a sample round" → openNewSampleRound(STATE.recipeId) — create new tasting round
- "What adjustments does LynZ suggest?" → askLynzAdjustments(STATE.recipeId) — AI analyzes feedback and suggests formula changes
- "Apply the adjustments" → applyAdjustments() — applies LynZ suggestions to formula

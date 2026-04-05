# Formulation Lab — Dashboard Navigation

## Navigation Commands
Navigate to any view. Recipe-level views auto-drill down to first available recipe if needed.

### GLOBAL VIEWS (work from any level)
- "Open integrations" → nav("m365") — M365/GWS integration hub
- "Show all clients" → navLevel("workspace"); nav("workspace")
- "Open ingredients database" → nav("ingredients")

### RECIPE-LEVEL VIEWS (auto-drill to recipe if needed)
- "Open formula builder" → nav("formula")
- "Check trial log" → nav("trials")
- "Open analytics" → nav("analytics")
- "Show scale-up calculator" → nav("scaleup")
- "Check version history" → nav("versions")
- "Open allergen matrix" → nav("allergens")
- "Check spec targets" → nav("specs")

### PROJECT-LEVEL VIEWS (auto-drill to project if needed)
- "Open stage-gate pipeline" → nav("gates")
- "Show timeline" → nav("timeline")
- "Open risk register" → nav("risks")

## Client & Recipe Navigation
Navigate to specific clients by name. Client IDs: sunburst, kultcha, tidewater, meadowgold.
- "Open Sunburst Beverages" → openClient("sunburst")
- "Go to Kultcha Wellness" → openClient("kultcha")
- "Open Premium OJ recipe" → openRecipe("sb_oj","bom1")
- "Back to workspace" → navLevel("workspace")
- "Go back" → navLevel("project"|"client"|"workspace") — goes up one level

## Platform Toggle (M365 ↔ GWS)
- "Switch to Google Workspace" → togglePlatform() — toggles between M365 and GWS on integrations page
- "Switch to Microsoft 365" → togglePlatform()

## Tabs Within Views
- Ingredients page (5 tabs): switchIngDbTab("ingredients"|"suppliers"|"pricing"|"allergens"|"specs")
- M365 page (8 tabs): switchM365Tab("outlook"|"sharepoint"|"onedrive"|"teams"|"excel"|"calendar"|"entraid"|"graphapi")
- GWS page (8 tabs): switchM365Tab("gmail"|"drive"|"sheets"|"docs"|"calendar"|"meet"|"chat"|"oauth") — same function, different tab IDs when on GWS platform

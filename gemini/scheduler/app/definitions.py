import dagster as dg
from gemini.scheduler.app.assets import all_assets
from gemini.scheduler.app.resources.gemini_api import GEMINIRESTAPI

defs = dg.Definitions(
    assets=all_assets,
    resources={
        "gemini_rest_api": GEMINIRESTAPI()
    }
)

# import dagster as dg
# from gemini.scheduler.app.assets import all_assets

# defs = dg.Definitions(
#     assets=all_assets,
# )


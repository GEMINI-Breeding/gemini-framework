import dagster as dg
import pandas as pd

from gemini.scheduler.app.resources.gemini_api import GEMINIRESTAPI

@dg.asset()
def all_datasets(context: dg.AssetExecutionContext, gemini_rest_api: GEMINIRESTAPI) -> pd.DataFrame:
    response = gemini_rest_api.get("api/datasets/all")
    context.log.info(f"Retrieved datasets: {response}")
    return pd.DataFrame()

dataset_assets = [
    # Define the asset for all datasets
    all_datasets,
]
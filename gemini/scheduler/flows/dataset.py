import pandas as pd
from prefect import flow

from datetime import date
from typing import List

from gemini.api.dataset import DatasetRecord
from gemini.scheduler.tasks.dataset import get_all_datasets, get_dataset_data
@flow(
    name="get_all_datasets_df",
    description="Get all datasets as a dataframe",
    retries=3,
    log_prints=True,
)
def get_all_datasets_df() -> pd.DataFrame:
    datasets = get_all_datasets()
    datasets = [dataset.model_dump() for dataset in datasets]
    dataset_df = pd.DataFrame(datasets)
    print(f"Created Dataframe with {len(dataset_df)} datasets")
    return dataset_df

@flow(
    name="get_dataset_data_df",
    description="Get dataset data as a dataframe",
    retries=3,
    log_prints=True,
)
def get_dataset_data_df(
    dataset_name: str = "Dataset A",
    experiment_name: str = "Experiment A",
    season_name: str = "Season 1A",
    site_name: str = "Site A1",
    collection_date: str = date.today().strftime("%Y-%m-%d"),
) -> pd.DataFrame:
    dataset_records= get_dataset_data(
        dataset_name=dataset_name,
        experiment_name=experiment_name,
        season_name=season_name,
        site_name=site_name,
        collection_date=collection_date,
    )
    return pd.DataFrame()


    

dataset_flow_deployments = [
    get_all_datasets_df.to_deployment(
        name="get_all_datasets_df",
        description="Get all datasets as a dataframe",
        tags=["dataset"]
    ),
    get_dataset_data_df.to_deployment(
        name="get_dataset_data_df",
        description="Get dataset data as a dataframe",
        tags=["dataset"],
        parameters={
            "dataset_name": "Dataset A",
            "experiment_name": "Experiment A",
            "season_name": "Season 1A",
            "site_name": "Site A1",
            "collection_date": date.today().strftime("%Y-%m-%d"),
        }
    ),
]
import pandas as pd
import io

from prefect import flow, runtime
from prefect.filesystems import LocalFileSystem

from datetime import date
from typing import List, Optional

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
    season_name: Optional[str] = None,
    site_name: Optional[str] = None,
    collection_date: Optional[str] = None,
) -> pd.DataFrame:
    dataset_records : List[DatasetRecord] = get_dataset_data(
        dataset_name=dataset_name,
        experiment_name=experiment_name,
        season_name=season_name,
        site_name=site_name,
        collection_date=collection_date,
    )
    dataset_record_dicts = [dataset_record.model_dump() for dataset_record in dataset_records]
    dataset_df = pd.DataFrame(dataset_record_dicts)
    dataset_df['timestamp'] = dataset_df['timestamp'].astype(str)
    print(f"Created Dataframe with {len(dataset_df)} dataset records")
    return dataset_df

@flow(
    name="compile_dataset_data",
    description="Compile dataset data into a CSV file",
    retries=3,
    log_prints=True,
)
def compile_dataset_data(
    dataset_name: str = "Dataset A",
    experiment_name: str = "Experiment A",
    season_name: Optional[str] = None,
    site_name: Optional[str] = None,
    collection_date: Optional[str] = None, 
) -> str:
    dataset_data_df = get_dataset_data_df(
        dataset_name=dataset_name,
        experiment_name=experiment_name,
        season_name=season_name,
        site_name=site_name,
        collection_date=collection_date,
    )
    # Convert dataset data into a CSV file
    folder_name = f"prefect-{runtime.flow_run.name}-{date.today()}"
    local_fs = LocalFileSystem(basepath=f"/tmp/{folder_name}")

    csv_buffer = io.BytesIO()
    dataset_data_df.to_csv(csv_buffer, index=False, encoding="utf-8")
    csv_bytes = csv_buffer.getvalue()
    local_fs.write_path(
        path=f"{local_fs.basepath}/data.csv",
        content=csv_bytes
    )
    print(f"CSV file created at {local_fs.basepath}/data.csv")
    return f"{local_fs.basepath}/data.csv"



    

dataset_flow_deployments = [
    get_all_datasets_df.to_deployment(
        name="get_all_datasets_df",
        description="Get all datasets as a dataframe",
        tags=["dataset"]
    ),
    get_dataset_data_df.to_deployment(
        name="get_dataset_data_df",
        description="Get dataset data as a dataframe",
        tags=["dataset"]
    ),
    compile_dataset_data.to_deployment(
        name="compile_dataset_data",
        description="Compile dataset data into a CSV file",
        tags=["dataset"]
    ),
]
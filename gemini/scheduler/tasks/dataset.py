from prefect import task

from gemini.api.dataset import Dataset, DatasetRecord

from typing import List, Optional
from datetime import date

@task(
    name="get_all_datasets",
    description="Get all datasets",
    tags=["dataset"],
    retries=3,
    log_prints=True,
)
def get_all_datasets() -> List[Dataset]:
    datasets = Dataset.get_all()
    print(f"Found {len(datasets)} datasets")
    return datasets

@task(
    name="get_dataset_by_id",
    description="Get dataset by id",
    tags=["dataset"],
    retries=3,
    log_prints=True,
)
def get_dataset_by_id(dataset_id: str) -> Optional[Dataset]:
    dataset = Dataset.get_by_id(dataset_id)
    if dataset is None:
        print(f"Dataset with id {dataset_id} not found")
    return dataset

@task(
    name="get_dataset_by_name",
    description="Get dataset by name",
    tags=["dataset"],
    retries=3,
    log_prints=True,
)
def get_dataset_by_name(dataset_name) -> Optional[Dataset]:
    dataset = Dataset.get(dataset_name=dataset_name)
    if dataset is None:
        print(f"Dataset with name {dataset_name} not found")
    return dataset

@task(
    name="get_dataset_data",
    description="Get dataset data",
    tags=["dataset"],
    retries=3,
    log_prints=True,
)
def get_dataset_data(
    dataset_name: str,
    experiment_name: Optional[str] = None,
    season_name: Optional[str] = None,
    site_name: Optional[str] = None,
    collection_date: Optional[str] = None,
) -> Optional[List[DatasetRecord]]:
    dataset = Dataset.get(
        dataset_name=dataset_name,
        experiment_name=experiment_name,
    )
    dataset_records_generator = dataset.get_records(
        collection_date=collection_date,
        site_name=site_name,
        season_name=season_name,
        experiment_name=experiment_name,
    )
    dataset_records = [dataset_record for dataset_record in dataset_records_generator]
    print(f"Found {len(dataset_records)} dataset records")
    return dataset_records
    
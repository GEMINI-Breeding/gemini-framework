from litestar.contrib.pydantic import PydanticDTO
from litestar.controller import Controller
from litestar.dto import DTOConfig, DTOData
from litestar.enums import RequestEncodingType, MediaType
from litestar.params import Body
from litestar.handlers import get, post, patch, delete
from pydantic import BaseModel, UUID4

from typing import List, Annotated, Optional
from datetime import datetime, date
from uuid import UUID

from gemini.api.dataset import Dataset
from gemini.api.experiment import Experiment
from gemini.api.dataset_record import DatasetRecord

class DatasetInput(BaseModel):
    dataset_name: str
    dataset_info: Optional[dict] = {}
    is_derived: Optional[bool] = False
    collection_date: Optional[date] = datetime.now().date()
    experiment_name: Optional[str] = None

class DatasetController(Controller):

    # Filter datasets
    @get()
    async def get_datasets(
        self, 
        dataset_name: Optional[str] = None,
        collection_date: Optional[date] = None,
        dataset_info: Optional[dict] = None
        ) -> List[Dataset]:
        datasets = Dataset.search(
            dataset_name=dataset_name,
            collection_date=collection_date,
            dataset_info=dataset_info
        )

        return datasets
    
    # Get Dataset by name
    @get(path="/{dataset_name:str}")
    async def get_dataset_by_name(self, dataset_name: str) -> Dataset:
        dataset = Dataset.get_by_name(dataset_name)
        return dataset
    
    # Get Dataset by ID
    @get(path="/id/{dataset_id:uuid}")
    async def get_dataset_by_id(self, dataset_id: UUID) -> Dataset:
        dataset = Dataset.get_by_id(dataset_id)
        return dataset
    
    # Create a new dataset
    @post()
    async def create_dataset(
        self, data: Annotated[DatasetInput, Body]
    ) -> Dataset:
        dataset = Dataset.create(
            dataset_name=data.dataset_name,
            dataset_info=data.dataset_info,
            is_derived=data.is_derived,
            collection_date=data.collection_date,
            experiment_name=data.experiment_name
        )
        return dataset
    
    # Update Dataset
    @patch(path="/{dataset_name:str}")
    async def update_dataset(
        self, dataset_name: str, data: Annotated[DatasetInput, Body]
    ) -> Dataset:
        dataset = Dataset.get_by_name(dataset_name)
        dataset = dataset.update(
            dataset_info=data.dataset_info,
            is_derived=data.is_derived,
            collection_date=data.collection_date
        )
        return dataset
    
    # Delete Dataset
    @delete(path="/{dataset_name:str}")
    async def delete_dataset(self, dataset_name: str) -> None:
        dataset = Dataset.get_by_name(dataset_name)
        dataset.delete()
    
    # Get Dataset Info
    @get(path="/{dataset_name:str}/info")
    async def get_dataset_info(self, dataset_name: str) -> dict:
        dataset = Dataset.get_by_name(dataset_name)
        dataset_info = dataset.get_info()
        return dataset_info
    
    # Set Dataset Info
    @patch(path="/{dataset_name:str}/info")
    async def set_dataset_info(
        self, dataset_name: str, data: dict
    ) -> Dataset:
        dataset = Dataset.get_by_name(dataset_name)
        dataset = dataset.set_info(dataset_info=data)
        return dataset
    
    # Get Dataset Experiment
    @get(path="/{dataset_name:str}/experiment")
    async def get_dataset_experiment(self, dataset_name: str) -> Experiment:
        dataset = Dataset.get_by_name(dataset_name)
        experiment = dataset.get_experiment()
        return experiment
    
    # Set Dataset Experiment

    # Get Dataset Records
    @get(path="/{dataset_name:str}/records")
    async def get_dataset_records(self, dataset_name: str) -> List[DatasetRecord]:
        dataset = Dataset.get_by_name(dataset_name)
        records = dataset.get_records()
        return records
    
    # Add Dataset Record

    # Get Records CSV
    
    
    

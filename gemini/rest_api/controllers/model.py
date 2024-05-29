from litestar.contrib.pydantic import PydanticDTO
from litestar.controller import Controller
from litestar.dto import DTOConfig, DTOData
from litestar.enums import RequestEncodingType, MediaType
from litestar.params import Body
from litestar.handlers import get, post, patch, delete
from pydantic import BaseModel, UUID4, ConfigDict

from typing import List, Annotated, Optional
from datetime import datetime, date
from uuid import UUID

from gemini.api.model import Model
from gemini.api.model_record import ModelRecord
from gemini.api.dataset import Dataset

class ModelInput(BaseModel):
    model_name: str
    model_info: Optional[dict] = {}
    model_url: Optional[str] = None

    model_config = ConfigDict(
        protected_namespaces=()
    )

class ModelController(Controller):

    # Filter models
    @get()
    async def get_models(
        self, 
        model_name: Optional[str] = None,
        model_info: Optional[dict] = None,
        model_url: Optional[str] = None
        ) -> List[Model]:
        models = Model.search(
            model_name=model_name,
            model_info=model_info,
            model_url=model_url
        )
        return models
    
    # Get Model by name
    @get(path="/{model_name:str}")
    async def get_model(self, model_name: str) -> Model:
        model = Model.get_by_name(model_name)
        return model
    
    # Get Model by ID
    @get(path="/id/{model_id:uuid}")
    async def get_model_by_id(self, model_id: UUID) -> Model:
        model = Model.get_by_id(model_id)
        return model
    
    # Create a new model
    @post()
    async def create_model(
        self, data: Annotated[ModelInput, Body]
        ) -> Model:
        model = Model.create(
            model_name=data.model_name,
            model_info=data.model_info,
            model_url=data.model_url
        )
        return model
    
    # Update a model
    @patch(path="/{model_name:str}")
    async def update_model(
        self, model_name: str, data: Annotated[ModelInput, Body]
        ) -> Model:
        model = Model.get_by_name(model_name)
        model = model.update(
            model_name=data.model_name,
            model_info=data.model_info,
            model_url=data.model_url
        )
        return model
    
    # Delete a model
    @delete(path="/{model_name:str}")
    async def delete_model(self, model_name: str) -> None:
        model = Model.get_by_name(model_name)
        model.delete()

    
    # Get Model Info
    @get(path="/{model_name:str}/info")
    async def get_model_info(self, model_name: str) -> dict:
        model = Model.get_by_name(model_name)
        return model.model_info
    
    # Set Model Info
    @patch(path="/{model_name:str}/info")
    async def set_model_info(
        self, model_name: str, data: Annotated[dict, Body]
        ) -> Model:
        model = Model.get_by_name(model_name)
        model = model.set_info(model_info=data)
        return model
    
    # Get Model Datasets
    @get(path="/{model_name:str}/datasets")
    async def get_model_datasets(self, model_name: str) -> List[Dataset]:
        model = Model.get_by_name(model_name)
        datasets = model.datasets
        return datasets
    
    # Create a new model dataset

    # Add Record
    # Add Records
    # Get Records
    # Get Records in CSV
    


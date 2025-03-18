from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller
from litestar.response import Stream
from litestar.serialization import encode_json

from collections.abc import AsyncGenerator, Generator

from pydantic import BaseModel

from gemini.api.model import Model
from gemini.api.model_record import ModelRecord
from gemini.rest_api.models import ( 
    ModelInput, 
    ModelOutput, 
    ModelUpdate,
    DatasetOutput,
    ModelRunOutput,
    RESTAPIError, 
    str_to_dict, 
    JSONB
)

from typing import List, Annotated, Optional

async def model_records_bytes_generator(model_record_generator: Generator[ModelRecord, None, None]) -> AsyncGenerator[bytes, None]:
    for record in model_record_generator:
        record = record.model_dump(exclude_none=True)
        record = encode_json(record) + b'\n'
        yield record


class ModelModelRunInput(BaseModel):
    model_run_info: Optional[JSONB] = {}

class ModelDatasetInput(BaseModel):
    dataset_name: str
    collection_date: Optional[str] = None
    dataset_info: Optional[JSONB] = {}
    experiment_name: Optional[str] = 'Experiment A'


class ModelController(Controller):

    # Get Models
    @get()
    async def get_models(
        self,
        model_name: Optional[str] = None,
        model_url: Optional[str] = None,
        model_info: Optional[JSONB] = None,
        experiment_name: Optional[str] = 'Experiment A'
    ) -> List[ModelOutput]:
        try:
            if model_info is not None:
                model_info = str_to_dict(model_info)
            models = Model.search(
                model_name=model_name,
                model_info=model_info,
                model_url=model_url,
                experiment_name=experiment_name
            )
            if models is None:
                error_html = RESTAPIError(
                    error="No models found",
                    error_description="No models were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return models
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving models"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Model by ID
    @get(path="/id/{model_id:str}")
    async def get_model_by_id(
        self, model_id: str
    ) -> ModelOutput:
        try:
            model = Model.get_by_id(id=model_id)
            if model is None:
                error_html = RESTAPIError(
                    error="Model not found",
                    error_description="The model with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return model
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the model"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
    
    # Create a new Model
    @post()
    async def create_model(
        self, data: Annotated[ModelInput, Body]
    ) -> ModelOutput:
        try:
            model = Model.create(
                model_name=data.model_name,
                model_url=data.model_url,
                model_info=data.model_info,
                experiment_name=data.experiment_name
            )
            if model is None:
                error_html = RESTAPIError(
                    error="Model not created",
                    error_description="The model could not be created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return model
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the model"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Update Model
    @patch(path="/id/{model_id:str}")
    async def update_model(
        self,
        model_id: str,
        data: Annotated[ModelUpdate, Body]
    ) -> ModelOutput:
        try:
            model = Model.get_by_id(id=model_id)
            if model is None:
                error_html = RESTAPIError(
                    error="Model not found",
                    error_description="The model with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            model = model.update(
                model_name=data.model_name,
                model_url=data.model_url,
                model_info=data.model_info
            )
            if model is None:
                error_html = RESTAPIError(
                    error="Model not updated",
                    error_description="The model could not be updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return model
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the model"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Delete Model
    @delete(path="/id/{model_id:str}")
    async def delete_model(
        self, model_id: str
    ) -> None:
        try:
            model = Model.get_by_id(id=model_id)
            if model is None:
                error_html = RESTAPIError(
                    error="Model not found",
                    error_description="The model with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = model.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Model not deleted",
                    error_description="The model could not be deleted"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return None
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the model"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Model Runs
    @get(path="/id/{model_id:str}/runs")
    async def get_model_runs(
        self, model_id: str
    ) -> List[ModelRunOutput]:
        try:
            model = Model.get_by_id(id=model_id)
            if model is None:
                error_html = RESTAPIError(
                    error="Model not found",
                    error_description="The model with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            model_runs = model.get_runs()
            if model_runs is None:
                error_html = RESTAPIError(
                    error="No model runs found",
                    error_description="No model runs were found for the given model"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return model_runs
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving model runs"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Model Datasets
    @get(path="/id/{model_id:str}/datasets")
    async def get_model_datasets(
        self, model_id: str
    ) -> List[DatasetOutput]:
        try:
            model = Model.get_by_id(id=model_id)
            if model is None:
                error_html = RESTAPIError(
                    error="Model not found",
                    error_description="The model with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            model_datasets = model.get_datasets()
            if model_datasets is None:
                error_html = RESTAPIError(
                    error="No model datasets found",
                    error_description="No model datasets were found for the given model"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return model_datasets
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving model datasets"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Create Model Run
    @post(path="/id/{model_id:str}/runs")
    async def create_model_run(
        self,
        model_id: str,
        data: Annotated[ModelModelRunInput, Body]
    ) -> ModelRunOutput:
        try:
            model = Model.get_by_id(id=model_id)
            if model is None:
                error_html = RESTAPIError(
                    error="Model not found",
                    error_description="The model with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            model_run = model.create_run(model_run_info=data.model_run_info)
            if model_run is None:
                error_html = RESTAPIError(
                    error="Model run not created",
                    error_description="The model run could not be created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return model_run
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the model run"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Create Model Dataset
    @post(path="/id/{model_id:str}/datasets")
    async def create_model_dataset(
        self,
        model_id: str,
        data: Annotated[ModelDatasetInput, Body]
    ) -> DatasetOutput:
        try:
            model = Model.get_by_id(id=model_id)
            if model is None:
                error_html = RESTAPIError(
                    error="Model not found",
                    error_description="The model with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            dataset = model.create_dataset(
                dataset_name=data.dataset_name,
                dataset_info=data.dataset_info,
                collection_date=data.collection_date,
                experiment_name=data.experiment_name
            )
            if dataset is None:
                error_html = RESTAPIError(
                    error="Dataset not created",
                    error_description="The dataset could not be created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return dataset
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the dataset"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)

    # Search Model Records
    @get(path="/id/{model_id:str}/records")
    async def search_model_records(
        self,
        model_id: str,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
        collection_date: Optional[str] = None
    ) -> Stream:
        try:
            model = Model.get_by_id(id=model_id)
            if model is None:
                error_html = RESTAPIError(
                    error="Model not found",
                    error_description="The model with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            model_records = model.get_records(
                collection_date=collection_date,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            return Stream(model_records_bytes_generator(model_records))
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving model records"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    
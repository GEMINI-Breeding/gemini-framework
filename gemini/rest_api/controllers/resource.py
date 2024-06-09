from litestar.controller import Controller
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar import Response
from litestar.response import Stream, File
from litestar.datastructures import UploadFile
from litestar.serialization import encode_json

from pydantic import BaseModel, UUID4, validator
from datetime import datetime, date
from collections.abc import AsyncGenerator

from gemini.api.resource import Resource
from gemini.api.experiment import Experiment
from gemini.rest_api.src.file_handler import file_handler


import json
from typing import List, Annotated, Optional, Union

class ResourceInput(BaseModel):
    resource_file: UploadFile
    resource_name: Optional[str] = None
    resource_tags: Optional[Union[dict, str]] = None
    resource_info: Optional[Union[dict, str]] = None
    experiment_name: Optional[str] = None

    model_config = {
        "arbitrary_types_allowed": True
    }

    @validator("resource_tags", "resource_info", pre=True)
    def convert_str_to_dict(cls, value):
        if isinstance(value, str):
            return json.loads(value)
        return value
    

class ResourceController(Controller):

    # Get Resources
    @get()
    async def get_resources(
        self,
        resource_name: Optional[str] = None,
        resource_file_name: Optional[str] = None,
        resource_uri: Optional[str] = None,
        resource_tags: Optional[dict] = None,
        resource_info: Optional[dict] = None,
        experiment_name: Optional[str] = None
    ) -> List[Resource]:
        experiment = Experiment.get(experiment_name=experiment_name)
        resources = Resource.search(
            resource_name=resource_name,
            resource_file_name=resource_file_name,
            resource_uri=resource_uri,
            resource_tags=resource_tags,
            resource_info=resource_info,
            experiment_id=experiment.id if experiment else None
        )
        return resources
    
    # Get Resource By Name
    @get()
    async def get_resource_by_name(
        self,
        resource_name: str
    ) -> Resource:
        resource = Resource.get(resource_name=resource_name)
        if not resource:
            return Response(content="Resource not found", status_code=404)
        return resource
    
    # Get Resources of an Experiment
    @get('/experiment/{experiment_name:str}')
    async def get_resources_by_experiment(
        self,
        experiment_name: str
    ) -> List[Resource]:
        resources = Resource.get_by_experiment(experiment_name=experiment_name)
        if not resources:
            return Response(content="No resources found", status_code=404)
        return resources
    
    # Get Resource Info By ID
    @get('/{resource_id:str}/info')
    async def get_resource_info(
        self,
        resource_id: str
    ) -> dict:
        resource = Resource.get(resource_id=resource_id)
        if not resource:
            return Response(content="Resource not found", status_code=404)
        return resource.get_info()
    
    # Set Resource Info By ID
    @patch('/{resource_id:str}/info')
    async def set_resource_info(
        self,
        resource_id: str,
        data: dict
    ) -> dict:
        resource = Resource.get(resource_id=resource_id)
        if not resource:
            return Response(content="Resource not found", status_code=404)
        resource.set_info(resource_info=data)
        return resource.get_info()

    # Create Resource
    @post()
    async def create_resource(
        self,
        data: Annotated[ResourceInput, Body(media_type=RequestEncodingType.MULTI_PART)]
    ) -> Resource:
        resource_file = data.resource_file
        resource_file_path = await file_handler.save_file(resource_file)

        # Create Resource
        resource = Resource.create(
            resource_file_path=resource_file_path,
            resource_name=data.resource_name if data.resource_name else resource_file.filename,
            resource_tags=data.resource_tags,
            resource_info=data.resource_info,
            experiment_name=data.experiment_name 
        )

        return resource
    
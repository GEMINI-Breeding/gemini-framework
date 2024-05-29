from collections.abc import AsyncGenerator
from datetime import datetime, date
from typing import Annotated, List, Optional, Union
from uuid import UUID

from litestar import Request
from litestar.controller import Controller
from litestar.dto import DTOConfig, DTOData
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import delete, get, patch, post
from litestar.params import Body
from litestar.response import Stream, File
from litestar.serialization import default_serializer, encode_json
from litestar.datastructures import UploadFile
from pydantic import BaseModel, ConfigDict, validator

from gemini.api.resource import Resource
from gemini.api.data_format import DataFormat
from gemini.api.experiment import Experiment

from gemini.api.enums import GEMINIDataFormat
import json


class ResourceInput(BaseModel):
    resource_file: UploadFile
    resource_name: Optional[str] = None
    resource_tags: Optional[Union[dict, str]] = {}
    resource_info: Optional[Union[dict, str]] = {}
    experiment_name: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @validator("resource_tags", "resource_info", pre=True)
    def convert_str_to_dict(cls, value):
        if isinstance(value, str):
            return json.loads(value)
        return value


class ResourceController(Controller):

    # Filter Resources
    @get()
    async def get_resources(
        self,
        resource_name: Optional[str] = None,
        resource_file_name: Optional[str] = None,
        resource_uri: Optional[str] = None,
        resource_tags: Optional[dict] = None,
        resource_info: Optional[dict] = None,
    ) -> List[Resource]:
        resources = Resource.search(
            resource_name=resource_name,
            resource_tags=resource_tags,
            resource_info=resource_info,
            resource_file_name=resource_file_name,
            resource_uri=resource_uri,
        )
        return resources

    # Get Resource by name
    @get("/{resource_name:str}")
    async def get_resource_by_name(self, resource_name: str) -> Resource:
        resource = Resource.get_by_name(resource_name)
        return resource

    # Get Resource by ID
    @get("/id/{resource_id:uuid}")
    async def get_resource_by_id(self, resource_id: UUID) -> Resource:
        resource = Resource.get_by_id(resource_id)
        return resource

    # Get By Resource URI
    @get("/uri/{resource_uri:str}")
    async def get_resource_by_uri(self, resource_uri: str) -> Resource:
        resource = Resource.get_by_uri(resource_uri)
        return resource

    # Create a new resource / Upload
    @post()
    async def create_resource(
        self,
        data: Annotated[ResourceInput, Body(media_type=RequestEncodingType.MULTI_PART)],
    ) -> Resource:

        # Write file content to local disk
        resource_file = data.resource_file
        resource_file_path = f"uploads/{resource_file.filename}"
        with open(resource_file_path, "wb") as f:
            f.write(await resource_file.read())

        # Create resource
        resource = Resource.upload(
            resource_file=resource_file_path,
            resource_file_name=resource_file.filename,
            resource_name=data.resource_name if data.resource_name else None,
            resource_tags=data.resource_tags,
            resource_info=data.resource_info,
            experiment_name=data.experiment_name,
        )
        return resource

    # Download resource given resource ID
    @get("/download/{resource_id:uuid}")
    async def download_resource(self, resource_id: UUID) -> Stream:
        resource = Resource.get_by_id(resource_id)
        resource_file_name = resource.resource_file_name
        download_path = f"downloads/{resource_file_name}"
        download_path = resource.download(download_path)
        return File(
            path=download_path,
            filename=resource.resource_file_name,
        )

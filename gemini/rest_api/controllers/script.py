from collections.abc import AsyncGenerator
from datetime import datetime, date
from typing import Annotated, List, Optional
from uuid import UUID

from litestar import Request
from litestar.controller import Controller
from litestar.dto import DTOConfig, DTOData
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import delete, get, patch, post
from litestar.params import Body
from litestar.response import Stream
from litestar.serialization import default_serializer, encode_json
from pydantic import BaseModel

from gemini.api.script import Script
from gemini.api.script_record import ScriptRecord
from gemini.api.dataset import Dataset


class ScriptInput(BaseModel):
    script_name: str
    script_url: Optional[str] = None
    script_extension: Optional[str] = None
    script_info: Optional[dict] = {}


class ScriptController(Controller):

    # Filter Scripts
    @get()
    async def get_scripts(
        self,
        script_name: Optional[str] = None,
        script_url: Optional[str] = None,
        script_extension: Optional[str] = None,
        script_info: Optional[dict] = None,
    ) -> List[Script]:
        scripts = Script.search(
            script_name=script_name,
            script_url=script_url,
            script_extension=script_extension,
            script_info=script_info,
        )
        return scripts

    # Get Script by name
    @get("/{script_name:str}")
    async def get_script_by_name(self, script_name: str) -> Script:
        script = Script.get_by_name(script_name)
        return script

    # Get Script by ID
    @get("/id/{script_id:uuid}")
    async def get_script_by_id(self, script_id: UUID) -> Script:
        script = Script.get_by_id(script_id)
        return script

    # Create a new script
    @post()
    async def create_script(self, script_input: Annotated[ScriptInput, Body]) -> Script:
        script = Script.create(
            script_name=script_input.script_name,
            script_url=script_input.script_url,
            script_extension=script_input.script_extension,
            script_info=script_input.script_info,
        )
        return script

    # Delete a script by name
    @delete("/{script_name:str}")
    async def delete_script_by_name(self, script_name: str) -> None:
        script = Script.get_by_name(script_name)
        script.delete()

    # Delete a script by ID
    @delete("/id/{script_id:uuid}")
    async def delete_script_by_id(self, script_id: UUID) -> None:
        script = Script.get_by_id(script_id)
        script.delete()

    # Get script info
    @get("/{script_name:str}/info")
    async def get_script_info(self, script_name: str) -> str:
        script = Script.get_by_name(script_name)
        script = script.get_info()
        return script

    # Set script info
    @patch("/{script_name:str}/info")
    async def set_script_info(
        self, script_name: str, info: Annotated[dict, Body]
    ) -> Script:
        script = Script.get_by_name(script_name)
        script = script.set_info(script_info=info)
        return script

    # Get script datasets
    @get("/{script_name:str}/datasets")
    async def get_script_datasets(self, script_name: str) -> List[Dataset]:
        script = Script.get_by_name(script_name)
        datasets = script.get_datasets()
        return datasets

    # Create a new script record

    # Add Record
    # Add Records
    # Get Records
    # Get Records in CSV

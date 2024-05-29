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

from gemini.api.procedure import Procedure
from gemini.api.procedure_record import ProcedureRecord
from gemini.api.dataset import Dataset


class ProcedureInput(BaseModel):
    procedure_name: str
    procedure_info: str


class ProcedureController(Controller):

    # Filter Procedures
    @get()
    async def get_procedures(
        self,
        procedure_name: Optional[str] = None,
        procedure_info: Optional[str] = None,
    ) -> List[Procedure]:
        procedures = Procedure.search(
            procedure_name=procedure_name,
            procedure_info=procedure_info,
        )
        return procedures

    # Get procedure by name
    @get("/{procedure_name:str}")
    async def get_procedure_by_name(self, procedure_name: str) -> Procedure:
        procedure = Procedure.get_by_name(procedure_name)
        return procedure

    # Get procedure by ID
    @get("/id/{procedure_id:uuid}")
    async def get_procedure_by_id(self, procedure_id: UUID) -> Procedure:
        procedure = Procedure.get_by_id(procedure_id)
        return procedure

    # Create a new procedure
    @post()
    async def create_procedure(
        self, data: Annotated[ProcedureInput, Body]
    ) -> Procedure:
        procedure = Procedure.create(
            procedure_name=data.procedure_name,
            procedure_info=data.procedure_info,
        )
        return procedure

    # Delete a procedure by name
    @delete("/{procedure_name:str}")
    async def delete_procedure_by_name(self, procedure_name: str) -> None:
        procedure = Procedure.get_by_name(procedure_name)
        procedure.delete()

    # Delete a procedure by ID
    @delete("/id/{procedure_id:uuid}")
    async def delete_procedure_by_id(self, procedure_id: UUID) -> None:
        procedure = Procedure.get_by_id(procedure_id)
        procedure.delete()

    # Get procedure info
    @get("/{procedure_name:str}/info")
    async def get_procedure_info(self, procedure_name: str) -> str:
        procedure = Procedure.get_by_name(procedure_name)
        procedure = procedure.get_info()
        return procedure

    # Set procedure info
    @patch("/{procedure_name:str}/info")
    async def set_procedure_info(
        self, procedure_name: str, data: Annotated[dict, Body]
    ) -> Procedure:
        procedure = Procedure.get_by_name(procedure_name)
        procedure = procedure.set_info(procedure_info=data)
        return procedure

    # Get procedure datasets
    @get("/{procedure_name:str}/datasets")
    async def get_procedure_datasets(self, procedure_name: str) -> List[Dataset]:
        procedure = Procedure.get_by_name(procedure_name)
        datasets = procedure.get_datasets()
        return datasets

    # Create a new procedure dataset

    # Add Record
    # Add Records
    # Get Records
    # Get Records in CSV

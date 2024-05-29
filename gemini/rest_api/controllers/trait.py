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
from collections.abc import AsyncGenerator
from pydantic import BaseModel

from gemini.api.trait import Trait
from gemini.api.trait_record import TraitRecord
from gemini.api.trait_level import TraitLevel
from gemini.api.experiment import Experiment
from gemini.api.dataset import Dataset
from gemini.api.enums import GEMINITraitLevel


async def trait_generator(**params) -> AsyncGenerator[bytes, None]:
    traits = Trait.search(**params)
    for trait in traits:
        trait = trait.model_dump_json()
        yield trait


class TraitInput(BaseModel):
    trait_name: str
    trait_units: Optional[str] = "mol/kg"
    trait_level: Optional[GEMINITraitLevel] = GEMINITraitLevel.Default
    trait_info: Optional[dict] = {}
    experiment_name: Optional[str] = None


class TraitRecordSearchFilter(BaseModel):
    sensor_name: Optional[str] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None


class TraitController(Controller):

    # Filter Traits
    @get()
    async def get_traits(
        self,
        trait_name: Optional[str] = None,
        trait_units: Optional[str] = None,
        trait_level: Optional[GEMINITraitLevel] = None,
    ) -> List[Trait]:
        traits = Trait.search(
            trait_name=trait_name,
            trait_units=trait_units,
            trait_level=trait_level,
        )
        return traits

    # Get Trait by name
    @get("/{trait_name:str}")
    async def get_trait_by_name(self, trait_name: str) -> Trait:
        trait = Trait.get_by_name(trait_name)
        return trait

    # Get Trait by ID
    @get("/id/{trait_id:uuid}")
    async def get_trait_by_id(self, trait_id: UUID) -> Trait:
        trait = Trait.get_by_id(trait_id)
        return trait

    # Create a new trait
    @post()
    async def create_trait(self, trait_input: Annotated[TraitInput, Body]) -> Trait:
        trait = Trait.create(
            trait_name=trait_input.trait_name,
            trait_units=trait_input.trait_units,
            trait_level=trait_input.trait_level,
            trait_info=trait_input.trait_info,
            experiment_name=trait_input.experiment_name,
        )
        return trait

    # Delete a trait by name
    @delete("/{trait_name:str}")
    async def delete_trait_by_name(self, trait_name: str) -> None:
        trait = Trait.get_by_name(trait_name)
        trait.delete()

    # Delete a trait by ID
    @delete("/id/{trait_id:uuid}")
    async def delete_trait_by_id(self, trait_id: UUID) -> None:
        trait = Trait.get_by_id(trait_id)
        trait.delete()

    # Get trait info
    @get("/{trait_name:str}/info")
    async def get_trait_info(self, trait_name: str) -> dict:
        trait = Trait.get_by_name(trait_name)
        trait = trait.get_info()
        return trait

    # Set trait info
    @patch("/{trait_name:str}/info")
    async def set_trait_info(
        self, trait_name: str, info: Annotated[dict, Body]
    ) -> Trait:
        trait = Trait.get_by_name(trait_name)
        trait = trait.set_info(trait_info=info)
        return trait

    # Get trait experiments
    @get("/{trait_name:str}/experiments")
    async def get_trait_experiments(self, trait_name: str) -> List[Experiment]:
        trait = Trait.get_by_name(trait_name)
        experiments = trait.get_experiments()
        return experiments

    # Get trait datasets
    @get("/{trait_name:str}/datasets")
    async def get_trait_datasets(self, trait_name: str) -> List[Dataset]:
        trait = Trait.get_by_name(trait_name)
        datasets = trait.get_datasets()
        return datasets

    # Todo: Get trait records
    @get("/{trait_name:str}/records")
    async def get_trait_records(
        self,
        trait_name: str,
        sensor_name: Optional[str] = None,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
        plot_number: Optional[int] = None,
        plot_row_number: Optional[int] = None,
        plot_column_number: Optional[int] = None,
    ) -> Stream:
        return Stream(
            trait_generator(
                trait_name=trait_name,
                sensor_name=sensor_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
            )
        )

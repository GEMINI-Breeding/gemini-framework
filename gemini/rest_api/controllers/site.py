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

from gemini.api.site import Site
from gemini.api.experiment import Experiment
from gemini.api.plot import Plot


class SiteInput(BaseModel):
    site_name: str
    site_city: Optional[str] = None
    site_state: Optional[str] = None
    site_country: Optional[str] = None
    site_info: Optional[dict] = {}
    experiment_name: Optional[str] = None


class SiteController(Controller):

    # Filter Sites
    @get()
    async def get_sites(
        self,
        site_name: Optional[str] = None,
        site_city: Optional[str] = None,
        site_state: Optional[str] = None,
        site_country: Optional[str] = None,
        site_info: Optional[dict] = None,
    ) -> List[Site]:
        sites = Site.search(
            site_name=site_name,
            site_city=site_city,
            site_state=site_state,
            site_country=site_country,
            site_info=site_info,
        )
        return sites

    # Get Site by name
    @get("/{site_name:str}")
    async def get_site_by_name(self, site_name: str) -> Site:
        site = Site.get_by_name(site_name)
        return site

    # Get Site by ID
    @get("/id/{site_id:uuid}")
    async def get_site_by_id(self, site_id: UUID) -> Site:
        site = Site.get_by_id(site_id)
        return site

    # Create a new site
    @post()
    async def create_site(self, site_input: Annotated[SiteInput, Body]) -> Site:
        site = Site.create(
            site_name=site_input.site_name,
            site_city=site_input.site_city,
            site_state=site_input.site_state,
            site_country=site_input.site_country,
            site_info=site_input.site_info,
            experiment_name=site_input.experiment_name,
        )
        return site

    # Delete a site by name
    @delete("/{site_name:str}")
    async def delete_site_by_name(self, site_name: str) -> None:
        site = Site.get_by_name(site_name)
        site.delete()

    # Delete a site by ID
    @delete("/id/{site_id:uuid}")
    async def delete_site_by_id(self, site_id: UUID) -> None:
        site = Site.get_by_id(site_id)
        site.delete()

    # Get site info
    @get("/{site_name:str}/info")
    async def get_site_info(self, site_name: str) -> dict:
        site = Site.get_by_name(site_name)
        site = site.get_info()
        return site

    # Set site info
    @patch("/{site_name:str}/info")
    async def set_site_info(self, site_name: str, info: Annotated[dict, Body]) -> Site:
        site = Site.get_by_name(site_name)
        site = site.set_info(site_info=info)
        return site

    # Get site experiments
    @get("/{site_name:str}/experiments")
    async def get_site_experiments(self, site_name: str) -> List[Experiment]:
        site = Site.get_by_name(site_name)
        experiments = site.get_experiments()
        return experiments

    # Get site plots
    @get("/{site_name:str}/plots")
    async def get_site_plots(self, site_name: str) -> List[Plot]:
        site = Site.get_by_name(site_name)
        plots = site.get_plots()
        return plots

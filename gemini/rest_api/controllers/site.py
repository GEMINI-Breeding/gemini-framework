from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.site import Site
from gemini.rest_api.models import SiteInput, SiteOutput, RESTAPIError, SiteUpdate, str_to_dict, JSONB

from typing import List, Annotated, Optional

class SiteController(Controller):

    # Get All Sites
    @get(path="/all")
    async def get_all_sites(self) -> List[SiteOutput]:
        try:
            sites = Site.get_all()
            if sites is None:
                error_html = RESTAPIError(
                    error="No sites found",
                    error_description="No sites were found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return sites
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving all sites"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)

    # Get Sites
    @get()
    async def get_sites(
        self,
        site_name: Optional[str] = None,
        site_city: Optional[str] = None,
        site_state: Optional[str] = None,
        site_country: Optional[str] = None,
        site_info: Optional[JSONB] = None,
        experiment_name: Optional[str] = 'Experiment A'
    ) -> List[SiteOutput]:
        try:
            if site_info is not None:
                site_info = str_to_dict(site_info)

            sites = Site.search(
                site_name=site_name,
                site_city=site_city,
                site_state=site_state,
                site_country=site_country,
                site_info=site_info,
                experiment_name=experiment_name
            )
            if sites is None:
                error_html = RESTAPIError(
                    error="No sites found",
                    error_description="No sites were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return sites
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving sites"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Site by ID
    @get(path="/id/{site_id:str}")
    async def get_site_by_id(
        self, site_id: str
    ) -> SiteOutput:
        try:
            site = Site.get_by_id(id=site_id)
            if site is None:
                error_html = RESTAPIError(
                    error="Site not found",
                    error_description="The site with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return site
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the site"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Create Site
    @post()
    async def create_site(
        self,
        data: Annotated[SiteInput, Body]
    ) -> SiteOutput:
        try:
            site = Site.create(
                site_name=data.site_name,
                site_city=data.site_city,
                site_state=data.site_state,
                site_country=data.site_country,
                site_info=data.site_info,
                experiment_name=data.experiment_name
            )
            if site is None:
                error_html = RESTAPIError(
                    error="Site not created",
                    error_description="The site was not created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return site
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the site"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)


    # Update Site
    @patch(path="/id/{site_id:str}")
    async def update_site(
        self,
        site_id: str,
        data: Annotated[SiteUpdate, Body]
    ) -> SiteOutput:
        try:
            site = Site.get_by_id(id=site_id)
            if site is None:
                error_html = RESTAPIError(
                    error="Site not found",
                    error_description="The site with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            site = site.update(
                site_name=data.site_name,
                site_city=data.site_city,
                site_state=data.site_state,
                site_country=data.site_country,
                site_info=data.site_info
            )
            return site
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the site"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Delete Site
    @delete(path="/id/{site_id:str}")
    async def delete_site(
        self, site_id: str
    ) -> None:
        try:
            site = Site.get_by_id(id=site_id)
            if site is None:
                error_html = RESTAPIError(
                    error="Site not found",
                    error_description="The site with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = site.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Failed to delete site",
                    error_description="The site could not be deleted"
                ).to_html()
                return Response(content=error_html, status_code=500)
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the site"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

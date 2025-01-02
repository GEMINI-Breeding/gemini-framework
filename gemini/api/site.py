from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.sites import SiteModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.views.experiment_views import ExperimentSitesViewModel

class Site(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "site_id"))

    site_name: str
    site_city: Optional[str] = None
    site_state: Optional[str] = None
    site_country: Optional[str] = None
    site_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        site_name: str,
        site_city: str,
        site_state: str,
        site_country: str,
        site_info: dict = {},
        experiment_name: str = "Default",
    ) -> "Site":
        try:
            db_instance = SiteModel.get_or_create(
                site_name=site_name,
                site_city=site_city,
                site_state=site_state,
                site_country=site_country,
                site_info=site_info,
            )
            site = cls.model_validate(db_instance)
            experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
            if experiment:
                experiment.sites.append(site)
            return site
        except Exception as e:
            raise e
        

    @classmethod
    def get(cls, site_name: str) -> "Site":
        try:
            db_instance = SiteModel.get_by_parameters(
                site_name=site_name,
            )
            site = cls.model_validate(db_instance)
            return site
        except Exception as e:
            raise e
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Site":
        try:
            db_instance = SiteModel.get(id)
            site = cls.model_validate(db_instance)
            return site
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["Site"]:
        try:
            sites = SiteModel.all()
            sites = [cls.model_validate(site) for site in sites]
            return sites if sites else None
        except Exception as e:
            raise e
        

    @classmethod
    def search(cls, **search_parameters) -> List["Site"]:
        try:
            sites = ExperimentSitesViewModel.search(**search_parameters)
            sites = [cls.model_validate(site) for site in sites]
            return sites if sites else None
        except Exception as e:
            raise e
        

    def update(self, **update_parameters) -> "Site":
        try:
            current_id = self.id
            site = SiteModel.get(current_id)
            site = SiteModel.update(site, **update_parameters)
            site = self.model_validate(site)
            return site
        except Exception as e:
            raise e
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            site = SiteModel.get(current_id)
            SiteModel.delete(site)
            return True
        except Exception as e:
            return False
        

    def refresh(self) -> "Site":
        try:
            db_instance = SiteModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    actual_value = getattr(instance, key)
                    setattr(self, key, actual_value)
            return self
        except Exception as e:
            raise e 
        
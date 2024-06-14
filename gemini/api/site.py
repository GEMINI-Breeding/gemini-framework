from typing import Optional, List, Any
from gemini.api.base import APIBase
from gemini.models import SiteModel, ExperimentModel, ExperimentSitesViewModel
from gemini.logger import logger_service


class Site(APIBase):

    db_model = SiteModel

    site_name: str
    site_city: Optional[str] = None
    site_state: Optional[str] = None
    site_country: Optional[str] = None
    site_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        site_name: str,
        site_city: str = 'Default',
        site_state: str = 'Default',
        site_country: str = 'Default',
        site_info: dict = {},
        experiment_name: str = 'Default'
    ):
        
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        db_instance = cls.db_model.get_or_create(
            site_name=site_name,
            site_city=site_city,
            site_state=site_state,
            site_country=site_country,
            site_info=site_info
        )
        if db_experiment and db_instance not in db_experiment.sites:
            db_experiment.sites.append(db_instance)
            db_experiment.save()
        instance = cls.model_validate(db_instance)
        logger_service.info(
            "API",
            f"Created a new instance of {cls.__name__} with id {instance.id}",
        )
        return instance
    
    @classmethod
    def get(cls, site_name: str) -> "Site":
        db_instance = cls.db_model.get_by_parameters(site_name=site_name)
        logger_service.info("API", f"Retrieved site with name {site_name} from the database")
        return cls.model_validate(db_instance)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.site_name} from the database")
        return self.site_info
    
    def set_info(self, site_info: Optional[dict] = None) -> "Site":
        self.update(site_info=site_info)
        logger_service.info("API", f"Set information about {self.site_name} in the database")
        return self
    
    def add_info(self, site_info: Optional[dict] = None) -> "Site":
        current_info = self.get_info()
        updated_info = {**current_info, **site_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information to {self.site_name} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Site":
        current_info = self.get_info()
        updated_info = {k: v for k, v in current_info.items() if k not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info("API", f"Removed information from {self.site_name} in the database")
        return self
    
    @classmethod
    def search(
        cls,
        experiment_name: str = None,
        **kwargs
    ) -> List["Site"]:
        db_sites = ExperimentSitesViewModel.search(
            experiment_name=experiment_name,
            **kwargs
        )
        logger_service.info("API", f"Retrieved sites from the database")
        return [cls.model_validate(db_site) for db_site in db_sites]




from typing import Optional, List
from gemini.api.base import APIBase, ID
from gemini.server.database.models import SiteModel, ExperimentModel, ExperimentSitesViewModel
from pydantic import Field, AliasChoices


class Site(APIBase):

    db_model = SiteModel

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
        site_city: str = 'Default',
        site_state: str = 'Default',
        site_country: str = 'Default',
        site_info: dict = {},
        experiment_name: str = 'Default'
    ):
        """
        Create a new site with the given parameters.

        Args:
            site_name (str): The name of the site.
            site_city (str, optional): The city of the site. Defaults to 'Default'.
            site_state (str, optional): The state of the site. Defaults to 'Default'.
            site_country (str, optional): The country of the site. Defaults to 'Default'.
            site_info (dict, optional): Additional information about the site. Defaults to {}.
            experiment_name (str, optional): The name of the experiment associated with the site. Defaults to 'Default'.

        Returns:
            Site: The created site instance.
        """
        
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
        return instance
    
    @classmethod
    def get(cls, site_name: str) -> "Site":
        """
        Get the site with the given name.

        Args:
            site_name (str): The name of the site.

        Returns:
            Site: The site instance.
        """
        db_instance = cls.db_model.get_by_parameters(site_name=site_name)
        return cls.model_validate(db_instance)
    
    def get_info(self) -> dict:
        """
        Get the information of the site.

        Returns:
            dict: The site information.
        """
        self.refresh()
        return self.site_info
    
    def set_info(self, site_info: Optional[dict] = None) -> "Site":
        """
        Set the information of the site.

        Args:
            site_info (dict, optional): The site information to set. Defaults to None.

        Returns:
            Site: The updated site instance.
        """
        self.update(site_info=site_info)
        return self
    
    def add_info(self, site_info: Optional[dict] = None) -> "Site":
        """
        Add additional information to the site.

        Args:
            site_info (dict, optional): The additional site information to add. Defaults to None.

        Returns:
            Site: The updated site instance.
        """
        current_info = self.get_info()
        updated_info = {**current_info, **site_info}
        self.set_info(updated_info)
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Site":
        """
        Remove specific keys from the site information.

        Args:
            keys_to_remove (List[str]): The keys to remove from the site information.

        Returns:
            Site: The updated site instance.
        """
        current_info = self.get_info()
        updated_info = {k: v for k, v in current_info.items() if k not in keys_to_remove}
        self.set_info(updated_info)
        return self
    
    @classmethod
    def search(
        cls,
        experiment_name: str = None,
        **kwargs
    ) -> List["Site"]:
        """
        Search for sites based on the given parameters.

        Args:
            experiment_name (str, optional): The name of the experiment associated with the sites. Defaults to None.
            **kwargs: Additional search parameters.

        Returns:
            List[Site]: The list of matching site instances.
        """
        db_sites = ExperimentSitesViewModel.search(
            experiment_name=experiment_name,
            **kwargs
        )
        return [cls.model_validate(db_site) for db_site in db_sites]

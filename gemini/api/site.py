from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.sites import SiteModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.associations import ExperimentSiteModel
from gemini.db.models.views.experiment_views import ExperimentSitesViewModel
from gemini.db.models.views.plot_view import PlotViewModel

class Site(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "site_id"))

    site_name: str
    site_city: Optional[str] = None
    site_state: Optional[str] = None
    site_country: Optional[str] = None
    site_info: Optional[dict] = None

    def __str__(self):
        return f"Site(name={self.site_name}, id={self.id})"
    
    def __repr__(self):
        return f"Site(site_name={self.site_name}, id={self.id})"
    
    @classmethod
    def exists(
        cls,
        site_name: str
    ) -> bool:
        try:
            exists = SiteModel.exists(site_name=site_name)
            return exists
        except Exception as e:
            print(f"Error checking existence of site: {e}")
            return False
        
    @classmethod
    def create(
        cls,
        site_name: str,
        site_city: str = None,
        site_state: str = None,
        site_country: str = None,
        site_info: dict = {},
        experiment_name: str = None
    ) -> Optional["Site"]:
        try:
            db_instance = SiteModel.get_or_create(
                site_name=site_name,
                site_city=site_city,
                site_state=site_state,
                site_country=site_country,
                site_info=site_info,
            )
            site = cls.model_validate(db_instance)
            if experiment_name:
                site.associate_experiment(experiment_name)
            return site
        except Exception as e:
            print(f"Error creating site: {e}")
            return None
    
    @classmethod
    def get(
        cls,
        site_name: str,
        experiment_name: str = None
    ) -> Optional["Site"]:
        try:
            db_instance = ExperimentSitesViewModel.get_by_parameters(
                site_name=site_name,
                experiment_name=experiment_name
            )
            if not db_instance:
                print(f"Site with name {site_name} not found.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting site: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["Site"]:
        try:
            db_instance = SiteModel.get(id)
            if not db_instance:
                print(f"Site with ID {id} does not exist.")
                return None
            site = cls.model_validate(db_instance)
            return site
        except Exception as e:
            print(f"Error getting site by ID: {e}")
            return None
        
    @classmethod
    def get_all(cls) -> Optional[List["Site"]]:
        try:
            sites = SiteModel.all()
            if not sites or len(sites) == 0:
                print("No sites found.")
                return None
            sites = [cls.model_validate(site) for site in sites]
            return sites
        except Exception as e:
            print(f"Error getting all sites: {e}")
            return None
        
    @classmethod
    def search(
        cls,
        site_name: str = None,
        site_city: str = None,
        site_state: str = None,
        site_country: str = None,
        site_info: dict = None,
        experiment_name: str = None
    ) -> Optional[List["Site"]]:
        try:
            if not any([site_name, site_city, site_state, site_country, site_info, experiment_name]):
                print("No search parameters provided.")
                return None

            sites = ExperimentSitesViewModel.search(
                site_name=site_name,
                site_city=site_city,
                site_state=site_state,
                site_country=site_country,
                site_info=site_info,
                experiment_name=experiment_name
            )
            if not sites or len(sites) == 0:
                print("No sites found matching the search criteria.")
                return None
            sites = [cls.model_validate(site) for site in sites]
            return sites
        except Exception as e:
            print(f"Error searching sites: {e}")
            return None
        
    def update(
        self,
        site_name: str = None,
        site_city: str = None,
        site_state: str = None,
        site_country: str = None,
        site_info: dict = None
    ) -> Optional["Site"]:
        try:
            if not any([site_city, site_state, site_country, site_info, site_name]):
                raise ValueError("At least one update parameter must be provided.")
            
            current_id = self.id
            site = SiteModel.get(current_id)
            if not site:
                print(f"Site with ID {current_id} does not exist.")
                return None
            
            updated_site = SiteModel.update(
                site,
                site_name=site_name,
                site_city=site_city,
                site_state=site_state,
                site_country=site_country,
                site_info=site_info
            )
            updated_site = self.model_validate(updated_site)
            self.refresh()
            return updated_site
        except Exception as e:
            print(f"Error updating site: {e}")
            return None
    
    def delete(self) -> bool:
        try:
            current_id = self.id
            site = SiteModel.get(current_id)
            if not site:
                print(f"Site with ID {current_id} does not exist.")
                return False
            
            SiteModel.delete(site)
            return True
        except Exception as e:
            print(f"Error deleting site: {e}")
            return False
        
    def refresh(self) -> Optional["Site"]:
        try:
            db_instance = SiteModel.get(self.id)
            if not db_instance:
                print(f"Site with ID {self.id} does not exist.")
                return self
            
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing site: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            site = SiteModel.get(current_id)
            if not site:
                print(f"Site with ID {current_id} does not exist.")
                return None
            
            site_info = site.site_info
            if not site_info:
                print("Site info is empty.")
                return None
            return site_info
        except Exception as e:
            print(f"Error getting site info: {e}")
            return None
        
    def set_info(self, site_info: dict) -> Optional["Site"]:
        try:
            current_id = self.id
            site = SiteModel.get(current_id)
            if not site:
                print(f"Site with ID {current_id} does not exist.")
                return None
            
            updated_site = SiteModel.update(
                site,
                site_info=site_info
            )
            updated_site = self.model_validate(updated_site)
            self.refresh()
            return updated_site
        except Exception as e:
            print(f"Error setting site info: {e}")
            return None
        
    def get_associated_experiments(self):
        try:
            from gemini.api.experiment import Experiment
            experiment_sites = ExperimentSitesViewModel.search(site_id=self.id)
            if not experiment_sites or len(experiment_sites) == 0:
                print(f"No associated experiments found for site {self.site_name}.")
                return None
            experiments = [Experiment.model_validate(experiment) for experiment in experiment_sites]
            return experiments
        except Exception as e:
            print(f"Error getting associated experiments: {e}")
            return None

    def associate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return None
            existing_association = ExperimentSiteModel.get_by_parameters(
                experiment_id=experiment.id,
                site_id=self.id
            )
            if existing_association:
                print(f"Site {self.site_name} already associated with experiment {experiment_name}.")
                return None
            new_association = ExperimentSiteModel.get_or_create(
                experiment_id=experiment.id,
                site_id=self.id
            )
            if not new_association:
                print(f"Failed to associate site {self.site_name} with experiment {experiment_name}.")
                return None
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error associating experiment: {e}")
            return None

    def unassociate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return None
            existing_association = ExperimentSiteModel.get_by_parameters(
                experiment_id=experiment.id,
                site_id=self.id
            )
            if not existing_association:
                print(f"Site {self.site_name} not associated with experiment {experiment_name}.")
                return None
            is_deleted = ExperimentSiteModel.delete(existing_association)
            if not is_deleted:
                print(f"Failed to unassociate site {self.site_name} from experiment {experiment_name}.")
                return None
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error unassociating experiment: {e}")
            return None

    def belongs_to_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return False
            association_exists = ExperimentSiteModel.exists(
                experiment_id=experiment.id,
                site_id=self.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking experiment membership: {e}")
            return False

    def get_associated_plots(self):
        try:
            from gemini.api.plot import Plot
            plots = PlotViewModel.search(site_id=self.id)
            if not plots or len(plots) == 0:
                print(f"No associated plots found for site {self.site_name}.")
                return None
            plots = [Plot.model_validate(plot) for plot in plots]
            return plots
        except Exception as e:
            print(f"Error getting associated plots: {e}")
            return None
        
    def create_new_plot(
        self,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        experiment_name: str = None,
        season_name: str = None,
        plot_info: dict = {}
    ):
        try:
            from gemini.api.plot import Plot
            new_plot = Plot.create(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=self.site_name,
                plot_info=plot_info
            )
            if not new_plot:
                print(f"Failed to create new plot {plot_number}.")
                return None
            return new_plot
        except Exception as e:
            print(f"Error creating new plot: {e}")
            return None

    def associate_plot(
        self,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        experiment_name: str = None,
        season_name: str = None
    ):
        try:
            from gemini.api.plot import Plot
            plot = Plot.get(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name
            )
            if not plot:
                print(f"Plot {plot_number} does not exist.")
                return None
            plot.associate_site(site_name=self.site_name)
            return plot
        except Exception as e:
            print(f"Error associating plot: {e}")
            return None
            

    def unassociate_plot(
        self,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        experiment_name: str = None,
        season_name: str = None
    ):
        try:
            from gemini.api.plot import Plot
            plot = Plot.get(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name
            )
            if not plot:
                print(f"Plot {plot_number} does not exist.")
                return None
            plot.unassociate_site()
            return plot
        except Exception as e:
            print(f"Error unassociating plot: {e}")
            return None
        

    def belongs_to_plot(
        self,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        experiment_name: str = None,
        season_name: str = None
    ):
        try:
            from gemini.api.plot import Plot
            plot = Plot.get(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name
            )
            if not plot:
                print(f"Plot {plot_number} does not exist.")
                return False
            association_exists = PlotViewModel.exists(
                site_id=self.id,
                plot_id=plot.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking plot membership: {e}")
            return False


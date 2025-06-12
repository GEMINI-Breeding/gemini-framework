from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices, computed_field
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.cultivar import Cultivar
from gemini.api.plant import Plant

from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.cultivars import CultivarModel
from gemini.db.models.plots import PlotModel

from gemini.db.models.views.experiment_views import (
    ExperimentSeasonsViewModel,
    ExperimentSitesViewModel,
    ExperimentCultivarsViewModel
)
from gemini.db.models.associations import PlotCultivarModel
from gemini.db.models.views.plot_cultivar_view import PlotCultivarViewModel
from gemini.db.models.views.plot_view import PlotViewModel
from gemini.db.models.views.plot_plant_view import PlotPlantViewModel
from gemini.db.models.views.validation_views import ValidPlotCombinationsViewModel

class Plot(APIBase):


    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "plot_id"))
    plot_number: int
    plot_row_number: int
    plot_column_number: int
    plot_geometry_info: Optional[dict] = None
    plot_info: Optional[dict] = None
    experiment_id: Optional[ID] = None
    season_id: Optional[ID] = None
    site_id: Optional[ID] = None

    experiment_name: Optional[str] = Field(None, exclude=True)
    season_name: Optional[str] = Field(None, exclude=True)
    site_name: Optional[str] = Field(None, exclude=True)

    def __str__(self):
        return f"Plot(number={self.plot_number}, row={self.plot_row_number}, column={self.plot_column_number}, id={self.id})"
    
    def __repr__(self):
        return f"Plot(plot_number={self.plot_number}, plot_row_number={self.plot_row_number}, plot_column_number={self.plot_column_number}, id={self.id})"
    
    @classmethod
    def exists(
        cls,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None
    ) -> bool:
        try:
            exists = PlotViewModel.exists(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            return exists
        except Exception as e:
            print(f"Error checking existence of plot: {e}")
            return False
        
    @classmethod
    def create(
        cls,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        plot_info: dict = {},
        plot_geometry_info: dict = {},
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        cultivar_accession: str = None,
        cultivar_population: str = None
    ) -> Optional["Plot"]:
        try:
            db_instance = PlotModel.get_or_create(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                plot_info=plot_info,
                plot_geometry_info=plot_geometry_info,
            )
            plot = cls.model_validate(db_instance)
            if experiment_name:
                plot.associate_experiment(experiment_name)
            if season_name:
                plot.associate_season(season_name, experiment_name)
            if site_name:
                plot.associate_site(site_name)
            if cultivar_accession and cultivar_population:
                plot.associate_cultivar(cultivar_accession, cultivar_population)
            return plot
        except Exception as e:
            print(f"Error creating plot: {e}")
            return None
        
    @classmethod
    def get(
        cls,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
    ) -> Optional["Plot"]:
        try:
            plot = PlotViewModel.get_by_parameters(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            if not plot:
                print(f"Plot with number {plot_number}, row {plot_row_number}, column {plot_column_number} not found.")
                return None
            plot = cls.model_validate(plot)
            return plot
        except Exception as e:
            print(f"Error getting plot: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["Plot"]:
        try:
            plot = PlotViewModel.get_by_parameters(plot_id=id)
            if not plot:
                print(f"Plot with ID {id} does not exist.")
                return None
            plot = cls.model_validate(plot)
            return plot
        except Exception as e:
            print(f"Error getting plot by ID: {e}")
            return None
        
    @classmethod
    def get_all(cls) -> Optional[List["Plot"]]:
        try:
            plots = PlotModel.all()
            if not plots or len(plots) == 0:
                print("No plots found.")
                return None
            plots = [cls.model_validate(plot) for plot in plots]
            return plots
        except Exception as e:
            print(f"Error getting all plots: {e}")
            return None
        
    @classmethod
    def search(
        cls,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        cultivar_accession: str = None,
        cultivar_population: str = None
    ) -> Optional[List["Plot"]]:
        try:
            if not any([plot_number, plot_row_number, plot_column_number, experiment_name, season_name, site_name]):
                print("At least one search parameter must be provided.")
                return None

            plots = PlotViewModel.search(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population
            )
            if not plots or len(plots) == 0:
                print("No plots found with the provided search parameters.")
                return None
            plots = [cls.model_validate(plot) for plot in plots]
            return plots if plots else None
        except Exception as e:
            print(f"Error searching plots: {e}")
            return None
        
    def update(
        self,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        plot_info: dict = None,
        plot_geometry_info: dict = None
    ) -> Optional["Plot"]:
        try:
            if not any([plot_number, plot_row_number, plot_column_number, plot_info, plot_geometry_info]):
                print("At least one parameter must be provided.")
                return None

            current_id = self.id
            plot = PlotModel.get(current_id)
            if not plot:
                print(f"Plot with ID {current_id} does not exist.")
                return None
            plot = PlotModel.update(
                plot,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                plot_info=plot_info,
                plot_geometry_info=plot_geometry_info
            )
            plot = self.model_validate(plot)
            self.refresh()
            return plot
        except Exception as e:
            print(f"Error updating plot: {e}")
            return None
        
    def refresh(self) -> Optional["Plot"]:
        try:
            db_instance = PlotViewModel.get_by_parameters(plot_id=self.id)
            if not db_instance:
                print(f"Plot with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            instance_dict = dict(instance)
            for key, value in instance_dict.items():
                if hasattr(self, key) and key != "id":
                    value = getattr(instance, key)
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing plot: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            plot = PlotModel.get(current_id)
            if not plot:
                print(f"Plot with ID {current_id} does not exist.")
                return False
            PlotModel.delete(plot)
            return True
        except Exception as e:
            print(f"Error deleting plot: {e}")
            return False
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            plot = PlotModel.get(current_id)
            if not plot:
                print(f"Plot with ID {current_id} does not exist.")
                return None
            plot_info = plot.plot_info
            if not plot_info:
                print("Plot info is empty.")
                return None
            return plot_info
        except Exception as e:
            print(f"Error getting plot info: {e}")
            return None
        
    def set_info(self, plot_info: dict) -> Optional["Plot"]:
        try:
            current_id = self.id
            plot = PlotModel.get(current_id)
            if not plot:
                print(f"Plot with ID {current_id} does not exist.")
                return None
            plot = PlotModel.update(
                plot,
                plot_info=plot_info
            )
            plot = self.model_validate(plot)
            self.refresh()
            return self
        except Exception as e:
            print(f"Error setting plot info: {e}")  
            return None
        
    def get_associated_experiment(self):
        try:
            from gemini.api.experiment import Experiment
            if not self.experiment_id:
                print("Plot does not belong to any experiment.")
                return None
            experiment = Experiment.get_by_id(self.experiment_id)
            if not experiment:
                print(f"Experiment with ID {self.experiment_id} does not exist.")
                return None
            return experiment
        except Exception as e:
            print(f"Error getting experiment: {e}")
            return None


    def belongs_to_experiment(self, experiment_name: str) -> bool:
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment with name {experiment_name} does not exist.")
                return False
            association_exists = PlotViewModel.exists(
                plot_id=self.id,
                experiment_id=experiment.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if plot belongs to experiment: {e}")
            return False

    def associate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment with name {experiment_name} does not exist.")
                return None
            existing_association = PlotViewModel.get_by_parameters(
                plot_id=self.id,
                experiment_id=experiment.id
            )
            if existing_association:
                print(f"Plot {self.id} is already associated with experiment {experiment_name}.")
                return self
            db_plot = PlotModel.get(self.id)
            db_plot = PlotModel.update_parameter(
                db_plot,
                "experiment_id",
                experiment.id
            )
            print(f"Plot {self.id} associated with experiment {experiment_name}.")
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error assigning experiment to plot: {e}")
            return None

    def unassociate_experiment(self):
        try:
            from gemini.api.experiment import Experiment
            if not self.experiment_id:
                print("Plot does not belong to any experiment.")
                return None
            experiment = Experiment.get_by_id(self.experiment_id)
            db_plot = PlotModel.get(self.id)
            db_plot = PlotModel.update_parameter(
                db_plot,
                "experiment_id",
                None
            )
            self.refresh()
            return experiment   
        except Exception as e:
            print(f"Error unassigning experiment from plot: {e}")
            return None

    def get_associated_season(self):
        try:
            from gemini.api.season import Season
            if not self.season_id:
                print("Plot does not belong to any season.")
                return None
            season = Season.get_by_id(self.season_id)
            if not season:
                print(f"Season with ID {self.season_id} does not exist.")
                return None
            return season
        except Exception as e:
            print(f"Error getting season: {e}")
            return None
        

    def belongs_to_season(self, season_name: str, experiment_name: str) -> bool:
        try:
            from gemini.api.season import Season
            from gemini.api.experiment import Experiment
            season = Season.get(season_name=season_name, experiment_name=experiment_name)
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment or not season:
                print(f"Experiment with name {experiment_name} or season with name {season_name} does not exist.")
                return False
            association_exists = PlotViewModel.exists(
                plot_id=self.id,
                season_id=self.season_id,
                experiment_id=experiment.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if plot belongs to season: {e}")
            return False

    def associate_season(self, season_name: str, experiment_name: str):
        try:
            from gemini.api.season import Season
            season = Season.get(season_name=season_name, experiment_name=experiment_name)
            if not season:
                print(f"Season with name {season_name} does not exist.")
                return None
            existing_association = PlotViewModel.get_by_parameters(
                plot_id=self.id,
                season_id=season.id,
                experiment_id=season.experiment_id
            )
            if existing_association:
                print(f"Plot {self.id} is already associated with season {season_name}.")
                return self
            db_plot = PlotModel.get(self.id)
            db_plot = PlotModel.update_parameter(
                db_plot,
                "season_id",
                season.id
            )
            print(f"Plot {self.id} associated with season {season_name}.")
            self.refresh()
            return season
        except Exception as e:
            print(f"Error assigning season to plot: {e}")
            return None

    def unassociate_season(self):
        try:
            from gemini.api.season import Season
            if not self.season_id:
                print("Plot does not belong to any season.")
                return None
            season = Season.get_by_id(self.season_id)
            db_plot = PlotModel.get(self.id)
            db_plot = PlotModel.update_parameter(
                db_plot,
                "season_id",
                None
            )
            self.refresh()
            return season
        except Exception as e:
            print(f"Error unassigning season from plot: {e}")
            return None
        
    def get_associated_site(self):
        try:
            from gemini.api.site import Site
            if not self.site_id:
                print("Plot does not belong to any site.")
                return None
            site = Site.get_by_id(self.site_id)
            if not site:
                print(f"Site with ID {self.site_id} does not exist.")
                return None
            return site
        except Exception as e:
            print(f"Error getting site: {e}")
            return None

    def belongs_to_site(self, site_name: str) -> bool:
        try:
            from gemini.api.site import Site
            site = Site.get(site_name=site_name)
            if not site:
                print(f"Site with name {site_name} does not exist.")
                return False
            association_exists = PlotViewModel.exists(
                plot_id=self.id,
                site_id=site.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if plot belongs to site: {e}")
            return False

    def associate_site(self, site_name: str):
        try:
            from gemini.api.site import Site
            site = Site.get(site_name=site_name)
            if not site:
                print(f"Site with name {site_name} does not exist.")
                return None
            existing_association = PlotViewModel.get_by_parameters(
                plot_id=self.id,
                site_id=site.id
            )
            if existing_association:
                print(f"Plot {self.id} is already associated with site {site_name}.")
                return self
            db_plot = PlotModel.get(self.id)
            db_plot = PlotModel.update_parameter(
                db_plot,
                "site_id",
                site.id
            )
            print(f"Plot {self.id} associated with site {site_name}.")
            self.refresh()
            return site
        except Exception as e:
            print(f"Error assigning site to plot: {e}")
            return None

    def unassociate_site(self):
        try:
            from gemini.api.site import Site
            if not self.site_id:
                print("Plot does not belong to any site.")
                return None
            site = Site.get_by_id(self.site_id)
            db_plot = PlotModel.get(self.id)
            db_plot = PlotModel.update_parameter(
                db_plot,
                "site_id",
                None
            )
            self.refresh()
            return site
        except Exception as e:
            print(f"Error unassigning site from plot: {e}")
            return None

    def get_associated_cultivars(self):
        try:
            from gemini.api.cultivar import Cultivar
            cultivars = PlotCultivarViewModel.search(plot_id=self.id)
            if not cultivars or len(cultivars) == 0:
                print("No associated cultivars found for this plot.")
                return None
            cultivars = [Cultivar.model_validate(cultivar) for cultivar in cultivars]
            return cultivars
        except Exception as e:
            print(f"Error getting associated cultivars: {e}")
            return None

    def associate_cultivar(
        self,
        cultivar_accession: str,
        cultivar_population: str
    ):
        try:
            from gemini.api.cultivar import Cultivar
            cultivar = Cultivar.get(
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population
            )
            if not cultivar:
                print(f"Cultivar {cultivar_accession} {cultivar_population} does not exist.")
                return None
            existing_association = PlotCultivarViewModel.get_by_parameters(
                plot_id=self.id,
                cultivar_id=cultivar.id
            )
            if existing_association:
                print(f"Cultivar {cultivar_accession} {cultivar_population} is already assigned to this plot.")
                return self
            new_association = PlotCultivarModel.get_or_create(
                plot_id=self.id,
                cultivar_id=cultivar.id
            )
            if not new_association:
                print(f"Failed to assign cultivar {cultivar_accession} {cultivar_population} to plot {self.id}.")
                return None
            self.refresh()
            return cultivar
        except Exception as e:
            print(f"Error assigning cultivar to plot: {e}")
            return None

    def unassociate_cultivar(
        self,
        cultivar_accession: str,
        cultivar_population: str
    ):
        try:
            from gemini.api.cultivar import Cultivar
            cultivar = Cultivar.get(
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population
            )
            if not cultivar:
                print(f"Cultivar {cultivar_accession} {cultivar_population} does not exist.")
                return None
            existing_association = PlotCultivarModel.get_by_parameters(
                plot_id=self.id,
                cultivar_id=cultivar.id
            )
            if not existing_association:
                print(f"Cultivar {cultivar_accession} {cultivar_population} is not assigned to this plot.")
                return None
            is_deleted = PlotCultivarModel.delete(existing_association)
            if not is_deleted:
                print(f"Failed to unassign cultivar {cultivar_accession} {cultivar_population} from plot {self.id}.")
                return None
            self.refresh()
            return cultivar
        except Exception as e:
            print(f"Error unassigning cultivar from plot: {e}")
            return None

    def belongs_to_cultivar(
        self,
        cultivar_accession: str,
        cultivar_population: str
    ) -> bool:
        try:
            from gemini.api.cultivar import Cultivar
            cultivar = Cultivar.get(
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population
            )
            if not cultivar:
                print(f"Cultivar {cultivar_accession} {cultivar_population} does not exist.")
                return False
            association_exists = PlotCultivarViewModel.exists(
                plot_id=self.id,
                cultivar_id=cultivar.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if plot has cultivar: {e}")
            return False 
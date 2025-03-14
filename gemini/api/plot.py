from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
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
    experiment_id: ID
    season_id: ID
    site_id: ID
    plot_number: int
    plot_row_number: int
    plot_column_number: int
    plot_geometry_info: Optional[dict] = None
    plot_info: Optional[dict] = None

    experiment_name: Optional[str] = Field(None, exclude=True)
    season_name: Optional[str] = Field(None, exclude=True)
    site_name: Optional[str] = Field(None, exclude=True)
    
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
    ) -> "Plot":
        try:

            if not all([experiment_name, season_name, site_name]):
                raise ValueError("Experiment, season and site names must be provided.")

            # Check if experiment, season and site are valid
            valid_combination = ValidPlotCombinationsViewModel.get_by_parameters(
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            if not valid_combination:
                raise ValueError(f"Invalid combination of experiment, season and site.")

           
            db_instance = PlotModel.get_or_create(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                plot_info=plot_info,
                plot_geometry_info=plot_geometry_info,
                experiment_id=valid_combination.experiment_id,
                site_id=valid_combination.site_id,
                season_id=valid_combination.season_id
            )

            if cultivar_accession and cultivar_population:

                 # Check if cultivar is part of the experiment
                if not ExperimentCultivarsViewModel.exists(
                    experiment_name=experiment_name,
                    cultivar_accession=cultivar_accession,
                    cultivar_population=cultivar_population
                ):
                    raise ValueError(f"Cultivar {cultivar_accession} {cultivar_population} is not part of the experiment {experiment_name}.")


                db_cultivar = CultivarModel.get_by_parameters(
                    cultivar_accession=cultivar_accession,
                    cultivar_population=cultivar_population
                )
                if db_cultivar:
                    PlotCultivarModel.get_or_create(
                        plot_id=db_instance.id,
                        cultivar_id=db_cultivar.id
                    )
            plot = cls.model_validate(db_instance)
            return plot
        except Exception as e:
            raise e
        
    @classmethod
    def get(
        cls,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
    ) -> "Plot":
        try:
            if not any([plot_number, plot_row_number, plot_column_number, experiment_name, season_name, site_name]):
                raise ValueError("At least one search parameter must be provided.")

            plot = PlotViewModel.get_by_parameters(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            plot = cls.model_validate(plot) if plot else None
            return plot
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Plot":
        try:
            plot = PlotViewModel.get_by_parameters(plot_id=id)
            if not plot:
                raise ValueError(f"Plot with ID {id} does not exist.")
            plot = cls.model_validate(plot) if plot else None
            return plot
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["Plot"]:
        try:
            plots = PlotModel.all()
            plots = [cls.model_validate(plot) for plot in plots]
            return plots if plots else None
        except Exception as e:
            raise e
        

    @classmethod
    def search(cls,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
    ) -> List["Plot"]:
        try:
            if not any([plot_number, plot_row_number, plot_column_number, experiment_name, season_name, site_name]):
                raise ValueError("At least one search parameter must be provided.")

            plots = PlotViewModel.search(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            plots = [cls.model_validate(plot) for plot in plots]
            return plots if plots else None
        except Exception as e:
            raise e
        

    def update(
        self,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        plot_info: dict = None,
        plot_geometry_info: dict = None
    ) -> "Plot":
        try:
            if not plot_number and not plot_row_number and not plot_column_number and not plot_info:
                raise ValueError("At least one parameter must be provided.")

            current_id = self.id
            plot = PlotModel.get(current_id)
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
            return None
        

    def refresh(self) -> "Plot":
        try:
            db_instance = PlotViewModel.get_by_parameters(plot_id=self.id)
            instance = self.model_validate(db_instance)
            instance_dict = dict(instance)
            for key, value in instance_dict.items():
                if hasattr(self, key) and key != "id":
                    value = getattr(instance, key)
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e
        

    def delete(self) -> bool:
        try:
            current_id = self.id
            plot = PlotModel.get(current_id)
            PlotModel.delete(plot)
            return True
        except Exception as e:
            return False
        

    @classmethod
    def get_valid_combinations(cls) -> List[dict]:
        try:
            valid_combinations = ValidPlotCombinationsViewModel.all()
            valid_combinations = [valid_combinations.to_dict() for valid_combinations in valid_combinations]
            return valid_combinations if valid_combinations else None
        except Exception as e:
            raise e
        
    def get_cultivars(self) -> List["Cultivar"]:
        try:
            cultivars = PlotCultivarViewModel.search(plot_id=self.id)
            cultivars = [Cultivar.model_validate(cultivar) for cultivar in cultivars]
            return cultivars if cultivars else None
        except Exception as e:
            raise e
        
    def add_cultivar(
        self,
        cultivar_accession: str,
        cultivar_population: str,
        cultivar_info: dict = {}
    ) -> "Cultivar":
        try:

            # Check if cultivar is part of the experiment
            if not ExperimentCultivarsViewModel.exists(
                experiment_id=self.experiment_id,
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population
            ):
                return None
            # Check if it is already added for the plot
            if PlotCultivarViewModel.exists(plot_id=self.id, cultivar_accession=cultivar_accession, cultivar_population=cultivar_population):
                return None
            
            cultivar = Cultivar.create(
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
                cultivar_info=cultivar_info
            )
            plot = PlotModel.get(self.id)
            plot = PlotCultivarModel.get_or_create(
                plot_id=plot.id,
                cultivar_id=cultivar.id
            )
            cultivar = Cultivar.model_validate(cultivar)
            return cultivar
        except Exception as e:
            raise e
        
        
    def set_experiment(self, experiment_name: str) -> "Plot":
        try:
            experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
            if not experiment:
                raise ValueError(f"Experiment with name {experiment_name} does not exist.")
            plot = PlotModel.get(self.id)
            PlotModel.update(plot, experiment_id=experiment.id)
            self.refresh()
            return self
        except Exception as e:
            return None
        

    def set_season(self, experiment_name: str, season_name: str) -> "Plot":
        try:
            season = ExperimentSeasonsViewModel.get_by_parameters(
                experiment_name=experiment_name,
                season_name=season_name
            )
            if not season:
                raise ValueError(f"Season with name {season_name} does not exist for experiment {experiment_name}.")
            plot = PlotModel.get(self.id)
            PlotModel.update(plot, season_id=season.season_id)
            self.refresh()
            return plot
        except Exception as e:
            return None
        
    def set_site(self, site_name: str) -> "Plot":
        try:
            site = ExperimentSitesViewModel.get_by_parameters(
                experiment_name=self.experiment_name,
                site_name=site_name
            )
            if not site:
                raise ValueError(f"Site with name {site_name} does not exist for experiment {self.experiment_name}.")
            plot = PlotModel.get(self.id)
            PlotModel.update(plot, site_id=site.site_id)
            self.refresh()
            return self
        except Exception as e:
            return None
        
    def get_plants(self) -> List["Plant"]:
        try:
            plants = PlotPlantViewModel.search(plot_id=self.id)
            plants = [Plant.model_validate(plant) for plant in plants]
            return plants if plants else None
        except Exception as e:
            raise e
        
    def add_plant(
        self,
        plant_number: int,
        cultivar_accession: str,
        cultivar_population: str,
        plant_info: dict = {}
    ) -> "Plant":
        try:
            # Check if cultivar is part of the experiment
            if not ExperimentCultivarsViewModel.exists(
                experiment_id=self.experiment_id,
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population
            ):
                raise ValueError(f"Cultivar {cultivar_accession} {cultivar_population} is not part of the experiment {self.experiment_name}.")

            plant = Plant.create(
                plot_id=self.id,
                plant_number=plant_number,
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
                plant_info=plant_info
            )
            return plant
        except Exception as e:
            raise e
        

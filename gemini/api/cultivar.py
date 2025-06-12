from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.cultivars import CultivarModel
from gemini.db.models.associations import ExperimentCultivarModel, PlotCultivarModel
from gemini.db.models.views.experiment_views import ExperimentCultivarsViewModel
from gemini.db.models.views.plot_cultivar_view import PlotCultivarViewModel
from gemini.db.models.views.plant_view import PlantViewModel

class Cultivar(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "cultivar_id"))

    cultivar_population: str
    cultivar_accession: Optional[str] = None
    cultivar_info: Optional[dict] = None

    def __str__(self):
        return f"Cultivar(population={self.cultivar_population}, accession={self.cultivar_accession}, id={self.id})"

    def __repr__(self):
        return f"Cultivar(cultivar_population={self.cultivar_population}, cultivar_accession={self.cultivar_accession}, id={self.id})"

    @classmethod
    def exists(
        cls,
        cultivar_population: str,
        cultivar_accession: str,
    ) -> bool:
        try:
            exists = CultivarModel.exists(
                cultivar_population=cultivar_population,
                cultivar_accession=cultivar_accession,
            )
            return exists
        except Exception as e:
            print(f"Error checking the existence of cultivar: {e}")
            return False

    @classmethod
    def create(
        cls,
        cultivar_population: str,
        cultivar_accession: str,
        cultivar_info: dict = {},
        experiment_name: str = None
    ) -> Optional["Cultivar"]:
        try:
            db_instance = CultivarModel.get_or_create(
                cultivar_population=cultivar_population,
                cultivar_accession=cultivar_accession,
                cultivar_info=cultivar_info,
            )
            cultivar = cls.model_validate(db_instance)
            # Associate with experiment if provided
            if experiment_name:
                cultivar.associate_experiment(experiment_name)
            return cultivar
        except Exception as e:
            print(f"Error creating cultivar: {e}")
            return None
        
    @classmethod
    def get(cls, cultivar_population: str, cultivar_accession: str, experiment_name: str = None) -> Optional["Cultivar"]:
        try:
            db_instance = ExperimentCultivarsViewModel.get_by_parameters(
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
                experiment_name=experiment_name,
            )
            if not db_instance:
                print(f"Cultivar with accession {cultivar_accession} and population {cultivar_population} not found.")
                return None
            cultivar = cls.model_validate(db_instance)
            return cultivar
        except Exception as e:
            print(f"Error getting cultivar: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["Cultivar"]:
        try:
            db_instance = CultivarModel.get(id)
            if not db_instance:
                print(f"Cultivar with ID {id} does not exist.")
                return None
            cultivar = cls.model_validate(db_instance)
            return cultivar
        except Exception as e:
            print(f"Error getting cultivar by ID: {e}")
            return None
        
    @classmethod
    def get_all(cls) -> Optional[List["Cultivar"]]:
        try:
            cultivars = CultivarModel.all()
            if not cultivars or len(cultivars) == 0:
                print("No cultivars found.")
                return None
            cultivars = [cls.model_validate(cultivar) for cultivar in cultivars]
            return cultivars
        except Exception as e:
            print(f"Error getting all cultivars: {e}")
            return None
        
    @classmethod
    def search(
        cls, 
        cultivar_population: str = None,
        cultivar_accession: str = None,
        cultivar_info: dict = None,
        experiment_name: str = None
    ) -> Optional[List["Cultivar"]]:
        try:
            if not any([experiment_name, cultivar_population, cultivar_accession, cultivar_info]):
                print("At least one search parameter must be provided.")
                return None
            cultivars = ExperimentCultivarsViewModel.search(
                experiment_name=experiment_name,
                cultivar_population=cultivar_population,
                cultivar_accession=cultivar_accession,
                cultivar_info=cultivar_info,
            )
            if not cultivars or len(cultivars) == 0:
                print("No cultivars found with the provided search parameters.")
                return None
            cultivars = [cls.model_validate(cultivar) for cultivar in cultivars]
            return cultivars
        except Exception as e:
            print(f"Error searching cultivars: {e}")
            return None
        
    def update(
        self,
        cultivar_accession: str = None,
        cultivar_population: str = None,
        cultivar_info: dict = None,
    ) -> Optional["Cultivar"]:
        try:
            if not any([cultivar_accession, cultivar_population, cultivar_info]):
                print("At least one parameter must be provided for update.")
                return None
            
            current_id = self.id
            cultivar = CultivarModel.get(current_id)
            if not cultivar:
                print(f"Cultivar with ID {current_id} does not exist.")
                return None
            cultivar = CultivarModel.update(
                cultivar,
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
                cultivar_info=cultivar_info,
            )
            cultivar = self.model_validate(cultivar)
            self.refresh()
            return cultivar
        except Exception as e:
            print(f"Error updating cultivar: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            cultivar = CultivarModel.get(current_id)
            if not cultivar:
                print(f"Cultivar with ID {current_id} does not exist.")
                return False
            CultivarModel.delete(cultivar)
            return True
        except Exception as e:
            return False
        
    
    def refresh(self) -> Optional["Cultivar"]:
        try:
            db_instance = CultivarModel.get(self.id)
            if not db_instance:
                print(f"Cultivar with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing cultivar: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            cultivar = CultivarModel.get(current_id)
            if not cultivar:
                print(f"Cultivar with ID {current_id} does not exist.")
                return None
            cultivar_info = cultivar.cultivar_info
            if not cultivar_info:
                print("Cultivar info is empty.")
                return None
            return cultivar_info
        except Exception as e:
            print(f"Error getting cultivar info: {e}")
            return None
        
    def set_info(self, cultivar_info: dict) -> Optional["Cultivar"]:
        try:
            current_id = self.id
            cultivar = CultivarModel.get(current_id)
            if not cultivar:
                print(f"Cultivar with ID {current_id} does not exist.")
                return None
            cultivar = CultivarModel.update(
                cultivar,
                cultivar_info=cultivar_info
            )
            cultivar = self.model_validate(cultivar)
            self.refresh()
            return cultivar
        except Exception as e:
            print(f"Error setting cultivar info: {e}")
            return None

    def get_associated_experiments(self):
        try:
            from gemini.api.experiment import Experiment
            current_id = self.id
            experiment_cultivars = ExperimentCultivarsViewModel.search(cultivar_id=current_id)
            if not experiment_cultivars or len(experiment_cultivars) == 0:
                print("No associated experiments found.")
                return None
            experiments = [Experiment.model_validate(experiment_cultivar) for experiment_cultivar in experiment_cultivars]
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
            existing_association = ExperimentCultivarModel.get_by_parameters(
                experiment_id=experiment.id,
                cultivar_id=self.id
            )
            if existing_association:
                print(f"Cultivar {self.cultivar_population} is already associated with experiment {experiment_name}.")
                return experiment
            new_association = ExperimentCultivarModel.get_or_create(
                experiment_id=experiment.id,
                cultivar_id=self.id
            )
            if not new_association:
                print(f"Failed to associate cultivar {self.cultivar_population} with experiment {experiment_name}.")
                return None
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error associating cultivar with experiment: {e}")
            return None
        
    def unassociate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return None
            existing_association = ExperimentCultivarModel.get_by_parameters(
                experiment_id=experiment.id,
                cultivar_id=self.id
            )
            if not existing_association:
                print(f"Cultivar {self.cultivar_population} is not associated with experiment {experiment_name}.")
                return None
            is_deleted = ExperimentCultivarModel.delete(existing_association)
            if not is_deleted:
                print(f"Failed to unassociate cultivar {self.cultivar_population} from experiment {experiment_name}.")
                return None
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error unassociating cultivar from experiment: {e}")
            return None

    def belongs_to_experiment(self, experiment_name: str) -> bool:
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return False
            association_exists = ExperimentCultivarModel.exists(
                experiment_id=experiment.id,
                cultivar_id=self.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if cultivar belongs to experiment: {e}")
            return False

    def get_associated_plots(self):
        try:
            from gemini.api.plot import Plot
            current_id = self.id
            plot_cultivars = PlotCultivarViewModel.search(cultivar_id=current_id)
            if not plot_cultivars or len(plot_cultivars) == 0:
                print("No associated plots found.")
                return None
            plots = [Plot.model_validate(plot_cultivar) for plot_cultivar in plot_cultivars]
            return plots
        except Exception as e:
            print(f"Error getting associated plots: {e}")
            return None

    def associate_plot(
        self,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None
    ):
        try:
            from gemini.api.plot import Plot
            plot = Plot.get(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            if not plot:
                print(f"Plot {plot_number} does not exist.")
                return None
            existing_association = PlotCultivarModel.get_by_parameters(
                plot_id=plot.id,
                cultivar_id=self.id
            )
            if existing_association:
                print(f"Cultivar {self.cultivar_population} is already associated with plot {plot_number}.")
                return plot
            new_association = PlotCultivarModel.get_or_create(
                plot_id=plot.id,
                cultivar_id=self.id
            )
            if not new_association:
                print(f"Failed to associate cultivar {self.cultivar_population} with plot {plot_number}.")
                return None
            self.refresh()
            return plot
        except Exception as e:
            print(f"Error associating cultivar with plot: {e}")
            return None

    def unassociate_plot(
        self,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None
    ):
        try:
            from gemini.api.plot import Plot
            plot = Plot.get(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            if not plot:
                print(f"Plot {plot_number} does not exist.")
                return None
            existing_association = PlotCultivarModel.get_by_parameters(
                plot_id=plot.id,
                cultivar_id=self.id
            )
            if not existing_association:
                print(f"Cultivar {self.cultivar_population} is not associated with plot {plot_number}.")
                return None
            is_deleted = PlotCultivarModel.delete(existing_association)
            if not is_deleted:
                print(f"Failed to unassociate cultivar {self.cultivar_population} from plot {plot_number}.")
                return None
            self.refresh()
            return plot
        except Exception as e:
            print(f"Error unassociating cultivar from plot: {e}")
            return None

    def belongs_to_plot(
        self,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None
    ) -> bool:
        try:
            from gemini.api.plot import Plot
            plot = Plot.get(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            if not plot:
                print(f"Plot {plot_number} does not exist.")
                return False
            association_exists = PlotCultivarModel.exists(
                plot_id=plot.id,
                cultivar_id=self.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if cultivar belongs to plot: {e}")
            return False
        
    def get_associated_plants(self):
        try:
            from gemini.api.plant import Plant
            current_id = self.id
            cultivar_plants = PlantViewModel.search(cultivar_id=current_id)
            if not cultivar_plants or len(cultivar_plants) == 0:
                print("No associated plants found.")
                return None
            plants = [Plant.model_validate(cultivar_plant) for cultivar_plant in cultivar_plants]
            return plants
        except Exception as e:
            print(f"Error getting associated plants: {e}")
            return None


    def belongs_to_plant(
        self,
        plant_number: int,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None
    ) -> bool:
        try:
            from gemini.api.plant import Plant
            plant = Plant.get(
                plant_number=plant_number,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            if not plant:
                print(f"Plant {plant_number} does not exist.")
                return False
            association_exists = PlantViewModel.exists(
                plant_id=plant.id,
                cultivar_id=self.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if cultivar belongs to plant: {e}")
            return False


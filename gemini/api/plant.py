from typing import List, Optional
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.cultivar import Cultivar
from gemini.db.models.views.plot_view import PlotViewModel
from gemini.db.models.plants import PlantModel
from gemini.db.models.cultivars import CultivarModel
from gemini.db.models.views.plant_view import PlantViewModel

class Plant(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "plant_id"))

    plant_number: int
    plant_info: Optional[dict] = None
    plot_id: Optional[UUID] = None
    cultivar_id: Optional[UUID] = None

    def __str__(self):
        return f"Plant(plot_id={self.plot_id}, plant_number={self.plant_number}, plant_info={self.plant_info}, id={self.id})"

    def __repr__(self):
        return f"Plant(plot_id={self.plot_id}, plant_number={self.plant_number}, plant_info={self.plant_info}, id={self.id})"

    @classmethod
    def exists(
        cls,
        plant_number: int,
        cultivar_accession: str = None,
        cultivar_population: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
    ) -> bool:
        try:
            exists = PlantViewModel.exists(
                plant_number=plant_number,
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number
            )
            return exists
        except Exception as e:
            print(f"Error checking existence of plant: {e}")
            return False
        
    @classmethod
    def create(
        cls,
        plant_number: int,
        plant_info: dict = None,
        cultivar_accession: str = None,
        cultivar_population: str = None,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None
    ) -> "Plant":
        try:
            db_instance = PlantModel.get_or_create(
                plant_number=plant_number,
                plant_info=plant_info
            )
            plant = cls.model_validate(db_instance)
            if all([cultivar_accession, cultivar_population]):
                plant.associate_cultivar(
                    cultivar_accession=cultivar_accession,
                    cultivar_population=cultivar_population
                )
            if all([plot_number, plot_row_number, plot_column_number, experiment_name, season_name, site_name]):
                plant.associate_plot(
                    plot_number=plot_number,
                    plot_row_number=plot_row_number,
                    plot_column_number=plot_column_number,
                    experiment_name=experiment_name,
                    season_name=season_name,
                    site_name=site_name
                )
            return plant
        except Exception as e:
            print(f"Error creating plant: {e}")
            return None
        
    @classmethod
    def get(
        cls,
        plant_number: int,
        cultivar_accession: str = None,
        cultivar_population: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None
    ) -> Optional["Plant"]:
        try:
            db_instance = PlantViewModel.get_by_parameters(
                plant_number=plant_number,
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number
            )
            if not db_instance:
                print(f"Plant with number {plant_number} not found.")
                return None
            plant = cls.model_validate(db_instance) if db_instance else None
            return plant
        except Exception as e:
            print(f"Error getting plant: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["Plant"]:
        try:
            db_instance = PlantModel.get(id)
            if not db_instance:
                print(f"Plant with ID {id} does not exist.")
                return None
            plant = cls.model_validate(db_instance) if db_instance else None
            return plant
        except Exception as e:
            print(f"Error getting plant by ID: {e}")
            return None
        
    @classmethod
    def get_all(cls) -> Optional[List["Plant"]]:
        try:
            plants = PlantModel.all()
            if not plants or len(plants) == 0:
                print("No plants found.")
                return None
            plants = [cls.model_validate(plant) for plant in plants]
            return plants
        except Exception as e:
            print(f"Error getting all plants: {e}")
            return None
        
    @classmethod
    def search(
        cls, 
        plant_number: int = None,
        cultivar_accession: str = None,
        cultivar_population: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None
    ) -> Optional[List["Plant"]]:
        try:
            if not any([plant_number, cultivar_accession, cultivar_population, experiment_name, season_name, site_name, plot_number, plot_row_number, plot_column_number]):
                print("At least one search parameter must be provided.")
                return None
            plants = PlantViewModel.search(
                plant_number=plant_number,
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number
            )
            if not plants or len(plants) == 0:
                print("No plants found with the provided search parameters.")
                return None
            plants = [cls.model_validate(plant) for plant in plants]
            return plants
        except Exception as e:
            print(f"Error searching for plants: {e}")
            return None
        
    def update(
        self,
        plant_number: int = None,
        plant_info: dict = None
    ) -> Optional["Plant"]:
        try:
            if not plant_info and not plant_number:
                print("At least one parameter must be provided for update.")
                return None
            current_id = self.id
            plant = PlantModel.get(current_id)
            if not plant:
                print(f"Plant with ID {current_id} does not exist.")
                return None
            plant = PlantModel.update(
                plant,
                plant_number=plant_number,
                plant_info=plant_info
            )
            plant = self.model_validate(plant)
            self.refresh()  # Update the current instance
            return plant
        except Exception as e:
            print(f"Error updating plant: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            plant = PlantModel.get(current_id)
            if not plant:
                print(f"Plant with ID {current_id} does not exist.")
                return False
            PlantModel.delete(plant)
            return True
        except Exception as e:
            print(f"Error deleting plant: {e}")
            return False

    def refresh(self) -> Optional["Plant"]:
        try:
            db_instance = PlantModel.get(self.id)
            if not db_instance:
                print(f"Plant with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing plant: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            plant = PlantModel.get(current_id)
            if not plant:
                print(f"Plant with ID {current_id} does not exist.")
                return None
            plant_info = plant.plant_info
            if not plant_info:
                print("Plant info is empty.")
                return None
            return plant_info
        except Exception as e:
            print(f"Error getting plant info: {e}")
            return None
        
    def set_info(self, plant_info: dict) -> Optional["Plant"]:
        try:
            current_id = self.id
            plant = PlantModel.get(current_id)
            if not plant:
                print(f"Plant with ID {current_id} does not exist.")
                return None
            plant = PlantModel.update(
                plant,
                plant_info=plant_info
            )
            plant = self.model_validate(plant)
            self.refresh()  # Update the current instance
            return plant
        except Exception as e:
            print(f"Error setting plant info: {e}")
            return None
    
    def get_associated_cultivar(self):
        try:
            from gemini.api.cultivar import Cultivar
            if not self.cultivar_id:
                print("No cultivar assigned to this plant.")
                return None
            cultivar = Cultivar.get_by_id(self.cultivar_id)
            if not cultivar:
                print(f"Cultivar with ID {self.cultivar_id} does not exist.")
                return None
            return cultivar
        except Exception as e:
            print(f"Error getting cultivar: {e}")
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
                print(f"Cultivar with accession {cultivar_accession} and population {cultivar_population} not found.")
                return None
            existing_association = PlantModel.exists(
                id=self.id,
                cultivar_id=cultivar.id
            )
            if existing_association:
                print(f"Plant with ID {self.id} already has cultivar {cultivar.id} assigned.")
                return None
            db_plant = PlantModel.get(self.id)
            db_plant = PlantModel.update_parameter(
                db_plant,
                "cultivar_id",
                cultivar.id
            )
            print(f"Assigned cultivar {cultivar.id} to plant {self.id}.")
            self.refresh()
            return cultivar
        except Exception as e:
            print(f"Error assigning cultivar: {e}")
            return None

    def belongs_to_cultivar(
        self,
        cultivar_accession: str = None,
        cultivar_population: str = None
    ) -> bool:
        try:
            from gemini.api.cultivar import Cultivar
            cultivar = Cultivar.get(
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population
            )
            if not cultivar:
                print("Cultivar not found.")
                return False
            association_exists = PlantModel.exists(
                id=self.id,
                cultivar_id=cultivar.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking cultivar assignment: {e}")
            return False

    def unassociate_cultivar(self):
        try:
            from gemini.api.cultivar import Cultivar
            if not self.cultivar_id:
                print("No cultivar assigned to this plant.")
                return False
            cultivar = Cultivar.get_by_id(self.cultivar_id)
            db_plant = PlantModel.get(self.id)
            db_plant = PlantModel.update_parameter(
                db_plant,
                "cultivar_id",
                None
            )
            self.refresh()  # Update the current instance
            return cultivar
        except Exception as e:
            print(f"Error unassigning cultivar: {e}")
            return False

    def get_associated_plot(self):
        try:
            from gemini.api.plot import Plot
            if not self.plot_id:
                print("No plot assigned to this plant.")
                return None
            plot = Plot.get_by_id(self.plot_id)
            if not plot:
                print(f"Plot with ID {self.plot_id} does not exist.")
                return None
            return plot
        except Exception as e:
            print(f"Error getting plot: {e}")
            return None

    def associate_plot(
        self,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
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
                print("Plot not found.")
                return None
            existing_association = PlantModel.get_by_parameters(
                id=self.id,
                plot_id=plot.id
            )
            if existing_association:
                print(f"Plant with ID {self.id} already has plot {plot.id} assigned.")
                return None
            db_plant = PlantModel.get(self.id)
            db_plant = PlantModel.update_parameter(
                db_plant,
                "plot_id",
                plot.id
            )
            self.refresh()  # Update the current instance
            return plot
        except Exception as e:
            print(f"Error assigning plot: {e}")
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
                print("Plot not found.")
                return False
            association_exists = PlantModel.exists(
                id=self.id,
                plot_id=plot.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking plot assignment: {e}")
            return False

    def unassociate_plot(self):
        try:
            from gemini.api.plot import Plot
            if not self.plot_id:
                print("No plot assigned to this plant.")
                return None
            # Assuming we want to unassign the plot by setting plot_id to None
            plot = Plot.get_by_id(self.plot_id)
            db_plant = PlantModel.get(self.id)
            db_plant = PlantModel.update_parameter(
                db_plant,
                "plot_id",
                None
            )
            self.refresh()  # Update the current instance
            return plot
        except Exception as e:
            print(f"Error unassigning plot: {e}")
            return None
 
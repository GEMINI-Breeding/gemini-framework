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

    plot_id: UUID
    plant_number: int
    plant_info: Optional[dict] = None
    cultivar_id: UUID 

    @classmethod
    def create(
        cls,
        plot_id: UUID,
        plant_number: int,
        cultivar_accession: str,
        cultivar_population: str,
        plant_info: dict = {}
    ) -> "Plant":
        try:

            cultivar = CultivarModel.get_by_parameters(
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
            )

            db_instance = PlantModel.get_or_create(
                plot_id=plot_id,
                plant_number=plant_number,
                plant_info=plant_info,
                cultivar_id = cultivar.id if cultivar else None,
            )
            plant = cls.model_validate(db_instance)
            return plant
        except Exception as e:
            raise e
        

    @classmethod
    def get(cls, plot_id: UUID, plant_number: int) -> "Plant":
        try:
            db_instance = PlantModel.get_by_parameters(
                plot_id=plot_id,
                plant_number=plant_number,
            )
            plant = cls.model_validate(db_instance)
            return plant
        except Exception as e:
            raise e
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Plant":
        try:
            db_instance = PlantModel.get(id)
            plant = cls.model_validate(db_instance)
            return plant
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["Plant"]:
        try:
            plants = PlantModel.all()
            plants = [cls.model_validate(plant) for plant in plants]
            return plants if plants else None
        except Exception as e:
            raise e
        

    @classmethod
    def search(
        cls, 
        plot_id: UUID = None,
        plant_number: int = None,
        cultivar_accession: str = None,
        cultivar_population: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None
    ) -> List["Plant"]:
        try:
            if not any([plot_id, plant_number, cultivar_accession, cultivar_population, experiment_name, season_name, site_name]):
                raise ValueError("At least one search parameter must be provided.")

            plants = PlantViewModel.search(
                plot_id=plot_id,
                plant_number=plant_number,
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            plants = [cls.model_validate(plant) for plant in plants]
            return plants if plants else None
        except Exception as e:
            raise e
        

    def update(
        self,
        plant_number: int = None,
        plant_info: dict = None,

    ) -> "Plant":
        try:
            if not plant_number and not plant_info:
                raise ValueError("At least one parameter must be provided.")

            current_id = self.id
            plant = PlantModel.get(current_id)
            plant = PlantModel.update(
                plant,
                plant_number=plant_number,
                plant_info=plant_info
            )
            plant = self.model_validate(plant)
            self.refresh()
            return plant
        except Exception as e:
            raise e
        

    def delete(self) -> bool:
        try:
            current_id = self.id
            plant = PlantModel.get(current_id)
            PlantModel.delete(plant)
            return True
        except Exception as e:
            raise e
        

    def refresh(self) -> "Plant":
        try:
            db_instance = PlantModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e

    def get_cultivar(self) -> "Cultivar":
        try:
            if not self.cultivar_id:
                return None
            cultivar = CultivarModel.get(self.cultivar_id)
            cultivar = Cultivar.model_validate(cultivar)
            return cultivar
        except Exception as e:
            raise e
        
    def set_cultivar(
        self,
        cultivar_accession: str,
        cultivar_population: str
    ) -> "Plant":
        try:
            cultivar = CultivarModel.get_by_parameters(
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
            )
            if not cultivar:
                raise ValueError("Cultivar not found.")
            current_id = self.id
            plant = PlantModel.get(current_id)
            plant = PlantModel.update(plant, cultivar_id=cultivar.id)
            self.refresh()
            return self
        except Exception as e:
            raise e

    
from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.site import Site
from gemini.api.sensor import Sensor, GEMINISensorType, GEMINIDataType, GEMINIDataFormat
from gemini.api.season import Season
from gemini.api.cultivar import Cultivar
from gemini.api.dataset import Dataset
from gemini.api.trait import Trait, GEMINITraitLevel
from gemini.api.model import Model
from gemini.api.procedure import Procedure
from gemini.api.script import Script
from gemini.api.sensor_platform import SensorPlatform
from gemini.api.enums import GEMINIDatasetType

from gemini.db.models.experiments import ExperimentModel

from datetime import date


class Experiment(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "experiment_id"))

    experiment_name: str
    experiment_info: Optional[dict] = None
    experiment_start_date: Optional[date] = None
    experiment_end_date: Optional[date] = None

    seasons : Optional[List[Season]] = None
    sites : Optional[List[Site]] = None
    sensors : Optional[List[Sensor]] = None
    cultivars : Optional[List[Cultivar]] = None
    datasets : Optional[List[Dataset]] = None
    traits : Optional[List[Trait]] = None
    models : Optional[List[Model]] = None
    procedures : Optional[List[Procedure]] = None
    scripts : Optional[List[Script]] = None
    platforms : Optional[List[SensorPlatform]] = None

    


    @classmethod
    def create(
        cls,
        experiment_name: str,
        experiment_info: dict = {},
        experiment_start_date: date = date.today(),
        experiment_end_date: date = date.today(),
    ) -> "Experiment":
        try:
            db_instance = ExperimentModel.get_or_create(
                experiment_name=experiment_name,
                experiment_info=experiment_info,
                experiment_start_date=experiment_start_date,
                experiment_end_date=experiment_end_date,
            )
            experiment = cls.model_validate(db_instance)
            return experiment
        except Exception as e:
            raise e
        

    @classmethod
    def get(cls, experiment_name: str) -> "Experiment":
        try:
            db_instance = ExperimentModel.get_by_parameters(
                experiment_name=experiment_name,
            )
            experiment = cls.model_validate(db_instance)
            return experiment
        except Exception as e:
            raise e
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Experiment":
        try:
            db_instance = ExperimentModel.get(id)
            experiment = cls.model_validate(db_instance)
            return experiment
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["Experiment"]:
        try:
            experiments = ExperimentModel.all()
            experiments = [cls.model_validate(experiment) for experiment in experiments]
            return experiments
        except Exception as e:
            raise e

    @classmethod
    def search(cls, **search_parameters) -> List["Experiment"]:
        try:
            experiments = ExperimentModel.search(**search_parameters)
            experiments = [cls.model_validate(experiment) for experiment in experiments]
            return experiments if experiments else None
        except Exception as e:
            raise e
        
    def update(self, **kwargs) -> "Experiment":
        try:
            curent_id = self.id
            experiment = ExperimentModel.get(curent_id)
            experiment = ExperimentModel.update(experiment, **kwargs)
            experiment = self.model_validate(experiment)
            self.refresh()
            return experiment
        except Exception as e:
            raise e
        

    def refresh(self) -> "Experiment":
        try:
            db_instance = ExperimentModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    actual_value = getattr(instance, key)
                    setattr(self, key, actual_value)
            return self
        except Exception as e:
            raise e
        

    def delete(self) -> bool:
        try:
            current_id = self.id
            experiment = ExperimentModel.get(current_id)
            ExperimentModel.delete(experiment)
            return True
        except Exception as e:
            return False
        

    def get_seasons(self) -> List[Season]:
        try:
            seasons = self.seasons
            seasons = [Season.model_validate(season) for season in seasons]
            return seasons
        except Exception as e:
            raise e

    def create_season(
        self,
        season_name: str,
        season_info: dict = {},
        season_start_date: date = date.today(),
        season_end_date: date = date.today()
    ) -> Season:
        try:
            season = Season.create(
                season_name=season_name,
                season_info=season_info,
                season_start_date=season_start_date,
                season_end_date=season_end_date,
                experiment_name=self.experiment_name
            )
            self.refresh()
            return season
        except Exception as e:
            raise e

    def get_sites(self) -> List[Site]:
        try:
            sites = self.sites
            sites = [Site.model_validate(site) for site in sites]
            return sites
        except Exception as e:
            raise e
        

    def create_site(
        self,
        site_name: str,
        site_city: str,
        site_state: str,
        site_country: str,
        site_info: dict = {}
    ) -> Site:
        try:
            site = Site.create(
                site_name=site_name,
                site_city=site_city,
                site_state=site_state,
                site_country=site_country,
                site_info=site_info,
                experiment_name=self.experiment_name
            )
            self.refresh()
            return site
        except Exception as e:
            raise e
        
    def get_sensors(self) -> List[Sensor]:
        try:
            sensors = self.sensors
            sensors = [Sensor.model_validate(sensor) for sensor in sensors]
            return sensors
        except Exception as e:
            raise e
        
    def create_sensor(
        self,
        sensor_name: str,
        sensor_type: GEMINISensorType = GEMINISensorType.Default,
        sensor_data_type: GEMINIDataType = GEMINIDataType.Default,
        sensor_data_format: GEMINIDataFormat = GEMINIDataFormat.Default,
        sensor_info: dict = {},
        sensor_platform_name: str = None
    ) -> Sensor:
        try:
            sensor = Sensor.create(
                sensor_name=sensor_name,
                sensor_type=sensor_type,
                sensor_data_type=sensor_data_type,
                sensor_data_format=sensor_data_format,
                sensor_info=sensor_info,
                experiment_name=self.experiment_name,
                sensor_platform_name=sensor_platform_name
            )
            self.refresh()
            return sensor
        except Exception as e:
            raise e
        
    def get_cultivars(self) -> List[Cultivar]:
        try:
            cultivars = self.cultivars
            cultivars = [Cultivar.model_validate(cultivar) for cultivar in cultivars]
            return cultivars
        except Exception as e:
            raise e
        
    def create_cultivar(
        self,
        cultivar_population: str,
        cultivar_accession: str,
        cultivar_info: dict = {}
    ) -> Cultivar:
        try:
            cultivar = Cultivar.create(
                cultivar_population=cultivar_population,
                cultivar_accession=cultivar_accession,
                cultivar_info=cultivar_info,
                experiment_name=self.experiment_name
            )
            self.refresh()
            return cultivar
        except Exception as e:
            raise e
        
    def get_datasets(self) -> List[Dataset]:
        try:
            datasets = self.datasets
            datasets = [Dataset.model_validate(dataset) for dataset in datasets]
            return datasets
        except Exception as e:
            raise e
        

    def create_dataset(
        self,
        dataset_name: str,
        dataset_info: dict = {},
        dataset_type: GEMINIDatasetType = GEMINIDatasetType.Default,
        collection_date: date = date.today()
    ) -> Dataset:
        try:
            dataset = Dataset.create(
                collection_date=collection_date,
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                dataset_type=dataset_type,
                experiment_name=self.experiment_name
            )
            self.refresh()
            return dataset
        except Exception as e:
            raise e
        
    def get_traits(self) -> List[Trait]:
        try:
            traits = self.traits
            traits = [Trait.model_validate(trait) for trait in traits]
            return traits
        except Exception as e:
            raise e
        
    def create_trait(
        self,
        trait_name: str,
        trait_units: str = None,
        trait_level: GEMINITraitLevel = GEMINITraitLevel.Default,
        trait_info: dict = {},
        trait_metrics: dict = {}
    ) -> Trait:
        try:
            trait = Trait.create(
                trait_name=trait_name,
                trait_units=trait_units,
                trait_level=trait_level,
                trait_info=trait_info,
                trait_metrics=trait_metrics,
                experiment_name=self.experiment_name
            )
            self.refresh()
            return trait
        except Exception as e:
            raise e
        

    def get_models(self) -> List[Model]:
        try:
            models = self.models
            models = [Model.model_validate(model) for model in models]
            return models
        except Exception as e:
            raise e
        
    def create_model(
        self,
        model_name: str,
        model_info: dict = {}
    ) -> Model:
        try:
            model = Model.create(
                model_name=model_name,
                model_info=model_info,
                experiment_name=self.experiment_name
            )
            self.refresh()
            return model
        except Exception as e:
            raise e
        

    def get_procedures(self) -> List[Procedure]:
        try:
            procedures = self.procedures
            procedures = [Procedure.model_validate(procedure) for procedure in procedures]
            return procedures
        except Exception as e:
            raise e
        
    def create_procedure(
        self,
        procedure_name: str,
        procedure_info: dict = {}
    ) -> Procedure:
        try:
            procedure = Procedure.create(
                procedure_name=procedure_name,
                procedure_info=procedure_info,
                experiment_name=self.experiment_name
            )
            self.refresh()
            return procedure
        except Exception as e:
            raise e
        

    def get_scripts(self) -> List[Script]:
        try:
            scripts = self.scripts
            scripts = [Script.model_validate(script) for script in scripts]
            return scripts
        except Exception as e:
            raise e
        
    def create_script(
        self,
        script_name: str,
        script_url: str = None,
        script_extension: str = None,
        script_info: dict = {}
    ) -> Script:
        try:
            script = Script.create(
                script_name=script_name,
                script_info=script_info,
                script_url=script_url,
                script_extension=script_extension,
                experiment_name=self.experiment_name
            )
            self.refresh()
            return script
        except Exception as e:
            raise e
        

    def get_platforms(self) -> List[SensorPlatform]:
        try:
            sensor_platforms = self.platforms
            sensor_platforms = [SensorPlatform.model_validate(sensor_platform) for sensor_platform in sensor_platforms]
            return sensor_platforms
        except Exception as e:
            raise e
        
    def create_platform(
        self,
        platform_name: str,
        platform_info: dict = {}
    ) -> SensorPlatform:
        try:
            sensor_platform = SensorPlatform.create(
                sensor_platform_name=platform_name,
                sensor_platform_info=platform_info,
                experiment_name=self.experiment_name
            )
            self.refresh()
            return sensor_platform
        except Exception as e:
            raise e
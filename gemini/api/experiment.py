from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID

from gemini.api.base import APIBase
from gemini.api.enums import (
    GEMINIDataFormat,
    GEMINIDatasetType,
    GEMINIDataType,
    GEMINISensorType,
    GEMINITraitLevel
)

from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.views.experiment_views import (
    ExperimentCultivarsViewModel,
    ExperimentProceduresViewModel,
    ExperimentScriptsViewModel,
    ExperimentModelsViewModel,
    ExperimentSensorsViewModel,
    ExperimentSitesViewModel,
    ExperimentSeasonsViewModel,
    ExperimentTraitsViewModel,
    ExperimentSensorPlatformsViewModel,
    ExperimentDatasetsViewModel
)
from gemini.db.models.views.plot_view import PlotViewModel

from datetime import date


class Experiment(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "experiment_id"))

    experiment_name: str
    experiment_info: Optional[dict] = None
    experiment_start_date: Optional[date] = None
    experiment_end_date: Optional[date] = None

    def __str__(self):
        return f"Experiment(name={self.experiment_name}, start_date={self.experiment_start_date}, end_date={self.experiment_end_date}, id={self.id})"
    
    def __repr__(self):
        return f"Experiment(experiment_name={self.experiment_name}, experiment_start_date={self.experiment_start_date}, experiment_end_date={self.experiment_end_date}, id={self.id})"
    
    @classmethod
    def exists(
        cls,
        experiment_name: str
    ) -> bool:
        try:
            exists = ExperimentModel.exists(experiment_name=experiment_name)
            return exists
        except Exception as e:
            print(f"Error checking existence of experiment: {e}")
            return False
        
    @classmethod
    def create(
        cls,
        experiment_name: str,
        experiment_info: dict = {},
        experiment_start_date: date = date.today(),
        experiment_end_date: date = date.today(),
    ) -> Optional["Experiment"]:
        try:
            db_instance = ExperimentModel.get_or_create(
                experiment_name=experiment_name,
                experiment_info=experiment_info,
                experiment_start_date=experiment_start_date,
                experiment_end_date=experiment_end_date,
            )
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print("Error creating experiment:", e)
            return None
        
    @classmethod
    def get(cls, experiment_name: str) -> Optional["Experiment"]:
        try:
            db_instance = ExperimentModel.get_by_parameters(
                experiment_name=experiment_name,
            )
            if not db_instance:
                print(f"Experiment with name {experiment_name} not found.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print("Error getting experiment:", e)
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["Experiment"]:
        try:
            db_instance = ExperimentModel.get(id)
            if not db_instance:
                print(f"Experiment with ID {id} does not exist.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print("Error getting experiment by ID:", e)
            return None
        
    @classmethod
    def get_all(cls) -> Optional[List["Experiment"]]:
        try:
            experiments = ExperimentModel.all()
            if not experiments or len(experiments) == 0:
                print("No experiments found.")
                return None
            experiments = [cls.model_validate(experiment) for experiment in experiments]
            return experiments
        except Exception as e:
            print("Error getting all experiments:", e)
            return None
        
    @classmethod
    def search(
        cls,
        experiment_name: str = None,
        experiment_info: dict = None,
        experiment_start_date: date = None,
        experiment_end_date: date = None
    ) -> Optional[List["Experiment"]]:
        try:
            if not any([experiment_name, experiment_info, experiment_start_date, experiment_end_date]):
                print("At least one parameter must be provided for search.")
                return None
            experiments = ExperimentModel.search(
                experiment_name=experiment_name,
                experiment_info=experiment_info,
                experiment_start_date=experiment_start_date,
                experiment_end_date=experiment_end_date
            )
            if not experiments or len(experiments) == 0:
                print("No experiments found with the provided search parameters.")
                return None
            experiments = [cls.model_validate(experiment) for experiment in experiments]
            return experiments
        except Exception as e:
            print("Error searching experiments:", e)
            return None
        
    def update(
        self,
        experiment_name: str = None, 
        experiment_info: dict = None,
        experiment_start_date: date = None,
        experiment_end_date: date = None
    ) -> Optional["Experiment"]:
        try:
            if not any([experiment_name, experiment_info, experiment_start_date, experiment_end_date]):
                print("At least one parameter must be provided for update.")
                return None

            current_id = self.id
            experiment = ExperimentModel.get(current_id)
            if not experiment:
                print(f"Experiment with ID {current_id} does not exist.")
                return None
            
            updated_experiment = ExperimentModel.update(
                experiment,
                experiment_name=experiment_name,
                experiment_info=experiment_info,
                experiment_start_date=experiment_start_date,
                experiment_end_date=experiment_end_date
            )
            updated_experiment = self.model_validate(updated_experiment)
            self.refresh()
            return updated_experiment
        except Exception as e:
            print("Error updating experiment:", e)
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            experiment = ExperimentModel.get(current_id)
            if not experiment:
                print(f"Experiment with ID {current_id} does not exist.")
                return False
            ExperimentModel.delete(experiment)
            return True
        except Exception as e:
            print("Error deleting experiment:", e)
            return False
        
    def refresh(self) -> Optional["Experiment"]:
        try:
            db_instance = ExperimentModel.get(self.id)
            if not db_instance:
                print(f"Experiment with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print("Error refreshing experiment:", e)
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            experiment = ExperimentModel.get(current_id)
            if not experiment:
                print(f"Experiment with ID {current_id} does not exist.")
                return None
            experiment_info = experiment.experiment_info
            if not experiment_info:
                print("Experiment info is empty.")
                return None
            return experiment_info
        except Exception as e:
            print("Error getting experiment info:", e)
            return None
        
    def set_info(self, experiment_info: dict) -> Optional["Experiment"]:
        try:
            current_id = self.id
            experiment = ExperimentModel.get(current_id)
            if not experiment:
                print(f"Experiment with ID {current_id} does not exist.")
                return None
            updated_experiment = ExperimentModel.update(
                experiment,
                experiment_info=experiment_info,
            )
            updated_experiment = self.model_validate(updated_experiment)
            self.refresh()
            return updated_experiment
        except Exception as e:
            print("Error setting experiment info:", e)
            return None

    # region Season

    def get_associated_seasons(self):
        try:
            from gemini.api.season import Season
            experiment_seasons = ExperimentSeasonsViewModel.search(experiment_id=self.id)
            if not experiment_seasons or len(experiment_seasons) == 0:
                print("No seasons found for this experiment.")
                return None
            seasons = [Season.model_validate(season) for season in experiment_seasons]
            return seasons
        except Exception as e:
            print("Error getting associated seasons:", e)
            return None

    def create_new_season(
        self,
        season_name: str,
        season_info: dict = {},
        season_start_date: date = date.today(),
        season_end_date: date = date.today(),
    ):
        try:
            from gemini.api.season import Season
            new_season = Season.create(
                season_name=season_name,
                season_info=season_info,
                season_start_date=season_start_date,
                season_end_date=season_end_date,
                experiment_name=self.experiment_name
            )
            if not new_season:
                print("Error creating new season.")
                return None
            return new_season
        except Exception as e:
            print("Error creating new season:", e)
            return None

    # endregion

    # region Cultivar
    def get_associated_cultivars(self):
        try:
            from gemini.api.cultivar import Cultivar
            experiment_cultivars = ExperimentCultivarsViewModel.search(experiment_id=self.id)
            if not experiment_cultivars or len(experiment_cultivars) == 0:
                print("No cultivars found for this experiment.")
                return None
            cultivars = [Cultivar.model_validate(cultivar) for cultivar in experiment_cultivars]
            return cultivars
        except Exception as e:
            print("Error getting associated cultivars:", e)
            return None

    def create_new_cultivar(
        self,
        cultivar_population: str,
        cultivar_accession: str,
        cultivar_info: dict = {},
    ):
        try:
            from gemini.api.cultivar import Cultivar
            new_cultivar = Cultivar.create(
                cultivar_population=cultivar_population,
                cultivar_accession=cultivar_accession,
                cultivar_info=cultivar_info,
                experiment_name=self.experiment_name
            )
            if not new_cultivar:
                print("Error creating new cultivar.")
                return None
            return new_cultivar
        except Exception as e:
            print("Error creating new cultivar:", e)
            return None

    def associate_cultivar(
        self,
        cultivar_population: str,
        cultivar_accession: str,
    ):
        try:
            from gemini.api.cultivar import Cultivar
            cultivar = Cultivar.get(cultivar_population=cultivar_population, cultivar_accession=cultivar_accession)
            if not cultivar:
                print("Cultivar not found.")
                return None
            cultivar.associate_experiment(experiment_name=self.experiment_name)
            return cultivar
        except Exception as e:
            print("Error associating cultivar:", e)
            return None

    def unassociate_cultivar(
        self,
        cultivar_population: str,
        cultivar_accession: str,
    ):
        try:
            from gemini.api.cultivar import Cultivar
            cultivar = Cultivar.get(cultivar_population=cultivar_population, cultivar_accession=cultivar_accession)
            if not cultivar:
                print("Cultivar not found.")
                return None
            cultivar.unassociate_experiment(experiment_name=self.experiment_name)
            return cultivar
        except Exception as e:
            print("Error unassociating cultivar:", e)
            return None

    def belongs_to_cultivar(
        self,
        cultivar_population: str,
        cultivar_accession: str,
    ) -> bool:
        try:
            from gemini.api.cultivar import Cultivar
            cultivar = Cultivar.get(cultivar_population=cultivar_population, cultivar_accession=cultivar_accession)
            if not cultivar:
                print("Cultivar not found.")
                return False
            association_exists = cultivar.belongs_to_experiment(experiment_name=self.experiment_name)
            return association_exists
        except Exception as e:
            print("Error checking if belongs to cultivar:", e)
            return False

    # endregion

    # region Procedure
    def get_associated_procedures(self):
        try:
            from gemini.api.procedure import Procedure
            experiment_procedures = ExperimentProceduresViewModel.search(experiment_id=self.id)
            if not experiment_procedures or len(experiment_procedures) == 0:
                print("No procedures found for this experiment.")
                return None
            procedures = [Procedure.model_validate(procedure) for procedure in experiment_procedures]
            return procedures
        except Exception as e:
            print("Error getting associated procedures:", e)
            return None
        
    def create_new_procedure(
        self,
        procedure_name: str,
        procedure_info: dict = {}
    ):
        try:
            from gemini.api.procedure import Procedure
            new_procedure = Procedure.create(
                procedure_name=procedure_name,
                procedure_info=procedure_info,
                experiment_name=self.experiment_name
            )
            if not new_procedure:
                print("Error creating new procedure.")
                return None
            return new_procedure
        except Exception as e:
            print("Error creating new procedure:", e)
            return None
        
    def associate_procedure(
        self,
        procedure_name: str,
    ):
        try:
            from gemini.api.procedure import Procedure
            procedure = Procedure.get(procedure_name=procedure_name)
            if not procedure:
                print("Procedure not found.")
                return None
            procedure.associate_experiment(experiment_name=self.experiment_name)
            return procedure
        except Exception as e:
            print("Error associating procedure:", e)
            return None
        
    def unassociate_procedure(
        self,
        procedure_name: str,
    ):
        try:
            from gemini.api.procedure import Procedure
            procedure = Procedure.get(procedure_name=procedure_name)
            if not procedure:
                print("Procedure not found.")
                return None
            procedure.unassociate_experiment(experiment_name=self.experiment_name)
            return procedure
        except Exception as e:
            print("Error unassociating procedure:", e)
            return None
        
    def belongs_to_procedure(
        self,
        procedure_name: str,
    ) -> bool:
        try:
            from gemini.api.procedure import Procedure
            procedure = Procedure.get(procedure_name=procedure_name)
            if not procedure:
                print("Procedure not found.")
                return False
            association_exists = procedure.belongs_to_experiment(experiment_name=self.experiment_name)
            return association_exists
        except Exception as e:
            print("Error checking if belongs to procedure:", e)
            return False
        
    # endregion

    # region Script
    def get_associated_scripts(self):
        try:
            from gemini.api.script import Script
            experiment_scripts = ExperimentScriptsViewModel.search(experiment_id=self.id)
            if not experiment_scripts or len(experiment_scripts) == 0:
                print("No scripts found for this experiment.")
                return None
            scripts = [Script.model_validate(script) for script in experiment_scripts]
            return scripts
        except Exception as e:
            print("Error getting associated scripts:", e)
            return None
        
    def create_new_script(
        self,
        script_name: str,
        script_extension: str = None,
        script_url: str = None,
        script_info: dict = {}
    ):
        try:
            from gemini.api.script import Script
            new_script = Script.create(
                script_name=script_name,
                script_url=script_url,
                script_info=script_info,
                script_extension=script_extension,
                experiment_name=self.experiment_name
            )
            if not new_script:
                print("Error creating new script.")
                return None
            return new_script
        except Exception as e:
            print("Error creating new script:", e)
            return None
        
    def associate_script(
        self,
        script_name: str,
    ):
        try:
            from gemini.api.script import Script
            script = Script.get(script_name=script_name)
            if not script:
                print("Script not found.")
                return None
            script.associate_experiment(experiment_name=self.experiment_name)
            return script
        except Exception as e:
            print("Error associating script:", e)
            return None
        
    def unassociate_script(
        self,
        script_name: str,
    ):
        try:
            from gemini.api.script import Script
            script = Script.get(script_name=script_name)
            if not script:
                print("Script not found.")
                return None
            script.unassociate_experiment(experiment_name=self.experiment_name)
            return script
        except Exception as e:
            print("Error unassociating script:", e)
            return None
        
    def belongs_to_script(
        self,
        script_name: str,
    ) -> bool:
        try:
            from gemini.api.script import Script
            script = Script.get(script_name=script_name)
            if not script:
                print("Script not found.")
                return False
            association_exists = script.belongs_to_experiment(experiment_name=self.experiment_name)
            return association_exists
        except Exception as e:
            print("Error checking if belongs to script:", e)
            return False
    # endregion

    # region Model
    def get_associated_models(self):
        try:
            from gemini.api.model import Model
            experiment_models = ExperimentModelsViewModel.search(experiment_id=self.id)
            if not experiment_models or len(experiment_models) == 0:
                print("No models found for this experiment.")
                return None
            models = [Model.model_validate(model) for model in experiment_models]
            return models
        except Exception as e:
            print("Error getting associated models:", e)
            return None
        
    def create_new_model(
        self,
        model_name: str,
        model_url: str = None,
        model_info: dict = {}
    ):
        try:
            from gemini.api.model import Model
            new_model = Model.create(
                model_name=model_name,
                model_info=model_info,
                model_url=model_url,
                experiment_name=self.experiment_name
            )
            if not new_model:
                print("Error creating new model.")
                return None
            return new_model
        except Exception as e:
            print("Error creating new model:", e)
            return None
        
    def associate_model(
        self,
        model_name: str,
    ):
        try:
            from gemini.api.model import Model
            model = Model.get(model_name=model_name)
            if not model:
                print("Model not found.")
                return None
            model.associate_experiment(experiment_name=self.experiment_name)
            return model
        except Exception as e:
            print("Error associating model:", e)
            return None
        
    def unassociate_model(
        self,
        model_name: str,
    ):
        try:
            from gemini.api.model import Model
            model = Model.get(model_name=model_name)
            if not model:
                print("Model not found.")
                return None
            model.unassociate_experiment(experiment_name=self.experiment_name)
            return model
        except Exception as e:
            print("Error unassociating model:", e)
            return None
        
    def belongs_to_model(
        self,
        model_name: str,
    ) -> bool:
        try:
            from gemini.api.model import Model
            model = Model.get(model_name=model_name)
            if not model:
                print("Model not found.")
                return False
            association_exists = model.belongs_to_experiment(experiment_name=self.experiment_name)
            return association_exists
        except Exception as e:
            print("Error checking if belongs to model:", e)
            return False
    # endregion

    # region Sensor
    def get_associated_sensors(self):
        try:
            from gemini.api.sensor import Sensor
            experiment_sensors = ExperimentSensorsViewModel.search(experiment_id=self.id)
            if not experiment_sensors or len(experiment_sensors) == 0:
                print("No sensors found for this experiment.")
                return None
            sensors = [Sensor.model_validate(sensor) for sensor in experiment_sensors]
            return sensors
        except Exception as e:
            print("Error getting associated sensors:", e)
            return None
        
    def create_new_sensor(
        self,
        sensor_name: str,
        sensor_type: GEMINISensorType = GEMINISensorType.Default,
        sensor_data_type: GEMINIDataType = GEMINIDataType.Default,
        sensor_data_format: GEMINIDataFormat = GEMINIDataFormat.Default,
        sensor_info: dict = {},
        sensor_platform_name: str = None
    ):
        try:
            from gemini.api.sensor import Sensor
            new_sensor = Sensor.create(
                sensor_name=sensor_name,
                sensor_type=sensor_type,
                sensor_data_type=sensor_data_type,
                sensor_data_format=sensor_data_format,
                sensor_info=sensor_info,
                experiment_name=self.experiment_name,
                sensor_platform_name=sensor_platform_name
            )
            if not new_sensor:
                print("Error creating new sensor.")
                return None
            return new_sensor
        except Exception as e:
            print("Error creating new sensor:", e)
            return None
        
    def associate_sensor(
        self,
        sensor_name: str,
    ):
        try:
            from gemini.api.sensor import Sensor
            sensor = Sensor.get(sensor_name=sensor_name)
            if not sensor:
                print("Sensor not found.")
                return None
            sensor.associate_experiment(experiment_name=self.experiment_name)
            return sensor
        except Exception as e:
            print("Error associating sensor:", e)
            return None
    
    def unassociate_sensor(
        self,
        sensor_name: str,
    ):
        try:
            from gemini.api.sensor import Sensor
            sensor = Sensor.get(sensor_name=sensor_name)
            if not sensor:
                print("Sensor not found.")
                return None
            sensor.unassociate_experiment(experiment_name=self.experiment_name)
            return sensor
        except Exception as e:
            print("Error unassociating sensor:", e)
            return None
        
    def belongs_to_sensor(
        self,
        sensor_name: str,
    ) -> bool:
        try:
            from gemini.api.sensor import Sensor
            sensor = Sensor.get(sensor_name=sensor_name)
            if not sensor:
                print("Sensor not found.")
                return False
            association_exists = sensor.belongs_to_experiment(experiment_name=self.experiment_name)
            return association_exists
        except Exception as e:
            print("Error checking if belongs to sensor:", e)
            return False
    # endregion

    # region Sensor Platform
    def get_associated_sensor_platforms(self):
        try:
            from gemini.api.sensor_platform import SensorPlatform
            experiment_sensor_platforms = ExperimentSensorPlatformsViewModel.search(experiment_id=self.id)
            if not experiment_sensor_platforms or len(experiment_sensor_platforms) == 0:
                print("No sensor platforms found for this experiment.")
                return None
            sensor_platforms = [SensorPlatform.model_validate(sensor_platform) for sensor_platform in experiment_sensor_platforms]
            return sensor_platforms
        except Exception as e:
            print("Error getting associated sensor platforms:", e)
            return None
        
    def create_new_sensor_platform(
        self,
        sensor_platform_name: str,
        sensor_platform_info: dict = {}
    ):
        try:
            from gemini.api.sensor_platform import SensorPlatform
            new_sensor_platform = SensorPlatform.create(
                sensor_platform_name=sensor_platform_name,
                sensor_platform_info=sensor_platform_info,
                experiment_name=self.experiment_name
            )
            if not new_sensor_platform:
                print("Error creating new sensor platform.")
                return None
            return new_sensor_platform
        except Exception as e:
            print("Error creating new sensor platform:", e)
            return None
        
    def associate_sensor_platform(
        self,
        sensor_platform_name: str,
    ):
        try:
            from gemini.api.sensor_platform import SensorPlatform
            sensor_platform = SensorPlatform.get(sensor_platform_name=sensor_platform_name)
            if not sensor_platform:
                print("Sensor platform not found.")
                return None
            sensor_platform.associate_experiment(experiment_name=self.experiment_name)
            return sensor_platform
        except Exception as e:
            print("Error associating sensor platform:", e)
            return None
        
    def unassociate_sensor_platform(
        self,
        sensor_platform_name: str,
    ):
        try:
            from gemini.api.sensor_platform import SensorPlatform
            sensor_platform = SensorPlatform.get(sensor_platform_name=sensor_platform_name)
            if not sensor_platform:
                print("Sensor platform not found.")
                return None
            sensor_platform.unassociate_experiment(experiment_name=self.experiment_name)
            return sensor_platform
        except Exception as e:
            print("Error unassociating sensor platform:", e)
            return None
        
    def belongs_to_sensor_platform(
        self,
        sensor_platform_name: str,
    ) -> bool:
        try:
            from gemini.api.sensor_platform import SensorPlatform
            sensor_platform = SensorPlatform.get(sensor_platform_name=sensor_platform_name)
            if not sensor_platform:
                print("Sensor platform not found.")
                return False
            association_exists = sensor_platform.belongs_to_experiment(experiment_name=self.experiment_name)
            return association_exists
        except Exception as e:
            print("Error checking if belongs to sensor platform:", e)
            return False
    # endregion

    # region Site
    def get_associated_sites(self):
        try:
            from gemini.api.site import Site
            experiment_sites = ExperimentSitesViewModel.search(experiment_id=self.id)
            if not experiment_sites or len(experiment_sites) == 0:
                print("No sites found for this experiment.")
                return None
            sites = [Site.model_validate(site) for site in experiment_sites]
            return sites
        except Exception as e:
            print("Error getting associated sites:", e)
            return None
        
    def create_new_site(
        self,
        site_name: str,
        site_city: str = None,
        site_state: str = None,
        site_country: str = None,
        site_info: dict = {}
    ):
        try:
            from gemini.api.site import Site
            new_site = Site.create(
                site_name=site_name,
                site_city=site_city,
                site_state=site_state,
                site_country=site_country,
                site_info=site_info,
                experiment_name=self.experiment_name
            )
            if not new_site:
                print("Error creating new site.")
                return None
            return new_site
        except Exception as e:
            print("Error creating new site:", e)
            return None
        
    def associate_site(
        self,
        site_name: str,
    ):
        try:
            from gemini.api.site import Site
            site = Site.get(site_name=site_name)
            if not site:
                print("Site not found.")
                return None
            site.associate_experiment(experiment_name=self.experiment_name)
            return site
        except Exception as e:
            print("Error associating site:", e)
            return None
        
    def unassociate_site(
        self,
        site_name: str,
    ):
        try:
            from gemini.api.site import Site
            site = Site.get(site_name=site_name)
            if not site:
                print("Site not found.")
                return None
            site.unassociate_experiment(experiment_name=self.experiment_name)
            return site
        except Exception as e:
            print("Error unassociating site:", e)
            return None
        
    def belongs_to_site(
        self,
        site_name: str,
    ) -> bool:
        try:
            from gemini.api.site import Site
            site = Site.get(site_name=site_name)
            if not site:
                print("Site not found.")
                return False
            association_exists = site.belongs_to_experiment(experiment_name=self.experiment_name)
            return association_exists
        except Exception as e:
            print("Error checking if belongs to site:", e)
            return False
    # endregion

    # region Dataset
    def get_associated_datasets(self):
        try:
            from gemini.api.dataset import Dataset
            experiment_datasets = ExperimentDatasetsViewModel.search(experiment_id=self.id)
            if not experiment_datasets or len(experiment_datasets) == 0:
                print("No datasets found for this experiment.")
                return None
            datasets = [Dataset.model_validate(dataset) for dataset in experiment_datasets]
            return datasets
        except Exception as e:
            print("Error getting associated datasets:", e)
            return None
        
    def create_new_dataset(
        self,
        dataset_name: str,
        dataset_info: dict = {},
        dataset_type: GEMINIDatasetType = GEMINIDatasetType.Default,
        collection_date: date = date.today()
    ):
        try:
            from gemini.api.dataset import Dataset
            new_dataset = Dataset.create(
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                dataset_type=dataset_type,
                collection_date=collection_date,
                experiment_name=self.experiment_name
            )
            if not new_dataset:
                print("Error creating new dataset.")
                return None
            return new_dataset
        except Exception as e:
            print("Error creating new dataset:", e)
            return None
        
    def associate_dataset(
        self,
        dataset_name: str,
    ):
        try:
            from gemini.api.dataset import Dataset
            dataset = Dataset.get(dataset_name=dataset_name)
            if not dataset:
                print("Dataset not found.")
                return None
            dataset.associate_experiment(experiment_name=self.experiment_name)
            return dataset
        except Exception as e:
            print("Error associating dataset:", e)
            return None
        
    def unassociate_dataset(
        self,
        dataset_name: str,
    ):
        try:
            from gemini.api.dataset import Dataset
            dataset = Dataset.get(dataset_name=dataset_name)
            if not dataset:
                print("Dataset not found.")
                return None
            dataset.unassociate_experiment(experiment_name=self.experiment_name)
            return dataset
        except Exception as e:
            print("Error unassociating dataset:", e)
            return None
        
    def belongs_to_dataset(
        self,
        dataset_name: str,
    ) -> bool:
        try:
            from gemini.api.dataset import Dataset
            dataset = Dataset.get(dataset_name=dataset_name)
            if not dataset:
                print("Dataset not found.")
                return False
            association_exists = dataset.belongs_to_experiment(experiment_name=self.experiment_name)
            return association_exists
        except Exception as e:
            print("Error checking if belongs to dataset:", e)
            return False
        
    # endregion

    # region Trait
    def get_associated_traits(self):
        try:
            from gemini.api.trait import Trait
            experiment_traits = ExperimentTraitsViewModel.search(experiment_id=self.id)
            if not experiment_traits or len(experiment_traits) == 0:
                print("No traits found for this experiment.")
                return None
            traits = [Trait.model_validate(trait) for trait in experiment_traits]
            return traits
        except Exception as e:
            print("Error getting associated traits:", e)
            return None
        
    def create_new_trait(
        self,
        trait_name: str,
        trait_units: str = None,
        trait_metrics: dict = {},
        trait_level: GEMINITraitLevel = GEMINITraitLevel.Default,
        trait_info: dict = {},
    ):
        try:
            from gemini.api.trait import Trait
            new_trait = Trait.create(
                trait_name=trait_name,
                trait_units=trait_units,
                trait_metrics=trait_metrics,
                trait_level=trait_level,
                trait_info=trait_info,
                experiment_name=self.experiment_name
            )
            if not new_trait:
                print("Error creating new trait.")
                return None
            return new_trait
        except Exception as e:
            print("Error creating new trait:", e)
            return None
        
    def associate_trait(
        self,
        trait_name: str,
    ):
        try:
            from gemini.api.trait import Trait
            trait = Trait.get(trait_name=trait_name)
            if not trait:
                print("Trait not found.")
                return None
            trait.associate_experiment(experiment_name=self.experiment_name)
            return trait
        except Exception as e:
            print("Error associating trait:", e)
            return None
        
    def unassociate_trait(
        self,
        trait_name: str,
    ):
        try:
            from gemini.api.trait import Trait
            trait = Trait.get(trait_name=trait_name)
            if not trait:
                print("Trait not found.")
                return None
            trait.unassociate_experiment(experiment_name=self.experiment_name)
            return trait
        except Exception as e:
            print("Error unassociating trait:", e)
            return None
        
    def belongs_to_trait(
        self,
        trait_name: str,
    ) -> bool:
        try:
            from gemini.api.trait import Trait
            trait = Trait.get(trait_name=trait_name)
            if not trait:
                print("Trait not found.")
                return False
            association_exists = trait.belongs_to_experiment(experiment_name=self.experiment_name)
            return association_exists
        except Exception as e:
            print("Error checking if belongs to trait:", e)
            return False
    # endregion

    # region Plot
    
    def get_associated_plots(self):
        try:
            from gemini.api.plot import Plot
            plots = PlotViewModel.search(experiment_id=self.id)
            if not plots or len(plots) == 0:
                print("No plots found for this experiment.")
                return None
            plots = [Plot.model_validate(plot) for plot in plots]
            return plots
        except Exception as e:
            print("Error getting associated plots:", e)
            return None
        
    def create_new_plot(
        self,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        season_name: str = None,
        site_name: str = None,
        plot_info: dict = {}
    ):
        try:
            from gemini.api.plot import Plot
            new_plot = Plot.create(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                season_name=season_name,
                site_name=site_name,
                plot_info=plot_info,
                experiment_name=self.experiment_name
            )
            if not new_plot:
                print("Error creating new plot.")
                return None
            return new_plot
        except Exception as e:
            print("Error creating new plot:", e)
            return None
        
    def associate_plot(
        self,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        season_name: str = None,
        site_name: str = None,
    ):
        try:
            from gemini.api.plot import Plot
            plot = Plot.get(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                season_name=season_name,
                site_name=site_name
            )
            if not plot:
                print("Plot not found.")
                return None
            plot.associate_experiment(experiment_name=self.experiment_name)
            return plot
        except Exception as e:
            print("Error associating plot:", e)
            return None
        
    def unassociate_plot(
        self,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        season_name: str = None,
        site_name: str = None,
    ):
        try:
            from gemini.api.plot import Plot
            plot = Plot.get(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                season_name=season_name,
                site_name=site_name
            )
            if not plot:
                print("Plot not found.")
                return None
            plot.unassociate_experiment()
            return plot
        except Exception as e:
            print("Error unassociating plot:", e)
            return None
        
    def belongs_to_plot(
        self,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        season_name: str = None,
        site_name: str = None,
    ) -> bool:
        try:
            from gemini.api.plot import Plot
            plot = Plot.get(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                season_name=season_name,
                site_name=site_name
            )
            if not plot:
                print("Plot not found.")
                return False
            association_exists = plot.belongs_to_experiment(experiment_name=self.experiment_name)
            return association_exists
        except Exception as e:
            print("Error checking if belongs to plot:", e)
            return False
    # endregion
            
        

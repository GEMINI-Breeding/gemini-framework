from typing import Optional, List
from gemini.api.base import APIBase
from gemini.api.season import Season
from gemini.api.sensor import Sensor
from gemini.api.trait import Trait
from gemini.api.site import Site
from gemini.api.cultivar import Cultivar
from gemini.api.dataset import Dataset
from gemini.api.sensor_platform import SensorPlatform
from gemini.server.database.models import ExperimentModel

from datetime import date


class Experiment(APIBase):
    """
    Represents an experiment in the Gemini framework.

    Attributes:
        db_model (ExperimentModel): The database model associated with the experiment.
        experiment_name (str): The name of the experiment.
        experiment_info (Optional[dict]): Additional information about the experiment.
        experiment_start_date (Optional[date]): The start date of the experiment.
        experiment_end_date (Optional[date]): The end date of the experiment.
        seasons (Optional[List[Season]]): The seasons associated with the experiment.
        sites (Optional[List[Site]]): The sites associated with the experiment.
        sensors (Optional[List[Sensor]]): The sensors associated with the experiment.
        traits (Optional[List[Trait]]): The traits associated with the experiment.
        resources (Optional[List[Resource]]): The resources associated with the experiment.
        cultivars (Optional[List[Cultivar]]): The cultivars associated with the experiment.
        datasets (Optional[List[Dataset]]): The datasets associated with the experiment.
    """

    db_model = ExperimentModel

    experiment_name: str
    experiment_info: Optional[dict] = None
    experiment_start_date: Optional[date] = None
    experiment_end_date: Optional[date] = None

    seasons: Optional[List[Season]] = None
    sites: Optional[List[Site]] = None
    sensors: Optional[List[Sensor]] = None
    traits: Optional[List[Trait]] = None
    cultivars: Optional[List[Cultivar]] = None
    datasets: Optional[List[Dataset]] = None
    platforms: Optional[List[SensorPlatform]] = None

    @classmethod
    def create(
        cls,
        experiment_name: str,
        experiment_info: dict = None,
        experiment_start_date: date = None,
        experiment_end_date: date = None,
    ) -> "Experiment":
        """
        Creates a new experiment.

        Args:
            experiment_name (str): The name of the experiment.
            experiment_info (dict, optional): Additional information about the experiment.
            experiment_start_date (date, optional): The start date of the experiment.
            experiment_end_date (date, optional): The end date of the experiment.

        Returns:
            Experiment: The created experiment instance.
        """
        db_instance = cls.db_model.get_or_create(
            experiment_name=experiment_name,
            experiment_info=experiment_info,
            experiment_start_date=experiment_start_date,
            experiment_end_date=experiment_end_date,
        )

        return cls.model_validate(db_instance)

    @classmethod
    def get(cls, experiment_name: str) -> "Experiment":
        """
        Retrieves an experiment by its name.

        Args:
            experiment_name (str): The name of the experiment.

        Returns:
            Experiment: The experiment instance if found, else None.
        """
        db_instance = cls.db_model.get_by_parameters(experiment_name=experiment_name)
        return cls.model_validate(db_instance) if db_instance else None

    def get_info(self) -> dict:
        """
        Retrieves the additional information about the experiment.

        Returns:
            dict: The experiment information.
        """
        self.refresh()
        return self.experiment_info

    def set_info(self, experiment_info: Optional[dict] = None) -> "Experiment":
        """
        Sets the additional information about the experiment.

        Args:
            experiment_info (dict, optional): The experiment information.

        Returns:
            Experiment: The updated experiment instance.
        """
        self.update(experiment_info=experiment_info)
        return self

    def add_info(self, experiment_info: Optional[dict] = None) -> "Experiment":
        """
        Adds additional information to the existing experiment information.

        Args:
            experiment_info (dict, optional): The experiment information to add.

        Returns:
            Experiment: The updated experiment instance.
        """
        current_info = self.get_info()
        updated_info = {**current_info, **experiment_info}
        self.set_info(updated_info)
        return self

    def remove_info(self, keys_to_remove: List[str]) -> "Experiment":
        """
        Removes specific keys from the experiment information.

        Args:
            keys_to_remove (List[str]): The keys to remove from the experiment information.

        Returns:
            Experiment: The updated experiment instance.
        """
        current_info = self.get_info()
        updated_info = {
            key: value
            for key, value in current_info.items()
            if key not in keys_to_remove
        }
        self.set_info(updated_info)
        return self

    def get_sensors(self) -> List[Sensor]:
        """
        Retrieves the sensors associated with the experiment.

        Returns:
            List[Sensor]: The list of sensors.
        """
        self.refresh()
        return self.sensors

    def get_sensor_platforms(self) -> List[SensorPlatform]:
        """
        Retrieves the sensor platforms associated with the experiment.

        Returns:
            List[SensorPlatform]: The list of sensor platforms.
        """
        self.refresh()
        return self.platforms

    def get_traits(self) -> List[Trait]:
        """
        Retrieves the traits associated with the experiment.

        Returns:
            List[Trait]: The list of traits.
        """
        self.refresh()
        return self.traits

    def get_sites(self) -> List[Site]:
        """
        Retrieves the sites associated with the experiment.

        Returns:
            List[Site]: The list of sites.
        """
        self.refresh()
        return self.sites

    def get_seasons(self) -> List[Season]:
        """
        Retrieves the seasons associated with the experiment.

        Returns:
            List[Season]: The list of seasons.
        """
        self.refresh()
        return self.seasons

    def get_cultivars(self) -> List[Cultivar]:
        """
        Retrieves the cultivars associated with the experiment.

        Returns:
            List[Cultivar]: The list of cultivars.
        """
        self.refresh()
        return self.cultivars

    def get_datasets(self) -> List[Dataset]:
        """
        Retrieves the datasets associated with the experiment.

        Returns:
            List[Dataset]: The list of datasets.
        """
        self.refresh()
        return self.datasets

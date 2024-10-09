from typing import Optional, List, Any
from gemini.api.base import APIBase, ID
from gemini.api.enums import GEMINIDatasetType
from gemini.api.dataset_type import DatasetType
from gemini.api.dataset_record import DatasetRecord
from gemini.server.database.models import DatasetModel, ExperimentModel, DatasetTypeModel
from gemini.server.database.models import ExperimentDatasetsViewModel

from datetime import datetime, date
from rich.progress import track
from pydantic import Field, AliasChoices


class Dataset(APIBase):

    db_model = DatasetModel

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "dataset_id"))
    dataset_name: str
    dataset_info: Optional[dict] = None
    is_derived: Optional[bool] = False
    collection_date: Optional[date] = None

    dataset_type: Optional[DatasetType] = None


    @classmethod
    def create(
        cls,
        dataset_name: str = 'Default',
        dataset_info: dict = {},
        is_derived: bool = False,
        collection_date: date = None,
        dataset_type: GEMINIDatasetType = GEMINIDatasetType.Default,
        experiment_name: str = 'Default'
    ):
        """
        Create a new dataset.

        Args:
            dataset_name (str): The name of the dataset. Defaults to 'Default'.
            dataset_info (dict): Additional information about the dataset. Defaults to an empty dictionary.
            is_derived (bool): Indicates if the dataset is derived from another dataset. Defaults to False.
            collection_date (date): The date when the dataset was collected. Defaults to None.
            dataset_type (GEMINIDatasetType): The type of the dataset. Defaults to GEMINIDatasetType.Default.
            experiment_name (str): The name of the experiment associated with the dataset. Defaults to 'Default'.

        Returns:
            The newly created dataset instance.

        """
        
        db_dataset_type = DatasetTypeModel.get_by_id(dataset_type.value)
        new_instance = cls.db_model.get_or_create(
            dataset_name=dataset_name,
            dataset_info=dataset_info,
            is_derived=is_derived,
            collection_date=collection_date,
            dataset_type=db_dataset_type
        )

        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        if db_experiment and new_instance not in db_experiment.datasets:
            db_experiment.datasets.append(new_instance)
            db_experiment.save()

        new_instance = cls.model_validate(new_instance)
        return new_instance
    
    @classmethod
    def get(cls, dataset_name: str) -> "Dataset":
        """
        Retrieve a dataset by its name.

        Args:
            dataset_name (str): The name of the dataset to retrieve.

        Returns:
            Dataset: The retrieved dataset object, or None if not found.
        """
        db_instance = cls.db_model.get_by_parameters(dataset_name=dataset_name)
        if db_instance is None:
            return None
        return cls.model_validate(db_instance)
    
    @classmethod
    def get_by_experiment(cls, experiment_name: str) -> List["Dataset"]:
        """
        Retrieve datasets associated with a specific experiment.

        Args:
            experiment_name (str): The name of the experiment.

        Returns:
            List[Dataset]: A list of Dataset objects associated with the experiment.
        """
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        if db_experiment is None:
            return []
        db_datasets = db_experiment.datasets
        return [cls.model_validate(db_dataset) for db_dataset in db_datasets]
    
    @classmethod
    def get_by_type(cls, dataset_type: GEMINIDatasetType) -> List["Dataset"]:
        """
        Retrieve datasets of a specific type from the database.

        Args:
            dataset_type (GEMINIDatasetType): The type of dataset to retrieve.

        Returns:
            List[Dataset]: A list of datasets of the specified type.
        """
        db_instances = cls.db_model.search(dataset_type_id=dataset_type.value)
        return [cls.model_validate(db_instance) for db_instance in db_instances]
    
    def get_info(self) -> dict:
        """
        Retrieves information about the dataset.

        Returns:
            dict: A dictionary containing information about the dataset.
        """
        self.refresh()
        return self.dataset_info
    
    def set_info(self, dataset_info: Optional[dict] = None) -> "Dataset":
        """
        Sets the information for the dataset.

        Args:
            dataset_info (Optional[dict]): A dictionary containing the dataset information.

        Returns:
            Dataset: The updated Dataset object.

        """
        self.update(dataset_info=dataset_info)
        return self

    def add_info(self, dataset_info: dict) -> "Dataset":
        """
        Adds additional information to the dataset.

        Args:
            dataset_info (dict): A dictionary containing the additional information to be added.

        Returns:
            Dataset: The updated Dataset object.

        """
        current_info = self.get_info()
        updated_info = {**current_info, **dataset_info}
        self.set_info(updated_info)
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Dataset":
        """
        Removes the specified keys from the dataset's info dictionary.

        Args:
            keys_to_remove (List[str]): A list of keys to be removed from the info dictionary.

        Returns:
            Dataset: The updated dataset object.

        """
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(current_info)
        return self
    
    @classmethod
    def search(
        cls,
        experiment_name: str = None,
        **search_parameters: Any
    ) -> List["Dataset"]:
        """
        Search for datasets based on the given parameters.

        Args:
            experiment_name (str, optional): The name of the experiment to filter datasets by.
            **search_parameters: Additional search parameters to filter datasets by.

        Returns:
            List[Dataset]: A list of datasets that match the search criteria, or None if no datasets are found.
        """
        datasets = ExperimentDatasetsViewModel.search(
            experiment_name=experiment_name,
            **search_parameters
        )
        datasets = [cls.model_validate(dataset) for dataset in datasets]
        return datasets if datasets else None
    
    # Todo: Add Records and Search Records methods
    def add_record(
            self,
            dataset_data: dict,
            timestamp: datetime = None,
            collection_date: date = None,
            dataset_name: str = 'Default',
            experiment_name: str = 'Default',
            season_name: str = '2023',
            site_name: str = 'Default',
            plot_number: int = -1,
            plot_row_number: int = -1,
            plot_column_number: int = -1,
            record_info: dict = {}
    ) -> bool:
        """
        Adds a record to the dataset.

        Args:
            dataset_data (dict): The data for the record.
            timestamp (datetime, optional): The timestamp of the record. If not provided, the current timestamp will be used.
            collection_date (date, optional): The collection date of the record. If not provided, the timestamp's date will be used.
            dataset_name (str, optional): The name of the dataset. Defaults to 'Default'.
            experiment_name (str, optional): The name of the experiment. Defaults to 'Default'.
            season_name (str, optional): The name of the season. Defaults to '2023'.
            site_name (str, optional): The name of the site. Defaults to 'Default'.
            plot_number (int, optional): The plot number. Defaults to -1.
            plot_row_number (int, optional): The row number of the plot. Defaults to -1.
            plot_column_number (int, optional): The column number of the plot. Defaults to -1.
            record_info (dict, optional): Additional information for the record. Defaults to an empty dictionary.

        Returns:
            bool: True if the record was successfully added, False otherwise.
        """
        if timestamp is None:
            timestamp = datetime.now()

        collection_date = timestamp.date() if collection_date is None else collection_date

        if dataset_name is None:
            dataset_name = self.dataset_name

        info = {
            "experiment_name": experiment_name,
            "season_name": season_name,
            "site_name": site_name,
            "plot_number": plot_number,
            "plot_row_number": plot_row_number,
            "plot_column_number": plot_column_number
        }

        if record_info:
            info.update(record_info)

        record = DatasetRecord.create(
            dataset_name=self.dataset_name,
            timestamp=timestamp,
            collection_date=collection_date,
            dataset_data=dataset_data,
            record_info=info
        )

        success = DatasetRecord.add([record])
        return success
    

    def add_records(
        self,
        dataset_data: List[dict],
        timestamps: List[datetime] = None,
        collection_date: date = None,
        dataset_name: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        plot_numbers: List[int] = None,
        plot_row_numbers: List[int] = None,
        plot_column_numbers: List[int] = None,
        record_info: List[dict] = None
    ) -> bool:
        """
        Add records to the dataset.

        Args:
            dataset_data (List[dict]): The list of dataset records to be added.
            timestamps (List[datetime], optional): The list of timestamps for the records. If not provided, the current
                timestamp will be used for each record. Defaults to None.
            collection_date (date, optional): The collection date for the records. If not provided, the collection date
                will be set to the date of the first timestamp. Defaults to None.
            dataset_name (str, optional): The name of the dataset. If not provided, the dataset name from the instance
                will be used. Defaults to None.
            experiment_name (str, optional): The name of the experiment. Defaults to None.
            season_name (str, optional): The name of the season. Defaults to None.
            site_name (str, optional): The name of the site. Defaults to None.
            plot_numbers (List[int], optional): The list of plot numbers. Defaults to None.
            plot_row_numbers (List[int], optional): The list of plot row numbers. Defaults to None.
            plot_column_numbers (List[int], optional): The list of plot column numbers. Defaults to None.
            record_info (List[dict], optional): Additional information for each record. Defaults to None.

        Returns:
            bool: True if the records were successfully added, False otherwise.
        """
        if timestamps is None:
            timestamps = [datetime.now() for _ in range(len(dataset_data))]

        if len(dataset_data) != len(timestamps):
            raise ValueError("The number of timestamps must match the number of records")

        collection_date = timestamps[0].date() if collection_date is None else collection_date

        if dataset_name is None:
            dataset_name = self.dataset_name

        db_dataset = DatasetModel.get_or_create(dataset_name=dataset_name)

        records = []

        for i in range(len(dataset_data)):
            info = {
                "experiment_name": experiment_name if experiment_name else None,
                "season_name": season_name if season_name else None,
                "site_name": site_name if site_name else None,
                "plot_number": plot_numbers[i] if plot_numbers else None,
                "plot_row_number": plot_row_numbers[i] if plot_row_numbers else None,
                "plot_column_number": plot_column_numbers[i] if plot_column_numbers else None
            }

            if record_info and record_info[i]:
                info.update(record_info[i])

            record = DatasetRecord.create(
                dataset_name=self.dataset_name,
                timestamp=timestamps[i],
                collection_date=collection_date,
                dataset_data=dataset_data[i],
                record_info=info
            )

            records.append(record)

        success = DatasetRecord.add(records)
        return success


    def get_records(
            self,
            collection_date: date = None,
            experiment_name: str = None,
            season_name: str = None,
            site_name: str = None,
            plot_number: int = None,
            plot_row_number: int = None,
            plot_column_number: int = None,
            record_info: dict = None
    ) -> List[DatasetRecord]:
        """
        Retrieves dataset records based on the specified filters.

        Args:
            collection_date (date, optional): The collection date of the records.
            experiment_name (str, optional): The name of the experiment.
            season_name (str, optional): The name of the season.
            site_name (str, optional): The name of the site.
            plot_number (int, optional): The plot number.
            plot_row_number (int, optional): The row number of the plot.
            plot_column_number (int, optional): The column number of the plot.
            record_info (dict, optional): Additional record information.

        Returns:
            List[DatasetRecord]: A list of dataset records matching the specified filters.
        """
        record_info = record_info if record_info else {}
        record_info.update({
            "experiment_name": experiment_name,
            "season_name": season_name,
            "site_name": site_name,
            "plot_number": plot_number,
            "plot_row_number": plot_row_number,
            "plot_column_number": plot_column_number
        })

        record_info = {key: value for key, value in record_info.items() if value is not None}

        records = DatasetRecord.search(
            dataset_name=self.dataset_name,
            collection_date=collection_date,
            record_info=record_info
        )
        return records

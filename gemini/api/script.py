from typing import Optional, List, Any
from gemini.api.base import APIBase
from gemini.api.script_run import ScriptRun
from gemini.api.dataset import Dataset
from gemini.models import ScriptModel, ScriptRunModel

from gemini.logger import logger_service


class Script(APIBase):

    db_model = ScriptModel

    script_name: str
    script_url: Optional[str] = None
    script_extension: Optional[str] = None
    script_info: Optional[dict] = None

    datasets: Optional[List[Dataset]] = None
    script_runs: Optional[List[ScriptRun]] = None

    @classmethod
    def create(
        cls,
        script_name: str,
        script_url: str = None,
        script_extension: str = None,
        script_info: dict = None,
    ):
        new_instance = cls.db_model.get_or_create(
            script_name=script_name,
            script_url=script_url,
            script_extension=script_extension,
            script_info=script_info,
        )
        logger_service.info(
            "API",
            f"Created a new script with name {new_instance.script_name} in the database",
        )
        new_instance = cls.model_validate(new_instance)
        return new_instance
    
    @classmethod
    def get(cls, script_name: str) -> "Script":
        script = cls.db_model.get_by_name(script_name)
        script = cls.model_validate(script)
        logger_service.info(
            "API",
            f"Retrieved script with name {script_name} from the database",
        )
        return script
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved information about {self.script_name} from the database",
        )
        return self.script_info
    
    def set_info(self, script_info: Optional[dict] = None) -> "Script":
        self.update(script_info=script_info)
        logger_service.info(
            "API",
            f"Updated information about {self.script_name} in the database",
        )
        return self
    
    def add_info(self, script_info: Optional[dict] = None) -> "Script":
        current_info = self.get_info()
        updated_info = {**current_info, **script_info}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Added information to {self.script_name} in the database",
        )
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Script":
        current_info = self.get_info()
        for key in keys_to_remove:
            current_info.pop(key, None)
        self.set_info(current_info)
        logger_service.info(
            "API",
            f"Removed information from {self.script_name} in the database",
        )
        return self
    
    def get_datasets(self) -> List[Dataset]:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved datasets for {self.script_name} from the database",
        )
        return self.datasets
    
    def get_script_runs(self) -> List[ScriptRun]:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved script runs for {self.script_name} from the database",
        )
        return self.script_runs
    
    # Todo: Adding, removing, searching data generated by a script
    # Todo: Add and remove datasets
    # Todo: Add and remove script runs


# from typing import Optional, List, Any
# from uuid import UUID
# from pydantic import Field
# from gemini.api.base import APIBase
# from gemini.api.script_record import ScriptRecord
# from gemini.models import ScriptModel

# from gemini.logger import logger_service
# import pandas as pd
# from datetime import datetime


# class Script(APIBase):

#     db_model = ScriptModel

#     script_name: str
#     script_url: Optional[str] = None
#     script_extension: Optional[str] = None
#     script_info: Optional[dict] = None

#     datasets: Optional[List[dict]] = None

#     @classmethod
#     def create(
#         cls,
#         script_name: str,
#         script_url: str = None,
#         script_extension: str = None,
#         script_info: dict = None,
#     ):
#         """
#         Create a new script

#         Args:
#         script_name (str): The name of the script
#         script_url (str, optional): The URL of the script. Defaults to None.
#         script_extension (str, optional): The extension of the script. Defaults to None.
#         script_info (dict, optional): The information about the script. Defaults to None.

#         Returns:
#         Script: The created script
#         """
#         new_instance = cls.db_model.get_or_create(
#             script_name=script_name,
#             script_url=script_url,
#             script_extension=script_extension,
#             script_info=script_info,
#         )
#         logger_service.info(
#             "API",
#             f"Created a new script with name {new_instance.script_name} in the database",
#         )
#         new_instance = cls.model_validate(new_instance)
#         return new_instance

#     @classmethod
#     def get_by_name(cls, script_name: str) -> "Script":
#         """
#         Get a script by name

#         Args:
#         script_name (str): The name of the script

#         Returns:
#         Script: The script with the given name
#         """
#         script = cls.db_model.get_by_name(script_name)
#         script = cls.model_validate(script)
#         logger_service.info(
#             "API",
#             f"Retrieved script with name {script_name} from the database",
#         )
#         return script

#     @classmethod
#     def get_by_extension(cls, script_extension: str) -> List["Script"]:
#         """
#         Get all the scripts of a given extension

#         Args:
#         script_extension (str): The extension of the scripts

#         Returns:
#         List[Script]: A list of all the scripts with the given extension
#         """
#         scripts = cls.db_model.get_by_parameter("script_extension", script_extension)
#         scripts = [cls.model_validate(script) for script in scripts]
#         logger_service.info(
#             "API",
#             f"Retrieved scripts with extension {script_extension} from the database",
#         )
#         return scripts

#     def get_info(self) -> dict:
#         """
#         Get the information about a script

#         Returns:
#         dict: The information about the script
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved information about {self.script_name} from the database",
#         )
#         return self.script_info

#     def set_info(self, script_info: Optional[dict] = None) -> "Script":
#         """
#         Set the information about a script

#         Args:
#         script_info (Optional[dict], optional): The information to set. Defaults to None.

#         Returns:
#         Script: The script with the updated information
#         """
#         self.update(script_info=script_info)
#         logger_service.info(
#             "API",
#             f"Updated information about {self.script_name} in the database",
#         )
#         return self

#     def add_info(self, script_info: Optional[dict] = None) -> "Script":
#         """
#         Add information to a script

#         Args:
#         script_info (Optional[dict], optional): The information to add. Defaults to None.

#         Returns:
#         Script: The script with the added information
#         """
#         current_info = self.get_info()
#         updated_info = {**current_info, **script_info}
#         self.set_info(updated_info)
#         logger_service.info(
#             "API",
#             f"Added information to {self.script_name} in the database",
#         )
#         return self

#     def remove_info(self, keys_to_remove: List[str]) -> "Script":
#         """
#         Remove information from a script

#         Args:
#         keys_to_remove (List[str]): The keys to remove
#         """

#         current_info = self.get_info()
#         for key in keys_to_remove:
#             current_info.pop(key, None)
#         self.set_info(current_info)
#         logger_service.info(
#             "API",
#             f"Removed information from {self.script_name} in the database",
#         )
#         return self

#     def get_datasets(self) -> List[dict]:
#         """
#         Get the datasets for a script

#         Returns:
#         List[Any]: The datasets for the script
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved datasets for {self.script_name} from the database",
#         )
#         return self.datasets

#     # Todo: Adding, removing, searching data generated by a script
#     def get_records(
#         self,
#         collection_date: datetime = None,
#         experiment: str = None,
#         season: str = None,
#         site: str = None,
#         plot_number: int = None,
#         plot_row_number: int = None,
#         plot_column_number: int = None,
#         record_info: dict = None,
#         as_dataframe: bool = False,
#     ) -> List[ScriptRecord]:
#         """
#         Get the records generated by a script

#         Args:
#         collection_date (str, optional): The collection date of the records. Defaults to None.
#         experiment (str, optional): The experiment of the records. Defaults to None.
#         season (str, optional): The season of the records. Defaults to None.
#         site (str, optional): The site of the records. Defaults to None.
#         plot_number (int, optional): The plot number of the records. Defaults to None.
#         plot_row_number (int, optional): The plot row number of the records. Defaults to None.
#         plot_column_number (int, optional): The plot column number of the records. Defaults to None.
#         record_info (dict, optional): The information about the records. Defaults to None.
#         as_dataframe (bool, optional): Whether to return the records as a pandas DataFrame. Defaults to False.

#         Returns:
#         List[ScriptRecord]: The records generated by the script
#         """
#         self.refresh()
#         searched_records = ScriptRecord.search(
#             collection_date=collection_date,
#             experiment_name=experiment,
#             season_name=season,
#             site_name=site,
#             script_name=self.script_name,
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#             record_info=record_info,
#         )
#         if as_dataframe:
#             searched_records = [record.model_dump() for record in searched_records]
#             searched_records = pd.DataFrame(searched_records)
#         logger_service.info(
#             "API",
#             f"Retrieved records generated by {self.script_name} from the database",
#         )
#         return searched_records

#     def add_record(
#         self,
#         timestamp: datetime,
#         collection_date: datetime,
#         script_data: dict,
#         record_info: dict = None,
#         experiment_name: str = None,
#         season_name: str = None,
#         site_name: str = None,
#         plot_number: int = None,
#         plot_row_number: int = None,
#         plot_column_number: int = None,
#     ) -> ScriptRecord:
#         """
#         Add a record generated by a script

#         Args:
#         timestamp (datetime): The timestamp of the record
#         collection_date (datetime): The collection date of the record
#         script_data (dict): The data of the record
#         record_info (dict, optional): The information about the record. Defaults to None.
#         experiment_name (str, optional): The name of the experiment. Defaults to None.
#         season_name (str, optional): The name of the season. Defaults to None.
#         site_name (str, optional): The name of the site. Defaults to None.
#         plot_number (int, optional): The plot number. Defaults to None.
#         plot_row_number (int, optional): The plot row number. Defaults to None.
#         plot_column_number (int, optional): The plot column number. Defaults to None.

#         Returns:
#         ScriptRecord: The record generated by the script
#         """
#         new_record = ScriptRecord.create(
#             script_name=self.script_name,
#             timestamp=timestamp,
#             collection_date=collection_date,
#             script_data=script_data,
#             record_info=record_info,
#             experiment_name=experiment_name,
#             season_name=season_name,
#             site_name=site_name,
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#         )
#         logger_service.info(
#             "API",
#             f"Added a record generated by {self.script_name} to the database",
#         )
#         return new_record

#     def add_records(
#         self,
#         script_data: List[dict],
#         timestamps: List[datetime] = None,
#         experiment_name: str = None,
#         season_name: str = None,
#         site_name: str = None,
#         plot_numbers: List[int] = None,
#         plot_column_numbers: List[int] = None,
#         plot_row_numbers: List[int] = None,
#         record_info: List[dict] = None,
#     ):

#         if timestamps is None:
#             timestamps = [datetime.now() for _ in range(len(script_data))]

#         if len(timestamps) != len(script_data):
#             raise ValueError(
#                 "The number of timestamps must match the number of records"
#             )

#         records = ScriptRecord.create_bulk(
#             timestamps=timestamps,
#             collection_dates=[timestamp.date() for timestamp in timestamps],
#             experiment_name=experiment_name,
#             season_name=season_name,
#             site_name=site_name,
#             plot_numbers=plot_numbers,
#             plot_column_numbers=plot_column_numbers,
#             plot_row_numbers=plot_row_numbers,
#             script_name=self.script_name,
#             script_data=script_data,
#             record_info=record_info,
#         )

#         logger_service.info(
#             "API",
#             f"Added records to {self.script_name} in the database",
#         )

#         return records

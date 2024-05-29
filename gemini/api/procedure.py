from typing import List, Optional, Any
from pydantic import Field
from gemini.api.base import APIBase
from gemini.api.dataset import Dataset
from gemini.api.procedure_run import ProcedureRun
from gemini.logger import logger_service
from gemini.models import ProcedureModel


class Procedure(APIBase):
    
    db_model = ProcedureModel

    procedure_name: str
    procedure_info: Optional[dict] = None

    datasets: Optional[List[Dataset]] = None
    procedure_runs: Optional[List[ProcedureRun]] = None

    @classmethod
    def create(
        cls,
        procedure_name: str,
        procedure_info: dict = None
    ):
        db_instance = ProcedureModel.get_or_create(
            procedure_name=procedure_name,
            procedure_info=procedure_info
        )
        instance = cls.model_validate(db_instance)
        logger_service.info(
            "API",
            f"Created a new instance of {cls.__name__} with id {instance.id}",
        )
        return instance
    
    @classmethod
    def get(cls, procedure_name: str) -> "Procedure":
        db_instance = ProcedureModel.get_by_parameters(procedure_name=procedure_name)
        logger_service.info("API", f"Retrieved procedure with name {procedure_name} from the database")
        return cls.model_validate(db_instance)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.procedure_name} from the database")
        return self.procedure_info
    
    def set_info(self, procedure_info: Optional[dict] = None) -> "Procedure":
        self.update(procedure_info=procedure_info)
        logger_service.info("API", f"Set information about {self.procedure_name} in the database")
        return self
    
    def add_info(self, procedure_info: Optional[dict] = None) -> "Procedure":
        current_info = self.get_info()
        updated_info = {**current_info, **procedure_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information to {self.procedure_name} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Procedure":
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove} 
        self.update(procedure_info=current_info)
        logger_service.info("API", f"Removed information from {self.procedure_name} in the database")
        return self
    
    def get_datasets(self) -> List[Dataset]:
        self.refresh()
        logger_service.info("API", f"Retrieved datasets for {self.procedure_name} from the database")
        return self.datasets
    
    def get_procedure_runs(self) -> List[ProcedureRun]:
        self.refresh()
        logger_service.info("API", f"Retrieved procedure runs for {self.procedure_name} from the database")
        return self.procedure_runs
    
    # Todo: Add, remove, and get datasets from a procedure
    # Todo: Add, remove, and get procedure runs from a procedure
    # Todo: Add, remove, and get records from a procedure

# from typing import List, Optional, Any
# from pydantic import Field
# from gemini.api.base import APIBase
# from gemini.api.procedure_record import ProcedureRecord
# from gemini.models.procedures import ProcedureModel

# from gemini.logger import logger_service
# import pandas as pd
# from datetime import datetime


# class Procedure(APIBase):

#     db_model = ProcedureModel

#     procedure_name: str = Field(..., title="Procedure Name", alias="procedure_name")
#     procedure_info: Optional[dict] = Field(
#         None, title="Procedure Information", alias="procedure_info"
#     )

#     datasets: Optional[List[dict]] = Field(None, title="Datasets")

#     @classmethod
#     def create(cls, procedure_name: str, procedure_info: dict = None):
#         """
#         Create a new procedure

#         Args:
#         procedure_name (str): The name of the procedure
#         procedure_info (dict, optional): The information about the procedure. Defaults to None.

#         Returns:
#         Procedure: The created procedure
#         """
#         new_instance = cls.db_model.get_or_create(
#             procedure_name=procedure_name,
#             procedure_info=procedure_info,
#         )
#         logger_service.info(
#             "API",
#             f"Created a new procedure with name {new_instance.procedure_name} in the database",
#         )
#         new_instance = cls.model_validate(new_instance)
#         return new_instance

#     def get_info(self) -> dict:
#         """
#         Get the information about a procedure

#         Returns:
#         dict: The information about the procedure
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved information about {self.procedure_name} from the database",
#         )
#         return self.procedure_info

#     def set_info(self, procedure_info: Optional[dict] = None) -> "Procedure":
#         """
#         Set the information about a procedure

#         Args:
#         procedure_info (Optional[dict], optional): The information to set. Defaults to None.

#         Returns:
#         Procedure: The procedure with the updated information
#         """
#         self.update(procedure_info=procedure_info)
#         logger_service.info(
#             "API",
#             f"Updated information about {self.procedure_name} in the database",
#         )
#         return self

#     def add_info(self, procedure_info: Optional[dict] = None) -> "Procedure":
#         """
#         Add information to a procedure

#         Args:
#         procedure_info (Optional[dict], optional): The information to add. Defaults to None.

#         Returns:
#         Procedure: The procedure with the added information
#         """
#         current_info = self.get_info()
#         if current_info is None:
#             current_info = {}
#         if procedure_info is not None:
#             current_info.update(procedure_info)
#         self.update(procedure_info=current_info)
#         logger_service.info(
#             "API",
#             f"Added information to {self.procedure_name} in the database",
#         )
#         return self

#     def remove_info(self, keys_to_remove: List[str]) -> "Procedure":
#         """
#         Remove information from a procedure

#         Args:
#         keys_to_remove (List[str]): The keys to remove

#         Returns:
#         Procedure: The procedure with the removed information
#         """
#         current_info = self.get_info()
#         for key in keys_to_remove:
#             current_info.pop(key, None)
#         self.update(procedure_info=current_info)
#         logger_service.info(
#             "API",
#             f"Removed information from {self.procedure_name} in the database",
#         )
#         return self

#     def get_datasets(self) -> List[dict]:
#         """
#         Get the datasets associated with a procedure

#         Returns:
#         List[Any]: The datasets associated with the procedure
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved datasets associated with {self.procedure_name} from the database",
#         )
#         return self.datasets

#     # Todo: Adding, removing, and getting datasets from a procedure
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
#     ) -> List[ProcedureRecord]:
#         """
#         Get records associated with a procedure

#         Args:
#         collection_date (Optional[str], optional): The collection date of the record. Defaults to None.
#         experiment (Optional[str], optional): The experiment of the record. Defaults to None.
#         season (Optional[str], optional): The season of the record. Defaults to None.
#         site (Optional[str], optional): The site of the record. Defaults to None.
#         plot_number (Optional[str], optional): The plot number of the record. Defaults to None.
#         plot_row_number (Optional[str], optional): The plot row number of the record. Defaults to None.
#         plot_column_number (Optional[str], optional): The plot column number of the record. Defaults to None.
#         record_info (Optional[dict], optional): The information about the record. Defaults to None.
#         as_dataframe (bool, optional): Return the records as a dataframe. Defaults to False.

#         Returns:
#         List[ProcedureRecord]: The records associated with the procedure
#         """
#         self.refresh()
#         searched_records = ProcedureRecord.search(
#             collection_date=collection_date,
#             experiment_name=experiment,
#             season_name=season,
#             site_name=site,
#             procedure_name=self.procedure_name,
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#             record_info=record_info,
#         )
#         logger_service.info(
#             "API",
#             f"Retrieved records associated with {self.procedure_name} from the database",
#         )
#         if as_dataframe:
#             searched_records = [record.model_dump() for record in searched_records]
#             searched_records = pd.DataFrame(searched_records)
#         return searched_records

#     def add_record(
#         self,
#         timestamp: datetime,
#         collection_date: datetime,
#         procudure_data: dict,
#         record_info: dict = None,
#         experiment_name: str = None,
#         season_name: str = None,
#         site_name: str = None,
#         plot_number: int = None,
#         plot_row_number: int = None,
#         plot_column_number: int = None,
#     ):
#         """
#         Add a record to a procedure

#         Args:
#         timestamp (str): The timestamp of the record
#         collection_date (str): The collection date of the record
#         procedure_data (dict): The data of the record
#         record_info (dict, optional): The information about the record. Defaults to None.
#         experiment_name (str, optional): The experiment name. Defaults to None.
#         season_name (str, optional): The season name. Defaults to None.
#         site_name (str, optional): The site name. Defaults to None.
#         plot_number (int, optional): The plot number. Defaults to None.
#         plot_row_number (int, optional): The plot row number. Defaults to None.
#         plot_column_number (int, optional): The plot column number. Defaults to None.

#         Returns:
#         ProcedureRecord: The added record
#         """
#         new_record = ProcedureRecord.create(
#             timestamp=timestamp,
#             collection_date=collection_date,
#             procedure_data=procudure_data,
#             record_info=record_info,
#             experiment_name=experiment_name,
#             season_name=season_name,
#             site_name=site_name,
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#             procedure_name=self.procedure_name,
#         )
#         logger_service.info(
#             "API",
#             f"Added a record to {self.procedure_name} in the database",
#         )
#         return new_record

#     def add_records(
#         self,
#         procedure_data: List[dict],
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
#             timestamps = [datetime.now() for _ in range(len(procedure_data))]

#         if len(timestamps) != len(procedure_data):
#             raise ValueError(
#                 "Timestamps and collection dates must have the same length"
#             )

#         records = ProcedureRecord.create_bulk(
#             timestamps=timestamps,
#             collection_dates=[timestamp.date() for timestamp in timestamps],
#             experiment_name=experiment_name,
#             season_name=season_name,
#             site_name=site_name,
#             plot_numbers=plot_numbers,
#             plot_column_numbers=plot_column_numbers,
#             plot_row_numbers=plot_row_numbers,
#             procedure_name=self.procedure_name,
#             procedure_data=procedure_data,
#             record_info=record_info,
#         )

#         logger_service.info(
#             "API",
#             f"Added records to {self.procedure_name} in the database",
#         )

#         return records

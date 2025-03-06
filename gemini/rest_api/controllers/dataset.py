from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.dataset import Dataset
from gemini.api.enums import GEMINIDatasetType
from gemini.rest_api.models import ( 
    DatasetInput, 
    DatasetOutput, 
    RESTAPIError, 
    DatasetUpdate, 
    str_to_dict, 
    JSONB
)

from typing import List, Annotated, Optional

class DatasetController(Controller):

    # Get Datasets
    @get()
    async def get_datasets(
        self,
        dataset_name: Optional[str] = None,
        dataset_info: Optional[JSONB] = None,
        dataset_type_id: Optional[int] = None,
        experiment_name: Optional[str] = 'Experiment A',
        collection_date: Optional[str] = None
    ) -> List[DatasetOutput]:
        try:
            if dataset_info is not None:
                dataset_info = str_to_dict(dataset_info)

            datasets = Dataset.search(
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                dataset_type=GEMINIDatasetType(dataset_type_id),
                experiment_name=experiment_name,
                collection_date=collection_date
            )
            if datasets is None:
                error_html = RESTAPIError(
                    error="No datasets found",
                    error_description="No datasets were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return datasets
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving datasets"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Dataset by ID
    @get(path="/id/{dataset_id:str}")
    async def get_dataset_by_id(
        self, dataset_id: str
    ) -> DatasetOutput:
        try:
            dataset = Dataset.get_by_id(id=dataset_id)
            if dataset is None:
                error_html = RESTAPIError(
                    error="Dataset not found",
                    error_description="No dataset was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return dataset
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the dataset"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Create Dataset
    @post()
    async def create_dataset(
        self, data: Annotated[DatasetInput, Body]
    ) -> DatasetOutput:
        try:
            dataset = Dataset.create(
                collection_date=data.collection_date,
                dataset_name=data.dataset_name,
                dataset_info=data.dataset_info,
                dataset_type=GEMINIDatasetType(data.dataset_type_id),
                experiment_name=data.experiment_name
            )
            if dataset is None:
                error_html = RESTAPIError(
                    error="Dataset not created",
                    error_description="The dataset was not created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return dataset
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the dataset"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Update Dataset
    @patch(path="/id/{dataset_id:str}")
    async def update_dataset(
        self, dataset_id: str, data: Annotated[DatasetUpdate, Body]
    ) -> DatasetOutput:
        try:
            dataset = Dataset.get_by_id(id=dataset_id)
            if dataset is None:
                error_html = RESTAPIError(
                    error="Dataset not found",
                    error_description="No dataset was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            
            dataset = dataset.update(
                collection_date=data.collection_date,
                dataset_name=data.dataset_name,
                dataset_info=data.dataset_info,
                dataset_type=GEMINIDatasetType(data.dataset_type_id)
            )
            if dataset is None:
                error_html = RESTAPIError(
                    error="Dataset not updated",
                    error_description="The dataset could not be updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return dataset
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the dataset"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Delete Dataset
    @delete(path="/id/{dataset_id:str}")
    async def delete_dataset(
        self, dataset_id: str
    ) -> None:
        try:
            dataset = Dataset.get_by_id(id=dataset_id)
            if dataset is None:
                error_html = RESTAPIError(
                    error="Dataset not found",
                    error_description="No dataset was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = dataset.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Dataset not deleted",
                    error_description="The dataset could not be deleted"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return None
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the dataset"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
        







    # # Get Datasets
    # @get()
    # async def get_datasets(
    #     self,
    #     collection_date: Optional[str] = None,
    #     dataset_name: Optional[str] = None,
    #     dataset_info: Optional[JSONB] = None,
    #     dataset_type_id: Optional[int] = None,
    #     experiment_name: Optional[str] = 'Default'
    # ) -> List[DatasetOutput]:
    #     try:

    #         if dataset_info is not None:
    #             dataset_info = str_to_dict(dataset_info)

    #         datasets = Dataset.search(
    #             collection_date=collection_date,
    #             dataset_name=dataset_name,
    #             dataset_info=dataset_info,
    #             dataset_type_id=dataset_type_id,
    #             experiment_name=experiment_name
    #         )
    #         if datasets is None:
    #             error_html = RESTAPIError(
    #                 error="No datasets found",
    #                 error_description="No datasets were found with the given search criteria"
    #             ).to_html()
    #             return Response(content=error_html, status_code=404)
    #         return datasets
    #     except Exception as e:
    #         error_message = RESTAPIError(
    #             error=str(e),
    #             error_description="An error occurred while retrieving datasets"
    #         )
    #         error_html = error_message.to_html()
    #         return Response(content=error_html, status_code=500)
        
    
    # # Get Dataset by ID
    # @get(path="/id/{dataset_id:str}")
    # async def get_dataset_by_id(
    #     self, dataset_id: str
    # ) -> DatasetOutput:
    #     try:
    #         dataset = Dataset.get_by_id(id=dataset_id)
    #         if dataset is None:
    #             error_html = RESTAPIError(
    #                 error="Dataset not found",
    #                 error_description="No dataset was found with the given ID"
    #             ).to_html()
    #             return Response(content=error_html, status_code=404)
    #         return dataset
    #     except Exception as e:
    #         error_message = RESTAPIError(
    #             error=str(e),
    #             error_description="An error occurred while retrieving the dataset"
    #         )
    #         error_html = error_message.to_html()
    #         return Response(content=error_html, status_code=500)
        
    # # Create Dataset
    # @post()
    # async def create_dataset(
    #     self, data: Annotated[DatasetInput, Body]
    # ) -> DatasetOutput:
    #     try:

    #         dataset_type = GEMINIDatasetType(data.dataset_type_id)

    #         dataset = Dataset.create(
    #             collection_date=data.collection_date,
    #             dataset_name=data.dataset_name,
    #             dataset_info=data.dataset_info,
    #             dataset_type = dataset_type,
    #             experiment_name=data.experiment_name
    #         )
    #         return dataset
    #     except Exception as e:
    #         error_message = RESTAPIError(
    #             error=str(e),
    #             error_description="An error occurred while creating the dataset"
    #         )
    #         error_html = error_message.to_html()
    #         return Response(content=error_html, status_code=500)
        
    # # Update Dataset
    # @patch(path="/id/{dataset_id:str}")
    # async def update_dataset(
    #     self, dataset_id: str, data: Annotated[DatasetUpdate, Body]
    # ) -> DatasetOutput:
    #     try:
    #         dataset = Dataset.get_by_id(id=dataset_id)
    #         if dataset is None:
    #             error_html = RESTAPIError(
    #                 error="Dataset not found",
    #                 error_description="No dataset was found with the given ID"
    #             ).to_html()
    #             return Response(content=error_html, status_code=404)
            
    #         parameters = data.model_dump()
    #         dataset = dataset.update(**parameters)
    #         return dataset
    #     except Exception as e:
    #         error_message = RESTAPIError(
    #             error=str(e),
    #             error_description="An error occurred while updating the dataset"
    #         )
    #         error_html = error_message.to_html()
    #         return Response(content=error_html, status_code=500)
        
    

    # # Delete Dataset
    # @delete(path="/id/{dataset_id:str}")
    # async def delete_dataset(
    #     self, dataset_id: str
    # ) -> None:
    #     try:
    #         dataset = Dataset.get_by_id(id=dataset_id)
    #         if dataset is None:
    #             error_html = RESTAPIError(
    #                 error="Dataset not found",
    #                 error_description="No dataset was found with the given ID"
    #             ).to_html()
    #             return Response(content=error_html, status_code=404)
    #         dataset.delete()
    #     except Exception as e:
    #         error_message = RESTAPIError(
    #             error=str(e),
    #             error_description="An error occurred while deleting the dataset"
    #         )
    #         error_html = error_message.to_html()
    #         return Response(content=error_html, status_code=500)
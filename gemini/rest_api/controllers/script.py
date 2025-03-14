from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.script import Script
from gemini.rest_api.models import ( 
    ScriptInput, 
    ScriptOutput, 
    ScriptUpdate,
    ScriptRunInput,
    ScriptRunOutput,
    DatasetInput,
    DatasetOutput, 
 RESTAPIError, 
    JSONB, 
    str_to_dict
)

from typing import List, Annotated, Optional

class ScriptController(Controller):

    # Get Scripts
    @get()
    async def get_scripts(
        self,
        script_name: Optional[str] = None,
        script_url: Optional[str] = None,
        script_extension: Optional[str] = None,
        script_info: Optional[JSONB] = None,
        experiment_name: Optional[str] = 'Experiment A'
    ) -> List[ScriptOutput]:
        try:
            if script_info is not None:
                script_info = str_to_dict(script_info)

            scripts = Script.search(
                script_name=script_name,
                script_url=script_url,
                script_extension=script_extension,
                script_info=script_info,
                experiment_name=experiment_name
            )
            if scripts is None:
                error_html = RESTAPIError(
                    error="No scripts found",
                    error_description="No scripts were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return scripts
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving scripts"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Script by ID
    @get(path="/id/{script_id:str}")
    async def get_script_by_id(
        self, script_id: str
    ) -> ScriptOutput:
        try:
            script = Script.get_by_id(id=script_id)
            if script is None:
                error_html = RESTAPIError(
                    error="Script not found",
                    error_description="The script with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return script
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the script"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Create Script
    @post()
    async def create_script(
        self,
        script: Annotated[ScriptInput, Body]
    ) -> ScriptOutput:
        try:
            script = Script.create(
                script_name=script.script_name,
                script_url=script.script_url,
                script_extension=script.script_extension,
                script_info=script.script_info,
                experiment_name=script.experiment_name
            )
            if script is None:
                error_html = RESTAPIError(
                    error="Script not created",
                    error_description="The script was not created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return script
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the script"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Update Script
    @patch(path="/id/{script_id:str}")
    async def update_script(
        self,
        script_id: str,
        data: Annotated[ScriptUpdate, Body]
    ) -> ScriptOutput:
        try:
            script = Script.get_by_id(id=script_id)
            if script is None:
                error_html = RESTAPIError(
                    error="Script not found",
                    error_description="The script with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            script = script.update(
                script_name=data.script_name,
                script_url=data.script_url,
                script_extension=data.script_extension,
                script_info=data.script_info
            )
            if script is None:
                error_html = RESTAPIError(
                    error="Script not updated",
                    error_description="The script was not updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return script
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the script"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Delete Script
    @delete(path="/id/{script_id:str}")
    async def delete_script(
        self,
        script_id: str
    ) -> None:
        try:
            script = Script.get_by_id(id=script_id)
            if script is None:
                error_html = RESTAPIError(
                    error="Script not found",
                    error_description="The script with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = script.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Script not deleted",
                    error_description="The script was not deleted"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return None
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the script"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Script Runs
    @get(path="/id/{script_id:str}/runs")
    async def get_script_runs(
        self, script_id: str
    ) -> List[ScriptRunOutput]:
        try:
            script = Script.get_by_id(id=script_id)
            if script is None:
                error_html = RESTAPIError(
                    error="Script not found",
                    error_description="The script with the given ID was not found"
                ).to_html()
            script_runs = script.get_runs()
            if script_runs is None:
                error_html = RESTAPIError(
                    error="No script runs found",
                    error_description="No script runs were found for the given script"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return script_runs
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving script runs"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Script Datasets
    @get(path="/id/{script_id:str}/datasets")
    async def get_script_datasets(
        self, script_id: str
    ) -> List[DatasetOutput]:
        try:
            script = Script.get_by_id(id=script_id)
            if script is None:
                error_html = RESTAPIError(
                    error="Script not found",
                    error_description="The script with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            datasets = script.get_datasets()
            if datasets is None:
                error_html = RESTAPIError(
                    error="No datasets found",
                    error_description="No datasets were found for the given script"
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
        
    # Create Script Run
    @post(path="/id/{script_id:str}/runs")
    async def create_script_run(
        self,
        script_id: str,
        data: Annotated[ScriptRunInput, Body]
    ) -> ScriptRunOutput:
        try:
            script = Script.get_by_id(id=script_id)
            if script is None:
                error_html = RESTAPIError(
                    error="Script not found",
                    error_description="The script with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            script_run = script.create_run(script_run_info=data.script_run_info)
            if script_run is None:
                error_html = RESTAPIError(
                    error="Script run not created",
                    error_description="The script run was not created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return script_run
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the script run"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Create Script Dataset
    @post(path="/id/{script_id:str}/datasets")
    async def create_script_dataset(
        self,
        script_id: str,
        data: Annotated[DatasetInput, Body]
    ) -> DatasetOutput:
        try:
            script = Script.get_by_id(id=script_id)
            if script is None:
                error_html = RESTAPIError(
                    error="Script not found",
                    error_description="The script with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            dataset = script.create_dataset(
                dataset_name=data.dataset_name,
                dataset_info=data.dataset_info,
                collection_date=data.collection_date,
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

        
     
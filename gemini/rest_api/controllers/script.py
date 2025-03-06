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
    RESTAPIBase, 
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
                error_html = RESTAPIBase(
                    error="No scripts found",
                    error_description="No scripts were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return scripts
        except Exception as e:
            error_message = RESTAPIBase(
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
                error_html = RESTAPIBase(
                    error="Script not found",
                    error_description="The script with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return script
        except Exception as e:
            error_message = RESTAPIBase(
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
                error_html = RESTAPIBase(
                    error="Script not created",
                    error_description="The script was not created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return script
        except Exception as e:
            error_message = RESTAPIBase(
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
                error_html = RESTAPIBase(
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
                error_html = RESTAPIBase(
                    error="Script not updated",
                    error_description="The script was not updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return script
        except Exception as e:
            error_message = RESTAPIBase(
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
                error_html = RESTAPIBase(
                    error="Script not found",
                    error_description="The script with the given ID was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = script.delete()
            if not is_deleted:
                error_html = RESTAPIBase(
                    error="Script not deleted",
                    error_description="The script was not deleted"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return None
        except Exception as e:
            error_message = RESTAPIBase(
                error=str(e),
                error_description="An error occurred while deleting the script"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)

        
        

    # # Get Scripts
    # @get()
    # async def get_scripts(
    #     self,
    #     script_name: Optional[str] = None,
    #     script_url: Optional[str] = None,
    #     script_extension: Optional[str] = None,
    #     script_info: Optional[JSONB] = None,
    #     experiment_name: Optional[str] = 'Default'
    # ) -> List[ScriptOutput]:
    #     try:
    #         if script_info is not None:
    #             script_info = str_to_dict(script_info)

    #         scripts = Script.search(
    #             script_name=script_name,
    #             script_url=script_url,
    #             script_extension=script_extension,
    #             script_info=script_info,
    #             experiment_name=experiment_name
    #         )

    #         if scripts is None:
    #             error_html = RESTAPIBase(
    #                 error="No scripts found",
    #                 error_description="No scripts were found with the given search criteria"
    #             ).to_html()
    #             return Response(content=error_html, status_code=404)
    #         return scripts
    #     except Exception as e:
    #         error_message = RESTAPIBase(
    #             error=str(e),
    #             error_description="An error occurred while retrieving scripts"
    #         )
    #         error_html = error_message.to_html()
    #         return Response(content=error_html, status_code=500)
        

    # # Get Script by ID
    # @get(path="/id/{script_id:str}")
    # async def get_script_by_id(
    #     self, script_id: str
    # ) -> ScriptOutput:
    #     try:
    #         script = Script.get_by_id(id=script_id)
    #         if script is None:
    #             error_html = RESTAPIBase(
    #                 error="Script not found",
    #                 error_description="The script with the given ID was not found"
    #             ).to_html()
    #             return Response(content=error_html, status_code=404)
    #         return script
    #     except Exception as e:
    #         error_message = RESTAPIBase(
    #             error=str(e),
    #             error_description="An error occurred while retrieving the script"
    #         )
    #         error_html = error_message.to_html()
    #         return Response(content=error_html, status_code=500)
        

    # # Create Script
    # async def create_script(
    #     self,
    #     script: Annotated[ScriptInput, Body]
    # ) -> ScriptOutput:
    #     try:
    #         script = Script.create(
    #             script_name=script.script_name,
    #             script_url=script.script_url,
    #             script_extension=script.script_extension,
    #             script_info=script.script_info,
    #             experiment_name=script.experiment_name
    #         )
    #         if script is None:
    #             error_html = RESTAPIBase(
    #                 error="Script not created",
    #                 error_description="The script was not created"
    #             ).to_html()
    #             return Response(content=error_html, status_code=500)
    #         return script
    #     except Exception as e:
    #         error_message = RESTAPIBase(
    #             error=str(e),
    #             error_description="An error occurred while creating the script"
    #         )
    #         error_html = error_message.to_html()
    #         return Response(content=error_html, status_code=500)
        

    # # Update Script
    # @patch(path="/id/{script_id:str}")
    # async def update_script(
    #     self,
    #     script_id: str,
    #     data: Annotated[ScriptUpdate, Body]
    # ) -> ScriptOutput:
    #     try:
    #         script = Script.get_by_id(id=script_id)
    #         if script is None:
    #             error_html = RESTAPIBase(
    #                 error="Script not found",
    #                 error_description="The script with the given ID was not found"
    #             ).to_html()
    #             return Response(content=error_html, status_code=404)
    #         parameters = data.model_dump()
    #         script = script.update(**parameters)
    #         return script
    #     except Exception as e:
    #         error_message = RESTAPIBase(
    #             error=str(e),
    #             error_description="An error occurred while updating the script"
    #         )
    #         error_html = error_message.to_html()
    #         return Response(content=error_html, status_code=500)
        

    # # Delete Script
    # @delete(path="/id/{script_id:str}")
    # async def delete_script(
    #     self, script_id: str
    # ) -> None:
    #     try:
    #         script = Script.get_by_id(id=script_id)
    #         if script is None:
    #             error_html = RESTAPIBase(
    #                 error="Script not found",
    #                 error_description="The script with the given ID was not found"
    #             ).to_html()
    #             return Response(content=error_html, status_code=404)
    #         script.delete()
    #     except Exception as e:
    #         error_message = RESTAPIBase(
    #             error=str(e),
    #             error_description="An error occurred while deleting the script"
    #         )
    #         error_html = error_message.to_html()
    #         return Response(content=error_html, status_code=500)
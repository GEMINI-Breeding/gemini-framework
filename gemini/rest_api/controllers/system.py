from litestar.controller import Controller
from litestar.handlers import get, post, put, delete, patch
from litestar.params import Body
from litestar import Response

from gemini.rest_api.worker import get_job_info

from saq import Job

class SystemController(Controller):
    
    @get('/job/{job_id:str}')
    async def get_job_info(self, job_id: str) -> dict:
        try:
            job_info = get_job_info(job_id)
            return job_info
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
        
        
from litestar.controller import Controller
from litestar.handlers import get, post, put, delete, patch
from litestar.params import Body
from litestar import Response

from saq import Job

class SystemController(Controller):
    
    @get('/job/{job_id:str}')
    async def get_job_info(self, job_id: str) -> dict:
        try:
            job = Job(key=job_id, function="get_system_time")
            await job.refresh()
            if not job:
                return Response(content="Job not found", status_code=404)
            job_info = job.to_dict()
            return job_info
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
        
        
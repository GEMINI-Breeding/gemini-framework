from litestar.controller import Controller
from litestar.handlers import get, post, put, delete, patch
from litestar.params import Body
from litestar import Response

from gemini.rest_api.worker import task_queue, get_job_info
from gemini.rest_api.src.models import JobInfo
from saq import Job

class SystemController(Controller):

    @get('/time')
    async def get_system_time(self) -> JobInfo:
        try:
            job = await task_queue.enqueue("get_system_time", timeout=20)
            job_info = JobInfo.from_job(job)
            if not job_info:
                return Response(content="Failed to get system time", status_code=500)
            return job_info
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    
    @get('/job/{job_id:str}')
    async def get_job_info(self, job_id: str) -> JobInfo:
        try:
            job_info = await get_job_info(job_id)
            return job_info
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
        
        
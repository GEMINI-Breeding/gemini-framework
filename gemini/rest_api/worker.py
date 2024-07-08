import asyncio, os
from saq import Queue

from gemini.rest_api.tasks import tasks
from gemini.rest_api.src.models import JobInfo


# REDIS Settings
islocal = os.getenv('GEMINI_IS_LOCAL')
islocal = True if islocal.lower() == 'true' else False
redis_host = os.getenv('LOGGER_HOSTNAME') if not islocal else 'localhost'
redis_password = os.getenv('LOGGER_PASSWORD')
redis_port = os.getenv('LOGGER_PORT')
redis_url = f'redis://{redis_password}@{redis_host}:{redis_port}'
task_queue = Queue.from_url(f'redis://{redis_host}:{redis_port}')

# Get Job Info
async def get_job_info(key: str, queue: str = "default") -> JobInfo:
    job = await task_queue.job(job_key=key)
    if not job:
        return None
    job_info = JobInfo.from_job(job)
    return job_info

# Startup Process
async def startup(ctx):
    print("Worker started")

# Shutdown Process
async def shutdown(ctx):
    print("Worker stopped")

# Worker Settings
settings = {
    "queue": task_queue,
    "concurrency": 10,  
    "functions": tasks,
    "startup": startup,
    "shutdown": shutdown,
}





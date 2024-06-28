import asyncio
from saq import Queue
import os

from gemini.rest_api.tasks import tasks

# REDIS
islocal = os.getenv('GEMINI_IS_LOCAL')
islocal = True if islocal.lower() == 'true' else False
redis_host = os.getenv('LOGGER_HOSTNAME') if not islocal else 'localhost'
redis_password = os.getenv('LOGGER_PASSWORD')
redis_port = os.getenv('LOGGER_PORT')
redis_url = f'redis://{redis_password}@{redis_host}:{redis_port}'

print(f"Connecting to Redis at {redis_url}")

task_queue = Queue.from_url(f'redis://{redis_host}:{redis_port}')


# Startup Process
async def startup(ctx):
    print("Worker started")

# Shutdown Process
async def shutdown(ctx):
    print("Worker stopped")


settings = {
    "queue": task_queue,
    "concurrency": 10,  
    "functions": tasks,
    "startup": startup,
    "shutdown": shutdown,
}





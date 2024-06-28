import asyncio
import time
from saq.types import Context

async def get_system_time(ctx : Context, **kwargs) -> int:
    await asyncio.sleep(10)
    return int(time.time())

tasks = [
    get_system_time
]


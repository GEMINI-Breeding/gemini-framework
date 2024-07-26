from celery import shared_task
from datetime import datetime
import time

@shared_task()
def get_system_time(pause_duration: int = 0) -> str:
    time.sleep(pause_duration)
    return {
        "system_time": datetime.now().isoformat(),
        "timezone": datetime.now().astimezone().tzinfo,
        "hours": datetime.now().hour,
        "minutes": datetime.now().minute,
        "seconds": datetime.now().second
    }
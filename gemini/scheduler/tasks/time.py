from prefect import task
import time, datetime

@task
def get_current_system_time() -> dict:
    current_time = time.localtime()
    return {
        "time": time.strftime("%Y-%m-%d %H:%M:%S", current_time),
        "year": current_time.tm_year,
        "month": current_time.tm_mon,
        "day": current_time.tm_mday,
        "hour": current_time.tm_hour,
        "minute": current_time.tm_min,
        "second": current_time.tm_sec,
        "millisecond": datetime.datetime.now().microsecond // 1000
    }
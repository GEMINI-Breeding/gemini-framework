from prefect import flow

import gemini.scheduler.tasks.time as time_tasks

@flow(retries=3, retry_delay_seconds=5, log_prints=True)
def get_current_system_time():
    return time_tasks.get_current_system_time()

if __name__ == "__main__":
    time = get_current_system_time()
    print(time)
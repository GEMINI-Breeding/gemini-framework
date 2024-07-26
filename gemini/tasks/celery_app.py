import os
from celery import Celery
from celery.bin import worker
from gemini.tasks.queues import task_queues
from multiprocessing import Process

def create_celery_app():
    redis_password = os.getenv('LOGGER_PASSWORD')
    redis_host = 'localhost'  # Replace with actual host
    redis_port = 6379  # Replace with actual port

    redis_broker_url = f'redis://{redis_host}:{redis_port}/0'
    redis_backend_url = f'redis://{redis_host}:{redis_port}/'

    celery_app = Celery('gemini', broker=redis_broker_url, backend=redis_backend_url)

    # Set up the task queues
    celery_app.conf.task_queues = task_queues
    celery_app.conf.task_default_queue = 'default'
    celery_app.conf.task_default_exchange = 'default'
    celery_app.conf.task_default_routing_key = 'default'

    # Add the broker_connection_retry_on_startup setting
    celery_app.conf.broker_connection_retry_on_startup = True

    return celery_app

def start_celery_worker(celery_app: Celery, queue_name: str = 'default', task_module: str = 'gemini.tasks.src.system'):
    worker_instance = celery_app.Worker(
        include=[task_module],
        queues=[queue_name],
        concurrency=1,
    )
    worker_instance.start()
    
def start_workers():
    celery_app = create_celery_app()
    processes = []
    
    for queue in task_queues.items():
        queue_name = queue[0]
        queue_info = queue[1]
        queue_module = queue_info['default_module']
        process = Process(target=start_celery_worker, args=(celery_app, queue_name, queue_module))
        processes.append(process)
        
    for process in processes:
        process.start()
        
    for process in processes:
        process.join()
        
if __name__ == '__main__':
    start_workers()
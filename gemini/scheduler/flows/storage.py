from prefect import flow

from gemini.scheduler.tasks.storage import get_object_info

@flow(
    name="get_object_info",
    description="Get object info from MinIO",
    retries=3,
    log_prints=True,
)
def get_object_info_flow(object_name: str, bucket_name: str = "gemini") -> dict:
    object_info = get_object_info(object_name=object_name, bucket_name=bucket_name)
    return object_info

minio_flow_deployments = [
    get_object_info_flow.to_deployment(
        name="get_object_info_flow",
        description="Get object info from MinIO",
        tags=["minio"],
    ),
]
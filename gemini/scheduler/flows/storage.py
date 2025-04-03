from prefect import flow

from typing import Optional, Dict

from gemini.scheduler.tasks.storage import (
    get_object_info,
    get_object_download_url,
    upload_object,
    delete_object
)

@flow(
    name="get_object_info",
    description="Get object info from MinIO",
    retries=3,
    log_prints=True,
)
def get_object_info_flow(object_name: str, bucket_name: str = "gemini") -> dict:
    object_info = get_object_info(object_name=object_name, bucket_name=bucket_name)
    return object_info


@flow(
    name="get_object_download_url",
    description="Get object download URL from MinIO",
    retries=3,
    log_prints=True,
)
def get_object_download_url_flow(object_name: str, bucket_name: str = "gemini") -> str:
    object_download_url = get_object_download_url(object_name=object_name, bucket_name=bucket_name)
    return object_download_url

@flow(
    name="upload_object",
    description="Upload object to MinIO",
    retries=3,
    log_prints=True,
)
def upload_object_flow(
    object_name: str,
    input_file_path: str,
    bucket_name: str = "gemini",
    metadata: Optional[Dict[str, str]] = None
) -> bool:
    upload_object(
        object_name=object_name,
        input_file_path=input_file_path,
        bucket_name=bucket_name,
        metadata=metadata
    )
    return True

@flow(
    name="delete_object",
    description="Delete object from MinIO",
    retries=3,
    log_prints=True,
)
def delete_object_flow(object_name: str, bucket_name: str = "gemini") -> bool:
    delete_object(object_name=object_name, bucket_name=bucket_name)
    return True


minio_flow_deployments = [
    get_object_info_flow.to_deployment(
        name="get_object_info_flow",
        description="Get object info from MinIO",
        tags=["minio"],
    ),
    get_object_download_url_flow.to_deployment(
        name="get_object_download_url_flow",
        description="Get object download URL from MinIO",
        tags=["minio"],
    ),
    upload_object_flow.to_deployment(
        name="upload_object_flow",
        description="Upload object to MinIO",
        tags=["minio"],
    ),
    delete_object_flow.to_deployment(
        name="delete_object_flow",
        description="Delete object from MinIO",
        tags=["minio"],
    ),
]
from gemini.storage.providers.minio_storage import MinioStorageProvider
from gemini.manager import GEMINIManager, GEMINIComponentType

from prefect import task

from typing import Optional, Dict
from mimetypes import guess_type

minio_storage_provider = GEMINIManager().get_component_provider(GEMINIComponentType.STORAGE)

@task(
    name="get_object_info",
    description="Get object info from MinIO",
    tags=["minio"],
    retries=3,
    log_prints=True,
)
def get_object_info(object_name: str, bucket_name: str = "gemini") -> dict:
    object_info = minio_storage_provider.get_file_metadata(
        object_name=object_name,
        bucket_name=bucket_name,
    )
    print(f"Object info: {object_info}")
    return object_info

@task(
    name="get_object_download_url",
    description="Get object download URL from MinIO",
    tags=["minio"],
    retries=3,
    log_prints=True,
)
def get_object_download_url(object_name: str, bucket_name: str = "gemini") -> str:
    object_download_url = minio_storage_provider.get_download_url(
        object_name=object_name,
        bucket_name=bucket_name,
    )
    print(f"Object download URL: {object_download_url}")
    return object_download_url

@task(
    name="upload_object",
    description="Upload object to MinIO",
    tags=["minio"],
    retries=3,
    log_prints=True,
)
def upload_object(
    object_name: str,
    input_file_path: str,
    bucket_name: str = "gemini",
    metadata: Optional[Dict[str, str]] = None
) -> bool:
    try:
        with open(input_file_path, "rb") as file:
            minio_storage_provider.upload_file(
                object_name=object_name,
                data_stream=file,
                content_type=guess_type(input_file_path)[0] or "application/octet-stream",
                metadata=metadata,
                bucket_name=bucket_name
            )
        print(f"Uploaded {input_file_path} to {bucket_name}/{object_name}")
        return True
    except Exception as e:
        print(f"Failed to upload {input_file_path} to {bucket_name}/{object_name}: {e}")
        return False
    
@task(
    name="delete_object",
    description="Delete object from MinIO",
    tags=["minio"],
    retries=3,
    log_prints=True,
    
)
def delete_object(object_name: str, bucket_name: str = "gemini") -> bool:
    try:
        minio_storage_provider.delete_file(
            object_name=object_name,
            bucket_name=bucket_name,
        )
        print(f"Deleted {bucket_name}/{object_name}")
        return True
    except Exception as e:
        print(f"Failed to delete {bucket_name}/{object_name}: {e}")
        return False
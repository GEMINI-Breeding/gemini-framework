from gemini.storage.providers.minio_storage import MinioStorageProvider
from gemini.manager import GEMINIManager, GEMINIComponentType

from prefect import task

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
from gemini.object_store import storage_service
from prefect import task
import os


@task
def download_file(
    key: str,
    bucket: str = None,
    destination_folder: str = None
) -> str:
    """
    Download a file from the object store
    """
    try:
        downloaded_file_path = storage_service.download_file(
            key=key, bucket=bucket, destination_folder=destination_folder
        )
        return downloaded_file_path
    except Exception as e:
        return None
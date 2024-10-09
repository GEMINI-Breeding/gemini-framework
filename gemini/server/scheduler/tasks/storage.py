from dagster import asset, AssetExecutionContext
from dagster_aws.s3 import S3Resource
from dagster import asset, Config
import os

class S3StorageConfig(Config):
    bucket: str
    key: str

@asset
def file_info(context: AssetExecutionContext, s3: S3Resource, config: S3StorageConfig) -> dict:
    try:
        file_info = s3.get_client().head_object(
            Bucket=config.bucket, Key=config.key
        )
        context.log.info(f"File info: {file_info}")
        return file_info
    except Exception as e:
        context.log.error(f"Error getting file info: {e}")
        return None
    

@asset
def presigned_download_url(context: AssetExecutionContext, s3: S3Resource, config: S3StorageConfig) -> str:
    try:
        url = s3.get_client().generate_presigned_url(
            "get_object", Params={"Bucket": config.bucket, "Key": config.key}
        )
        context.log.info(f"Presigned download url: {url}")
        return url
    except Exception as e:
        context.log.error(f"Error getting presigned download url: {e}")
        return None

@asset
def presigned_upload_url(context: AssetExecutionContext, s3: S3Resource, config: S3StorageConfig) -> str:
    try:
        url = s3.get_client().generate_presigned_url(
            "put_object", Params={"Bucket": config.bucket, "Key": config.key}
        )
        context.log.info(f"Presigned upload url: {url}")
        return url
    except Exception as e:
        context.log.error(f"Error getting presigned upload url: {e}")
        return None

@asset
def downloaded_file(context: AssetExecutionContext, s3: S3Resource, config: S3StorageConfig) -> str:
    try:
        download_path = f"/tmp/gemini/{config.key}"
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        s3.get_client().download_file(config.bucket, config.key, download_path)
        context.log.info(f"Downloaded file: {download_path}")
        return download_path
    except Exception as e:
        context.log.error(f"Error downloading file: {e}")
        return None


storage_assets = [
    file_info,
    presigned_download_url,
    presigned_upload_url,
    downloaded_file
]
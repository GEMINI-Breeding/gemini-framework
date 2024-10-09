import os
from dagster import Definitions
from dagster_aws.s3 import S3Resource

from tasks.storage import storage_assets
from tasks.amiga import amiga_assets

is_local = os.getenv("GEMINI_LOCAL") == "true"
minio_hostname = os.getenv("MINIO_HOSTNAME") if not is_local else "localhost"
minio_port = os.getenv("MINIO_PORT", 9000)
minio_access_key = os.getenv("MINIO_ACCESS_KEY")
minio_secret_key = os.getenv("MINIO_SECRET_KEY")
minio_secure = False

minio_resource = S3Resource(
    endpoint_url=f"http://{minio_hostname}:{minio_port}",
    use_ssl=minio_secure,
    aws_access_key_id=minio_access_key,
    aws_secret_access_key=minio_secret_key,
)

defs = Definitions(
    assets=[*storage_assets, *amiga_assets],
    resources={"s3": minio_resource},
)
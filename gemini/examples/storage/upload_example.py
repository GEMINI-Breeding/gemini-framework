from gemini.storage.config import MinioStorageConfig
from gemini.storage.providers.minio_storage import MinioStorageProvider

from gemini.config.settings import GEMINISettings

import os

minio_config = MinioStorageConfig(
    endpoint="localhost:9000",
    access_key="gemini_storage_user",
    secret_key="gemini_secret",
    bucket_name="gemini",
    region="us-west-1",
    secure=False
)

print(minio_config)

minio_storage = MinioStorageProvider(config=minio_config)

print(minio_storage)

# Get Storage config from settings
settings = GEMINISettings()
print(settings.get_storage_config())

# Get the current script directory
current_dir = os.path.dirname(os.path.realpath(__file__))
test_file = os.path.join(current_dir, "upload_example.txt")

# Turn into BinaryIO
with open(test_file, "rb") as f:
    binary_data = f.read()
    minio_storage.upload_file(
        object_name="upload_example.txt",
        data_stream=f
    )
    print("Uploaded file to storage provider")

# Download the same file that was uploaded
downloaded_file = minio_storage.download_file(
    object_name="upload_example.txt",
    file_path=os.path.join(current_dir, "downloaded_file.txt")
)

print(f"Downloaded file to {downloaded_file}")
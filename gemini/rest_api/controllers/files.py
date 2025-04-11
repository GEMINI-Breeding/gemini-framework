from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller
from litestar.response import Stream
from litestar.enums import RequestEncodingType

from urllib3.response import HTTPResponse
from mimetypes import guess_type

from gemini.rest_api.models import (
    RESTAPIError,
    FileMetadata,
    UploadFileRequest
)

from gemini.manager import GEMINIManager, GEMINIComponentType
from gemini.storage.providers.minio_storage import MinioStorageProvider
from gemini.storage.config.storage_config import MinioStorageConfig

from typing import Optional, List, Annotated

manager = GEMINIManager()
minio_storage_settings = manager.get_component_settings(GEMINIComponentType.STORAGE)
minio_storage_config = MinioStorageConfig(
    endpoint=f"{minio_storage_settings['GEMINI_STORAGE_HOSTNAME']}:{minio_storage_settings['GEMINI_STORAGE_PORT']}",
    access_key=minio_storage_settings['GEMINI_STORAGE_ACCESS_KEY'],
    secret_key=minio_storage_settings['GEMINI_STORAGE_SECRET_KEY'],
    bucket_name=minio_storage_settings['GEMINI_STORAGE_BUCKET_NAME'],
    secure=False
)
minio_storage_provider = MinioStorageProvider(minio_storage_config)

class FileController(Controller):

    @get(path="/metadata/{file_path:path}")
    async def get_file_metadata(
        self,
        file_path: str
    ) -> FileMetadata:
        try:
            bucket_name = file_path.split('/')[1]
            if not minio_storage_provider.bucket_exists(bucket_name):
                error_html = RESTAPIError(
                    error="Bucket not found",
                    error_description=f"Bucket {bucket_name} does not exist"
                ).to_html()
                return Response(content=error_html, status_code=404)
            object_name = '/'.join(file_path.split('/')[2:])
            file_exists = minio_storage_provider.file_exists(
                object_name=object_name,
                bucket_name=bucket_name
            )
            if not file_exists:
                error_html = RESTAPIError(
                    error="File not found",
                    error_description=f"File {file_path} does not exist"
                ).to_html()
                return Response(content=error_html, status_code=404)
            file_info = minio_storage_provider.get_file_metadata(
                object_name=object_name,
                bucket_name=bucket_name
            )
            return FileMetadata(
                bucket_name=file_info['bucket_name'],
                object_name=file_info['object_name'],
                size=file_info['size'],
                last_modified=file_info['last_modified'],
                content_type=file_info['content_type'],
                etag=file_info['etag']
            )
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving file metadata"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    @get(path="/download/{file_path:path}")
    async def download_file(
        self,
        file_path: str
    ) -> Stream:
        try:
            bucket_name = file_path.split('/')[1]
            if not minio_storage_provider.bucket_exists(bucket_name):
                error_html = RESTAPIError(
                    error="Bucket not found",
                    error_description=f"Bucket {bucket_name} does not exist"
                ).to_html()
                return Response(content=error_html, status_code=404)
            object_name = '/'.join(file_path.split('/')[2:])
            file_name = object_name.split('/')[-1]
            file_exists = minio_storage_provider.file_exists(
                object_name=object_name,
                bucket_name=bucket_name
            )
            if not file_exists:
                error_html = RESTAPIError(
                    error="File not found",
                    error_description=f"File {file_path} does not exist"
                ).to_html()
                return Response(content=error_html, status_code=404)
            file_stream = minio_storage_provider.download_file_stream(
                object_name=object_name,
                bucket_name=bucket_name
            )
            return Stream(
                content=file_stream.stream(),
                media_type=guess_type(file_name)[0] or "application/octet-stream",
                headers={"Content-Disposition": f"attachment; filename={file_name}"}
            )
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while downloading the file"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    @post(path="/upload")
    async def upload_file(
        self,
        data: Annotated[UploadFileRequest, Body(media_type=RequestEncodingType.MULTI_PART)]
    ) -> FileMetadata:
        try:
            bucket_name = data.bucket_name
            if not minio_storage_provider.bucket_exists(bucket_name):
                error_html = RESTAPIError(
                    error="Bucket not found",
                    error_description=f"Bucket {bucket_name} does not exist"
                ).to_html()
                return Response(content=error_html, status_code=404)
            file_stream = data.file.file
            minio_storage_provider.upload_file(
                bucket_name=bucket_name,
                object_name=data.object_name,
                data_stream=file_stream
            )
            file_info = minio_storage_provider.get_file_metadata(
                object_name=data.object_name,
                bucket_name=bucket_name
            )
            return FileMetadata(
                bucket_name=file_info['bucket_name'],
                object_name=file_info['object_name'],
                size=file_info['size'],
                last_modified=file_info['last_modified'],
                content_type=file_info['content_type'],
                etag=file_info['etag']
            )
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while uploading the file"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    @delete(path="/delete/{file_path:path}")
    async def delete_file(
        self,
        file_path: str
    ) -> None:
        try:
            bucket_name = file_path.split('/')[1]
            if not minio_storage_provider.bucket_exists(bucket_name):
                error_html = RESTAPIError(
                    error="Bucket not found",
                    error_description=f"Bucket {bucket_name} does not exist"
                ).to_html()
                return Response(content=error_html, status_code=404)
            object_name = '/'.join(file_path.split('/')[2:])
            file_exists = minio_storage_provider.file_exists(
                object_name=object_name,
                bucket_name=bucket_name
            )
            if not file_exists:
                error_html = RESTAPIError(
                    error="File not found",
                    error_description=f"File {file_path} does not exist"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = minio_storage_provider.delete_file(
                object_name=object_name,
                bucket_name=bucket_name
            )
            if not is_deleted:
                error_html = RESTAPIError(
                    error="File deletion failed",
                    error_description=f"Failed to delete file {file_path}"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return None
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the file"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)



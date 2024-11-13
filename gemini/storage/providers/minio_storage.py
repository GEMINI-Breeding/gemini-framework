# gemini/storage/providers/minio_storage.py

import os
from datetime import datetime, timedelta
from typing import BinaryIO, Optional, Union, Dict, Any
from pathlib import Path
from minio import Minio
from minio.error import S3Error
from urllib.parse import urlparse

from gemini.storage.interfaces.storage_provider import StorageProvider
from gemini.storage.config.storage_config import MinioStorageConfig
from gemini.storage.exceptions import (
    StorageError,
    StorageFileNotFoundError,
    StorageUploadError,
    StorageDownloadError,
    StorageDeleteError,
    StorageInitializationError,
    StorageConnectionError,
    StorageAuthError
)

class MinioStorageProvider(StorageProvider):
    """Provider for MinIO object storage."""

    def __init__(self, config: MinioStorageConfig):
        """Initialize MinIO client with configuration.
        
        Args:
            config: MinIO configuration
            
        Raises:
            StorageInitializationError: If client initialization fails
        """
        self.config = config
        try:
            self.client = Minio(
                endpoint=config.endpoint,
                access_key=config.access_key,
                secret_key=config.secret_key,
                secure=config.secure,
                region=config.region,
                http_client=config.http_client
            )
            self.bucket_name = config.bucket_name
        except Exception as e:
            raise StorageInitializationError(f"Failed to initialize MinIO client: {e}")

    def initialize(self) -> bool:
        """Initialize MinIO storage and create bucket if needed.
        
        Returns:
            bool: True if initialization successful
            
        Raises:
            StorageInitializationError: If initialization fails
        """
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name, self.config.region)
            return True
        except S3Error as e:
            raise StorageInitializationError(f"Failed to initialize MinIO storage: {e}")
        except Exception as e:
            raise StorageInitializationError(f"Unexpected error during initialization: {e}")

    def upload_file(
        self,
        object_name: str,
        data_stream: BinaryIO,
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> str:
        """Upload a file to MinIO storage.
        
        Args:
            object_name: Name/path of the object in storage
            data_stream: File-like object containing the data
            content_type: MIME type of the file
            metadata: Additional metadata to store
            
        Returns:
            str: URL for the uploaded file
            
        Raises:
            StorageUploadError: If upload fails
            StorageConnectionError: If connection fails
        """
        try:
            # Get file size
            data_stream.seek(0, os.SEEK_END)
            file_size = data_stream.tell()
            data_stream.seek(0)
            
            # Prepare metadata
            tags = metadata.copy() if metadata else {}
            if content_type:
                tags['Content-Type'] = content_type
            
            # Upload file
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=data_stream,
                length=file_size,
                content_type=content_type,
                metadata=tags
            )
            
            return self.get_download_url(object_name)
            
        except S3Error as e:
            if 'AccessDenied' in str(e):
                raise StorageAuthError(f"Access denied while uploading file: {e}")
            raise StorageUploadError(f"Failed to upload file: {e}")
        except ConnectionError as e:
            raise StorageConnectionError(f"Connection failed during upload: {e}")
        except Exception as e:
            raise StorageUploadError(f"Unexpected error during upload: {e}")

    def download_file(
        self,
        object_name: str,
        file_path: Union[str, Path]
    ) -> Path:
        """Download a file from MinIO storage.
        
        Args:
            object_name: Name/path of the object in storage
            file_path: Local path to save the file
            
        Returns:
            Path: Path where file was saved
            
        Raises:
            StorageDownloadError: If download fails
            StorageFileNotFoundError: If file doesn't exist
            StorageConnectionError: If connection fails
        """
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.client.fget_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                file_path=str(file_path)
            )
            
            return file_path
            
        except S3Error as e:
            if 'NoSuchKey' in str(e):
                raise StorageFileNotFoundError(f"File not found: {object_name}")
            elif 'AccessDenied' in str(e):
                raise StorageAuthError(f"Access denied while downloading file: {e}")
            raise StorageDownloadError(f"Failed to download file: {e}")
        except ConnectionError as e:
            raise StorageConnectionError(f"Connection failed during download: {e}")
        except Exception as e:
            raise StorageDownloadError(f"Unexpected error during download: {e}")

    def delete_file(self, object_name: str) -> bool:
        """Delete a file from MinIO storage.
        
        Args:
            object_name: Name/path of the object to delete
            
        Returns:
            bool: True if deletion was successful
            
        Raises:
            StorageDeleteError: If deletion fails
            StorageConnectionError: If connection fails
        """
        try:
            self.client.remove_object(
                bucket_name=self.bucket_name,
                object_name=object_name
            )
            return True
        except S3Error as e:
            if 'AccessDenied' in str(e):
                raise StorageAuthError(f"Access denied while deleting file: {e}")
            raise StorageDeleteError(f"Failed to delete file: {e}")
        except ConnectionError as e:
            raise StorageConnectionError(f"Connection failed during deletion: {e}")
        except Exception as e:
            raise StorageDeleteError(f"Unexpected error during deletion: {e}")

    def get_download_url(
        self,
        object_name: str,
        expires: Optional[datetime] = None,
        response_headers: Optional[Dict[str, str]] = None
    ) -> str:
        """Get a pre-signed URL for downloading the file.
        
        Args:
            object_name: Name/path of the object
            expires: URL expiration time
            response_headers: Headers for the response
            
        Returns:
            str: Pre-signed URL
            
        Raises:
            StorageError: If URL generation fails
            StorageFileNotFoundError: If file doesn't exist
        """
        try:
            # Ensure file exists
            if not self.file_exists(object_name):
                raise StorageFileNotFoundError(f"File not found: {object_name}")
            
            # Default expiration of 7 days if not specified
            if expires is None:
                expires = datetime.now() + timedelta(days=7)
                
            # Calculate expiration in seconds
            expiry = int((expires - datetime.now()).total_seconds())
            
            url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                expires=expiry,
                response_headers=response_headers
            )
            
            return url
            
        except S3Error as e:
            if 'AccessDenied' in str(e):
                raise StorageAuthError(f"Access denied while generating URL: {e}")
            raise StorageError(f"Failed to generate pre-signed URL: {e}")
        except ConnectionError as e:
            raise StorageConnectionError(f"Connection failed while generating URL: {e}")
        except Exception as e:
            raise StorageError(f"Unexpected error while generating URL: {e}")

    def list_files(
        self,
        prefix: Optional[str] = None,
        recursive: bool = True
    ) -> list[str]:
        """List all files in MinIO storage with given prefix.
        
        Args:
            prefix: Filter files by prefix
            recursive: Search recursively in directories
            
        Returns:
            list[str]: List of file paths
            
        Raises:
            StorageError: If listing fails
            StorageConnectionError: If connection fails
        """
        try:
            objects = self.client.list_objects(
                bucket_name=self.bucket_name,
                prefix=prefix,
                recursive=recursive
            )
            return [obj.object_name for obj in objects]
            
        except S3Error as e:
            if 'AccessDenied' in str(e):
                raise StorageAuthError(f"Access denied while listing files: {e}")
            raise StorageError(f"Failed to list files: {e}")
        except ConnectionError as e:
            raise StorageConnectionError(f"Connection failed while listing files: {e}")
        except Exception as e:
            raise StorageError(f"Unexpected error while listing files: {e}")

    def file_exists(self, object_name: str) -> bool:
        """Check if a file exists in MinIO storage.
        
        Args:
            object_name: Name/path of the object
            
        Returns:
            bool: True if file exists
            
        Raises:
            StorageConnectionError: If connection check fails
        """
        try:
            self.client.stat_object(
                bucket_name=self.bucket_name,
                object_name=object_name
            )
            return True
        except S3Error:
            return False
        except ConnectionError as e:
            raise StorageConnectionError(f"Connection failed while checking file: {e}")

    def get_file_metadata(self, object_name: str) -> Dict[str, Any]:
        """Get metadata for a file in MinIO storage.
        
        Args:
            object_name: Name/path of the object
            
        Returns:
            dict: File metadata including size, dates, content type and custom metadata
            
        Raises:
            StorageError: If metadata retrieval fails
            StorageFileNotFoundError: If file doesn't exist
            StorageConnectionError: If connection fails
        """
        try:
            stat = self.client.stat_object(
                bucket_name=self.bucket_name,
                object_name=object_name
            )
            
            return {
                'size': stat.size,
                'etag': stat.etag,
                'last_modified': stat.last_modified,
                'content_type': stat.content_type,
                'metadata': stat.metadata
            }
            
        except S3Error as e:
            if 'NoSuchKey' in str(e):
                raise StorageFileNotFoundError(f"File not found: {object_name}")
            elif 'AccessDenied' in str(e):
                raise StorageAuthError(f"Access denied while getting metadata: {e}")
            raise StorageError(f"Failed to get file metadata: {e}")
        except ConnectionError as e:
            raise StorageConnectionError(f"Connection failed while getting metadata: {e}")
        except Exception as e:
            raise StorageError(f"Unexpected error while getting metadata: {e}")
        
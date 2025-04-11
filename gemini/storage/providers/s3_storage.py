# gemini/storage/providers/s3_storage.py

import os
import sys
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
from datetime import datetime, timedelta, timezone
from typing import BinaryIO, Optional, Union, Dict, Any
from pathlib import Path

from gemini.storage.interfaces.storage_provider import StorageProvider
from gemini.storage.config.storage_config import S3StorageConfig
from gemini.storage.exceptions import (
    StorageError,
    StorageFileNotFoundError,
    StorageUploadError,
    StorageDownloadError,
    StorageDeleteError,
    StorageInitializationError,
    StorageConnectionError,
    StorageAuthError,
    StorageConfigurationError
)

class S3StorageProvider(StorageProvider):
    """Provider for AWS S3 object storage using Boto3."""

    def __init__(self, config: S3StorageConfig):
        """Initialize Boto3 S3 client with configuration.

        Args:
            config: S3 configuration

        Raises:
            StorageInitializationError: If client initialization fails
            StorageAuthError: If credentials are not found or invalid
        """
        self.config = config
        try:
            # Boto3 automatically searches for credentials (env vars, shared file, IAM role)
            # We provide them explicitly from config if available
            session = boto3.Session(
                aws_access_key_id=config.access_key,
                aws_secret_access_key=config.secret_key,
            )
            self.client = session.client(
                's3',
                endpoint_url=config.endpoint_url, # Optional: for S3-compatible storage
                config=Config(
                    region_name='us-east-1',
                    signature_version='v4'
                )
            )
            self.bucket_name = config.bucket_name
        except (NoCredentialsError, PartialCredentialsError) as e:
             raise StorageAuthError(f"AWS credentials not found or incomplete: {e}")
        except ClientError as e:
            raise StorageInitializationError(f"Failed to initialize Boto3 S3 client: {e}")
        except Exception as e:
            raise StorageInitializationError(f"Unexpected error during S3 client initialization: {e}")

    def initialize(self) -> bool:
        """Initialize S3 storage and check bucket existence.

        Returns:
            bool: True if initialization successful (bucket exists)

        Raises:
            StorageInitializationError: If initialization fails (bucket doesn't exist or access denied)
            StorageConnectionError: If connection to AWS fails
        """
        try:
            # Check if bucket exists and we have access
            self.client.head_bucket(Bucket=self.bucket_name)
            return True
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == '404': # Not Found
                raise StorageInitializationError(f"S3 bucket '{self.bucket_name}' not found.")
            elif error_code == '403': # Forbidden
                raise StorageAuthError(f"Access denied to S3 bucket '{self.bucket_name}'. Check permissions.")
            else:
                raise StorageConnectionError(f"Failed to connect or access S3 bucket '{self.bucket_name}': {e}")
        except Exception as e:
            raise StorageInitializationError(f"Unexpected error during S3 initialization: {e}")

    def upload_file(
        self,
        object_name: str,
        data_stream: Optional[BinaryIO] = None,
        input_file_path: Optional[Union[str, Path]] = None,
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        bucket_name: Optional[str] = None
    ) -> str:
        """Upload a file to S3 storage.

        Args:
            object_name: Name/path of the object in storage
            data_stream: File-like object containing the data
            input_file_path: Path to the local file to upload
            content_type: MIME type of the file
            metadata: Additional metadata (converted to string values for S3)

        Returns:
            str: Pre-signed URL for the uploaded file

        Raises:
            StorageUploadError: If upload fails
            StorageConnectionError: If connection fails
            StorageAuthError: If access is denied
            ValueError: If neither data_stream nor input_file_path is provided
        """
        target_bucket = bucket_name if bucket_name is not None else self.bucket_name
        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type
        if metadata:
            # S3 metadata values must be strings
            extra_args['Metadata'] = {k: str(v) for k, v in metadata.items()}

        try:
            if input_file_path:
                input_file_path = Path(input_file_path)
                self.client.upload_file(
                    Filename=str(input_file_path),
                    Bucket=target_bucket,
                    Key=object_name,
                    ExtraArgs=extra_args
                )
            elif data_stream:
                data_stream.seek(0) # Ensure stream is at the beginning
                self.client.upload_fileobj(
                    Fileobj=data_stream,
                    Bucket=target_bucket,
                    Key=object_name,
                    ExtraArgs=extra_args
                )
            else:
                 raise ValueError("Either data_stream or input_file_path must be provided")

            # Return a pre-signed URL as the identifier/URL
            return self.get_download_url(object_name, bucket_name=target_bucket)

        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == 'AccessDenied':
                raise StorageAuthError(f"Access denied while uploading to S3 bucket '{target_bucket}': {e}")
            else:
                raise StorageUploadError(f"Failed to upload file '{object_name}' to S3: {e}")
        except FileNotFoundError as e:
             raise StorageUploadError(f"Input file path not found: {input_file_path}")
        except Exception as e:
            # Catch potential connection errors implicitly handled by boto3/botocore
            if "Could not connect to the endpoint URL" in str(e):
                 raise StorageConnectionError(f"Connection failed during S3 upload: {e}")
            raise StorageUploadError(f"Unexpected error during S3 upload: {e}")

    def download_file(
        self,
        object_name: str,
        file_path: Union[str, Path],
        bucket_name: Optional[str] = None
    ) -> Path:
        """Download a file from S3 storage.

        Args:
            object_name: Name/path of the object in storage
            file_path: Local path to save the file
            bucket_name: Optional specific bucket name

        Returns:
            Path: Path where the file was saved

        Raises:
            StorageDownloadError: If download fails
            StorageFileNotFoundError: If file doesn't exist
            StorageConnectionError: If connection fails
            StorageAuthError: If access is denied
        """
        target_bucket = bucket_name if bucket_name is not None else self.bucket_name
        output_path = Path(file_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            self.client.download_file(
                Bucket=target_bucket,
                Key=object_name,
                Filename=str(output_path)
            )
            return output_path
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == '404' or 'NoSuchKey' in str(e): # Check both for robustness
                raise StorageFileNotFoundError(f"File '{object_name}' not found in S3 bucket '{target_bucket}'.")
            elif error_code == '403' or 'AccessDenied' in str(e):
                raise StorageAuthError(f"Access denied while downloading '{object_name}' from S3 bucket '{target_bucket}': {e}")
            else:
                raise StorageDownloadError(f"Failed to download file '{object_name}' from S3: {e}")
        except Exception as e:
            if "Could not connect to the endpoint URL" in str(e):
                 raise StorageConnectionError(f"Connection failed during S3 download: {e}")
            raise StorageDownloadError(f"Unexpected error during S3 download: {e}")

    def delete_file(self, object_name: str, bucket_name: str = None) -> bool:
        """Delete a file from S3 storage.

        Args:
            object_name: Name/path of the object to delete
            bucket_name: Optional specific bucket name

        Returns:
            bool: True if deletion was successful

        Raises:
            StorageDeleteError: If deletion fails
            StorageConnectionError: If connection fails
            StorageAuthError: If access is denied
        """
        target_bucket = bucket_name if bucket_name is not None else self.bucket_name
        try:
            self.client.delete_object(Bucket=target_bucket, Key=object_name)
            return True
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == 'AccessDenied':
                raise StorageAuthError(f"Access denied while deleting '{object_name}' from S3 bucket '{target_bucket}': {e}")
            else:
                # Note: delete_object doesn't typically fail if the object doesn't exist
                raise StorageDeleteError(f"Failed to delete file '{object_name}' from S3: {e}")
        except Exception as e:
            if "Could not connect to the endpoint URL" in str(e):
                 raise StorageConnectionError(f"Connection failed during S3 deletion: {e}")
            raise StorageDeleteError(f"Unexpected error during S3 deletion: {e}")

    def get_download_url(
        self,
        object_name: str,
        expires: Optional[Union[int, timedelta]] = 3600, # Default: 1 hour
        response_headers: Optional[Dict[str, str]] = None, # Note: Boto3 uses Response* params
        bucket_name: Optional[str] = None
    ) -> str:
        """Get a pre-signed URL for downloading the file.

        Args:
            object_name: Name/path of the object
            expires: URL expiration time in seconds or timedelta (default 1 hour)
            response_headers: Headers to override in the response (e.g., ContentDisposition)
            bucket_name: Optional specific bucket name

        Returns:
            str: Pre-signed URL

        Raises:
            StorageError: If URL generation fails
            StorageFileNotFoundError: If file doesn't exist (checked implicitly by generate_presigned_url)
            StorageAuthError: If access is denied
            StorageConnectionError: If connection fails
        """
        target_bucket = bucket_name if bucket_name is not None else self.bucket_name

        if isinstance(expires, timedelta):
            expires_in_seconds = int(expires.total_seconds())
        elif isinstance(expires, int):
            expires_in_seconds = expires
        else:
            expires_in_seconds = 3600 # Default to 1 hour if invalid type

        params = {
            'Bucket': target_bucket,
            'Key': object_name
        }
        if response_headers:
             # Map common headers to Boto3 presigned URL parameters if needed
             # Example: params['ResponseContentDisposition'] = response_headers.get('Content-Disposition')
             # For simplicity, we'll pass them directly if Boto3 supports them, otherwise ignore.
             # Boto3 supports ResponseCacheControl, ResponseContentDisposition, ResponseContentEncoding, etc.
             for k, v in response_headers.items():
                 # Basic mapping for common headers
                 param_key = f"Response{k.replace('-', '')}"
                 params[param_key] = v


        try:
            # First check if file exists to provide a clearer error
            self.file_exists(object_name, bucket_name=target_bucket)

            url = self.client.generate_presigned_url(
                ClientMethod='get_object',
                Params=params,
                ExpiresIn=expires_in_seconds
            )
            return url
        except StorageFileNotFoundError: # Re-raise the specific error from file_exists
             raise
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == 'AccessDenied':
                raise StorageAuthError(f"Access denied while generating URL for '{object_name}' in S3 bucket '{target_bucket}': {e}")
            elif error_code == 'NoSuchKey':
                 raise StorageFileNotFoundError(f"File '{object_name}' not found in S3 bucket '{target_bucket}' when generating URL.")
            else:
                raise StorageError(f"Failed to generate pre-signed URL for '{object_name}': {e}")
        except Exception as e:
            if "Could not connect to the endpoint URL" in str(e):
                 raise StorageConnectionError(f"Connection failed while generating S3 URL: {e}")
            raise StorageError(f"Unexpected error while generating S3 URL: {e}")

    def list_files(
        self,
        prefix: Optional[str] = None,
        recursive: bool = True, # S3 list_objects_v2 is recursive by default when prefix is used
        bucket_name: Optional[str] = None
    ) -> list[str]:
        """List all files in S3 storage with given prefix.

        Args:
            prefix: Filter files by prefix
            recursive: If False, uses '/' as delimiter (not fully supported by interface)
            bucket_name: Optional specific bucket name

        Returns:
            list[str]: List of file object keys (paths)

        Raises:
            StorageError: If listing fails
            StorageConnectionError: If connection fails
            StorageAuthError: If access is denied
        """
        target_bucket = bucket_name if bucket_name is not None else self.bucket_name
        paginator = self.client.get_paginator('list_objects_v2')
        list_kwargs = {'Bucket': target_bucket}
        if prefix:
            list_kwargs['Prefix'] = prefix
        # Note: The 'recursive' flag doesn't directly map well to S3's delimiter concept.
        # We'll ignore `recursive=False` for now as the interface doesn't specify delimiter behavior.
        # If `recursive=False` was critical, we'd add `Delimiter='/'` and process `CommonPrefixes`.

        file_list = []
        try:
            for page in paginator.paginate(**list_kwargs):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        file_list.append(obj['Key'])
            return file_list
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == 'AccessDenied':
                raise StorageAuthError(f"Access denied while listing files in S3 bucket '{target_bucket}': {e}")
            elif error_code == 'NoSuchBucket':
                 raise StorageFileNotFoundError(f"S3 bucket '{target_bucket}' not found during list operation.")
            else:
                raise StorageError(f"Failed to list files in S3 bucket '{target_bucket}': {e}")
        except Exception as e:
            if "Could not connect to the endpoint URL" in str(e):
                 raise StorageConnectionError(f"Connection failed during S3 list operation: {e}")
            raise StorageError(f"Unexpected error during S3 list operation: {e}")

    def file_exists(self, object_name: str, bucket_name: str = None) -> bool:
        """Check if a file exists in S3 storage.

        Args:
            object_name: Name/path of the object
            bucket_name: Optional specific bucket name

        Returns:
            bool: True if file exists

        Raises:
            StorageConnectionError: If connection check fails
            StorageAuthError: If access is denied
        """
        target_bucket = bucket_name if bucket_name is not None else self.bucket_name
        try:
            self.client.head_object(Bucket=target_bucket, Key=object_name)
            return True
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == '404' or error_code == 'NoSuchKey':
                return False
            elif error_code == '403' or error_code == 'AccessDenied':
                 # It exists but we can't access it - raise AuthError? Or return False?
                 # Let's raise AuthError as it indicates a permission issue, not non-existence.
                 raise StorageAuthError(f"Access denied checking existence of '{object_name}' in S3 bucket '{target_bucket}': {e}")
            else:
                # Treat other errors as connection/configuration issues
                raise StorageConnectionError(f"Failed to check file existence for '{object_name}' in S3: {e}")
        except Exception as e:
            if "Could not connect to the endpoint URL" in str(e):
                 raise StorageConnectionError(f"Connection failed while checking S3 file existence: {e}")
            raise StorageError(f"Unexpected error checking S3 file existence: {e}")


    def get_file_metadata(self, object_name: str, bucket_name: str = None) -> Dict[str, Any]:
        """Get metadata for a file in S3 storage.

        Args:
            object_name: Name/path of the object
            bucket_name: Optional specific bucket name

        Returns:
            dict: File metadata including size, last_modified, content_type, etag, and custom metadata

        Raises:
            StorageError: If metadata retrieval fails
            StorageFileNotFoundError: If file doesn't exist
            StorageConnectionError: If connection fails
            StorageAuthError: If access is denied
        """
        target_bucket = bucket_name if bucket_name is not None else self.bucket_name
        try:
            response = self.client.head_object(Bucket=target_bucket, Key=object_name)

            # Convert last_modified to timezone-aware datetime if not already
            last_modified = response.get('LastModified')
            if last_modified and not last_modified.tzinfo:
                 last_modified = last_modified.replace(tzinfo=timezone.utc)

            return {
                'bucket_name': target_bucket,
                'object_name': object_name,
                'size': response.get('ContentLength'),
                'etag': response.get('ETag', '').strip('"'), # Remove quotes from ETag
                'last_modified': last_modified,
                'content_type': response.get('ContentType'),
                'metadata': response.get('Metadata', {}) # Custom metadata
                # S3 head_object doesn't return creation date easily
            }

        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == '404' or error_code == 'NoSuchKey':
                raise StorageFileNotFoundError(f"File '{object_name}' not found in S3 bucket '{target_bucket}' for metadata retrieval.")
            elif error_code == '403' or error_code == 'AccessDenied':
                raise StorageAuthError(f"Access denied while getting metadata for '{object_name}' from S3 bucket '{target_bucket}': {e}")
            else:
                raise StorageError(f"Failed to get file metadata for '{object_name}' from S3: {e}")
        except Exception as e:
            if "Could not connect to the endpoint URL" in str(e):
                 raise StorageConnectionError(f"Connection failed while getting S3 metadata: {e}")
            raise StorageError(f"Unexpected error while getting S3 metadata: {e}")

    def healthcheck(self) -> bool:
        """Check the connection to AWS S3 and bucket accessibility.

        Returns:
            bool: True if the connection is successful and the bucket is accessible.

        Raises:
            StorageConnectionError: If the connection fails or the bucket is not accessible.
            StorageAuthError: If credentials are invalid or insufficient.
        """
        try:
            # head_bucket checks connection, authentication, and bucket presence
            self.client.head_bucket(Bucket=self.bucket_name)
            return True
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code')
            if error_code == '403': # Forbidden
                raise StorageAuthError(f"S3 healthcheck failed: Access denied to bucket '{self.bucket_name}'.")
            else: # Includes 404 Not Found, connection errors, etc.
                raise StorageConnectionError(f"S3 healthcheck failed for bucket '{self.bucket_name}': {e}")
        except (NoCredentialsError, PartialCredentialsError) as e:
             raise StorageAuthError(f"S3 healthcheck failed: AWS credentials error: {e}")
        except Exception as e:
            # Catch potential network errors or other unexpected issues
            raise StorageConnectionError(f"Unexpected error during S3 healthcheck: {e}")

# gemini/storage/config/storage_config.py

from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Optional, Dict, Any
from pathlib import Path
from gemini.storage.exceptions import StorageConfigurationError

class StorageConfig(BaseModel):
    """Base configuration for storage providers."""
    
    provider: str = Field(
        ...,  # Required field
        description="Name of the storage provider (local, minio, s3, azure)"
    )
    base_path: Optional[str] = Field(
        None,
        description="Base path prefix for all storage operations"
    )

    model_config = {
        "extra": "forbid"  # Prevent additional attributes
    }

class LocalStorageConfig(StorageConfig):
    """Configuration for local filesystem storage."""
    
    provider: str = Field(
        "local",
        frozen=True,
        description="Provider name, must be 'local'"
    )
    root_directory: Path = Field(
        ...,
        description="Root directory for file storage"
    )
    create_directory: bool = Field(
        True,
        description="Create root directory if it doesn't exist"
    )

    @field_validator('root_directory')
    @classmethod
    def validate_root_directory(cls, v: Path) -> Path:
        """Validate root directory path."""
        try:
            path = Path(v)
            return path.resolve()
        except Exception as e:
            raise StorageConfigurationError(f"Invalid root directory path: {e}")

class MinioStorageConfig(StorageConfig):
    """Configuration for MinIO object storage."""
    
    provider: str = Field(
        "minio",
        frozen=True,
        description="Provider name, must be 'minio'"
    )
    endpoint: str = Field(
        ...,
        description="MinIO server endpoint (e.g., 'localhost:9000')"
    )
    access_key: str = Field(
        ...,
        description="MinIO access key"
    )
    secret_key: str = Field(
        ...,
        description="MinIO secret key"
    )
    bucket_name: str = Field(
        ...,
        description="Name of the bucket to use"
    )
    secure: bool = Field(
        True,
        description="Use HTTPS for connection"
    )
    region: Optional[str] = Field(
        None,
        description="MinIO region name"
    )
    http_client: Optional[Dict[str, Any]] = Field(
        None,
        description="Custom HTTP client configuration"
    )

    @field_validator('endpoint')
    @classmethod
    def validate_endpoint(cls, v: str) -> str:
        """Validate MinIO endpoint."""
        if not v:
            raise StorageConfigurationError("MinIO endpoint cannot be empty")
        if '://' in v:
            raise StorageConfigurationError("Endpoint should not include protocol (http/https)")
        return v

    @model_validator(mode='after')
    def validate_credentials(self) -> 'MinioStorageConfig':
        """Validate that credentials are provided."""
        if not self.access_key or not self.secret_key:
            raise StorageConfigurationError("Both access_key and secret_key must be provided")
        return self

class S3StorageConfig(StorageConfig):
    """Configuration for AWS S3 storage."""
    
    provider: str = Field(
        "s3",
        frozen=True,
        description="Provider name, must be 's3'"
    )
    region: str = Field(
        ...,
        description="AWS region (e.g., 'us-east-1')"
    )
    access_key: str = Field(
        ...,
        description="AWS access key ID"
    )
    secret_key: str = Field(
        ...,
        description="AWS secret access key"
    )
    bucket_name: str = Field(
        ...,
        description="Name of the S3 bucket"
    )
    endpoint_url: Optional[str] = Field(
        None,
        description="Custom endpoint URL for S3-compatible storage"
    )

    @model_validator(mode='after')
    def validate_credentials(self) -> 'S3StorageConfig':
        """Validate that credentials are provided."""
        if not self.access_key or not self.secret_key:
            raise StorageConfigurationError("Both access_key and secret_key must be provided")
        return self

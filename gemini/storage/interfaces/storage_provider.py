# gemini/storage/interfaces/storage_provider.py

from abc import ABC, abstractmethod
from typing import BinaryIO, Optional, Union, Dict, Any
from pathlib import Path
from datetime import datetime
from gemini.server.storage.exceptions import StorageError

class StorageProvider(ABC):
    """Base interface for all storage providers.
    
    This interface defines the contract that all storage providers must implement.
    It provides a standard set of operations for file storage and retrieval,
    regardless of the underlying storage system (local, MinIO, S3, etc.).
    """
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize storage provider and create necessary resources.
        
        Returns:
            bool: True if initialization was successful
            
        Raises:
            StorageInitializationError: If initialization fails
        """
        pass

    @abstractmethod
    def upload_file(
        self, 
        object_name: str,
        data_stream: BinaryIO,
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> str:
        """Upload a file to storage.
        
        Args:
            object_name: Name/path of the object in storage
            data_stream: File-like object containing the data
            content_type: MIME type of the file
            metadata: Additional metadata
            
        Returns:
            str: URL or identifier for the uploaded file
            
        Raises:
            StorageUploadError: If upload fails
            StorageConnectionError: If connection fails
        """
        pass

    @abstractmethod
    def download_file(
        self, 
        object_name: str,
        file_path: Union[str, Path]
    ) -> Path:
        """Download a file from storage.
        
        Args:
            object_name: Name/path of the object in storage
            file_path: Local path to save the file
            
        Returns:
            Path: Path where the file was saved
            
        Raises:
            StorageDownloadError: If download fails
            StorageFileNotFoundError: If file doesn't exist
            StorageConnectionError: If connection fails
        """
        pass

    @abstractmethod
    def delete_file(self, object_name: str) -> bool:
        """Delete a file from storage.
        
        Args:
            object_name: Name/path of the object to delete
            
        Returns:
            bool: True if deletion was successful
            
        Raises:
            StorageDeleteError: If deletion fails
            StorageConnectionError: If connection fails
        """
        pass

    @abstractmethod
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
        pass
    
    @abstractmethod
    def list_files(
        self,
        prefix: Optional[str] = None,
        recursive: bool = True
    ) -> list[str]:
        """List all files in storage with given prefix.
        
        Args:
            prefix: Filter files by prefix
            recursive: Search recursively in directories
            
        Returns:
            list[str]: List of file paths
            
        Raises:
            StorageError: If listing fails
            StorageConnectionError: If connection fails
        """
        pass

    @abstractmethod
    def file_exists(self, object_name: str) -> bool:
        """Check if a file exists in storage.
        
        Args:
            object_name: Name/path of the object
            
        Returns:
            bool: True if file exists
            
        Raises:
            StorageConnectionError: If connection check fails
        """
        pass

    @abstractmethod
    def get_file_metadata(self, object_name: str) -> Dict[str, Any]:
        """Get metadata for a file.
        
        Args:
            object_name: Name/path of the object
            
        Returns:
            Dict[str, Any]: File metadata including:
                - size: File size in bytes
                - created: Creation timestamp
                - modified: Last modification timestamp
                - content_type: MIME type if available
                - metadata: Additional metadata dictionary
                
        Raises:
            StorageError: If metadata retrieval fails
            StorageFileNotFoundError: If file doesn't exist
            StorageConnectionError: If connection fails
        """
        pass
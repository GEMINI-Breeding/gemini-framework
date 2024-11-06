# gemini/storage/providers/local_storage.py

import os
import shutil
import mimetypes
import json
from datetime import datetime
from pathlib import Path
from typing import BinaryIO, Optional, Union, Dict, Any
from gemini.storage.interfaces.storage_provider import StorageProvider
from gemini.storage.config.storage_config import LocalStorageConfig
from gemini.storage.exceptions import (
    StorageError,
    StorageFileNotFoundError,
    StorageUploadError,
    StorageDownloadError,
    StorageDeleteError,
    StorageInitializationError
)

class LocalStorageProvider(StorageProvider):
    """Provider for local filesystem storage."""

    def __init__(self, config: LocalStorageConfig):
        """Initialize local storage provider.
        
        Args:
            config: Configuration for local storage
            
        Raises:
            StorageInitializationError: If initialization fails
        """
        self.config = config
        self.root_directory = Path(config.root_directory).resolve()
        
        if config.create_directory:
            try:
                self.root_directory.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise StorageInitializationError(f"Failed to create root directory: {e}")
        elif not self.root_directory.exists():
            raise StorageInitializationError(
                f"Storage directory {config.root_directory} does not exist"
            )
        
    def initialize(self) -> bool:
        """Initialize local storage.
        
        Returns:
            bool: True if initialization successful
            
        Raises:
            StorageInitializationError: If initialization fails
        """
        try:
            self.root_directory.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            raise StorageInitializationError(f"Failed to initialize local storage: {e}")

    def _get_full_path(self, object_name: str) -> Path:
        """Get full filesystem path for an object.
        
        Args:
            object_name: Relative path of the object
            
        Returns:
            Path: Full filesystem path
            
        Raises:
            StorageError: If path would escape root directory
        """
        # Clean the object name to prevent directory traversal
        clean_name = Path(object_name).parts
        full_path = (self.root_directory.joinpath(*clean_name)).resolve()
        
        if not str(full_path).startswith(str(self.root_directory)):
            raise StorageError(f"Access denied: {object_name} is outside root directory")
        return full_path

    def _save_metadata(self, file_path: Path, metadata: Dict[str, Any]) -> None:
        """Save metadata to a companion file.
        
        Args:
            file_path: Path of the main file
            metadata: Metadata to save
        """
        meta_path = file_path.with_suffix(file_path.suffix + '.meta')
        with open(meta_path, 'w') as f:
            json.dump(metadata, f, default=str)

    def _load_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Load metadata from companion file.
        
        Args:
            file_path: Path of the main file
            
        Returns:
            dict: Loaded metadata or empty dict if no metadata exists
        """
        meta_path = file_path.with_suffix(file_path.suffix + '.meta')
        if meta_path.exists():
            with open(meta_path, 'r') as f:
                return json.load(f)
        return {}

    def upload_file(
        self,
        object_name: str,
        data_stream: BinaryIO,
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> str:
        """Upload a file to local storage.
        
        Args:
            object_name: Destination path for the file
            data_stream: File-like object containing the data
            content_type: MIME type (stored in metadata file)
            metadata: Additional metadata to store
            
        Returns:
            str: Local file URL
            
        Raises:
            StorageUploadError: If upload fails
        """
        try:
            file_path = self._get_full_path(object_name)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file data
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(data_stream, f)
            
            # Store metadata if provided
            if metadata or content_type:
                meta_data = metadata or {}
                if content_type:
                    meta_data['content_type'] = content_type
                self._save_metadata(file_path, meta_data)
            
            return self.get_download_url(object_name)
            
        except Exception as e:
            raise StorageUploadError(f"Failed to upload file: {e}")

    def download_file(
        self,
        object_name: str,
        file_path: Union[str, Path]
    ) -> Path:
        """Download a file from local storage.
        
        Args:
            object_name: Path of the file in storage
            file_path: Destination path
            
        Returns:
            Path: Path where file was saved
            
        Raises:
            StorageDownloadError: If download fails
            StorageFileNotFoundError: If file doesn't exist
        """
        try:
            source_path = self._get_full_path(object_name)
            if not source_path.exists():
                raise StorageFileNotFoundError(f"File not found: {object_name}")
            
            dest_path = Path(file_path)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(source_path, dest_path)
            return dest_path
            
        except StorageFileNotFoundError:
            raise
        except Exception as e:
            raise StorageDownloadError(f"Failed to download file: {e}")

    def delete_file(self, object_name: str) -> bool:
        """Delete a file from local storage.
        
        Args:
            object_name: Path of the file to delete
            
        Returns:
            bool: True if deletion was successful
            
        Raises:
            StorageDeleteError: If deletion fails
        """
        try:
            file_path = self._get_full_path(object_name)
            if not file_path.exists():
                return False
                
            file_path.unlink()
            
            # Remove metadata file if it exists
            meta_path = file_path.with_suffix(file_path.suffix + '.meta')
            if meta_path.exists():
                meta_path.unlink()
                
            return True
            
        except Exception as e:
            raise StorageDeleteError(f"Failed to delete file: {e}")

    def get_download_url(
        self,
        object_name: str,
        expires: Optional[datetime] = None,
        response_headers: Optional[Dict[str, str]] = None
    ) -> str:
        """Get a local filesystem URL for the file.
        
        Args:
            object_name: Path of the file
            expires: Ignored for local storage
            response_headers: Ignored for local storage
            
        Returns:
            str: Local file URL
            
        Raises:
            StorageFileNotFoundError: If file doesn't exist
        """
        file_path = self._get_full_path(object_name)
        if not file_path.exists():
            raise StorageFileNotFoundError(f"File not found: {object_name}")
        return f"file://{file_path.absolute()}"

    def list_files(
        self,
        prefix: Optional[str] = None,
        recursive: bool = True
    ) -> list[str]:
        """List files in local storage.
        
        Args:
            prefix: Optional path prefix to filter by
            recursive: If True, list files in subdirectories
            
        Returns:
            list[str]: List of relative file paths
            
        Raises:
            StorageError: If listing fails
        """
        try:
            if prefix:
                base_path = self._get_full_path(prefix)
            else:
                base_path = self.root_directory
                
            files = []
            pattern = '**/*' if recursive else '*'
            
            for path in base_path.glob(pattern):
                if path.is_file() and not path.name.endswith('.meta'):
                    rel_path = path.relative_to(self.root_directory)
                    files.append(str(rel_path))
                    
            return sorted(files)
            
        except Exception as e:
            raise StorageError(f"Failed to list files: {e}")

    def file_exists(self, object_name: str) -> bool:
        """Check if a file exists in local storage.
        
        Args:
            object_name: Path of the file to check
            
        Returns:
            bool: True if file exists
        """
        try:
            path = self._get_full_path(object_name)
            return path.is_file()
        except Exception:
            return False

    def get_file_metadata(self, object_name: str) -> Dict[str, Any]:
        """Get metadata for a file.
        
        Args:
            object_name: Path of the file
            
        Returns:
            dict: File metadata including size, dates, and custom metadata
            
        Raises:
            StorageFileNotFoundError: If file doesn't exist
            StorageError: If metadata retrieval fails
        """
        try:
            file_path = self._get_full_path(object_name)
            if not file_path.exists():
                raise StorageFileNotFoundError(f"File not found: {object_name}")
                
            stat = file_path.stat()
            metadata = {
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'content_type': mimetypes.guess_type(file_path)[0],
                'metadata': self._load_metadata(file_path)
            }
                    
            return metadata
            
        except StorageFileNotFoundError:
            raise
        except Exception as e:
            raise StorageError(f"Failed to get file metadata: {e}")
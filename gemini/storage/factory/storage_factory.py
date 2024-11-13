# gemini/storage/factory/storage_factory.py

from typing import Dict, Type, Optional
from gemini.storage.interfaces.storage_provider import StorageProvider
from gemini.storage.providers.local_storage import LocalStorageProvider
from gemini.storage.providers.minio_storage import MinioStorageProvider
from gemini.storage.config.storage_config import (
    StorageConfig,
    LocalStorageConfig,
    MinioStorageConfig,
    S3StorageConfig
)
from gemini.storage.exceptions import StorageError, StorageInitializationError

class StorageFactory:
    """Factory for creating storage provider instances.
    
    This class maintains a registry of available storage providers and creates
    instances based on configuration. It ensures providers are properly initialized
    and configured before use.
    """

    # Registry of available storage providers
    _providers: Dict[str, Type[StorageProvider]] = {
        'local': LocalStorageProvider,
        'minio': MinioStorageProvider,
        # Add more providers here as they're implemented
        # 's3': S3StorageProvider,
        # 'azure': AzureStorageProvider,
    }

    # Singleton instance
    _instance: Optional[StorageProvider] = None

    @classmethod
    def register_provider(cls, provider_name: str, provider_class: Type[StorageProvider]) -> None:
        """Register a new storage provider.
        
        Args:
            provider_name: Name to register the provider under
            provider_class: The provider class to register
            
        Raises:
            ValueError: If provider_name is already registered
        """
        if provider_name in cls._providers:
            raise ValueError(f"Provider {provider_name} is already registered")
        cls._providers[provider_name] = provider_class

    @classmethod
    def create_provider(cls, config: StorageConfig) -> StorageProvider:
        """Create a new storage provider instance based on configuration.
        
        Args:
            config: Storage configuration
            
        Returns:
            StorageProvider: Configured storage provider instance
            
        Raises:
            StorageError: If provider creation fails
            ValueError: If provider type is not supported
        """
        provider_class = cls._providers.get(config.provider.lower())
        if not provider_class:
            raise ValueError(f"Unsupported storage provider: {config.provider}")
        
        try:
            provider = provider_class(config)
            provider.initialize()  # Ensure provider is properly initialized
            return provider
        except Exception as e:
            raise StorageInitializationError(f"Failed to create storage provider: {e}")

    @classmethod
    def get_provider(cls, config: Optional[StorageConfig] = None) -> StorageProvider:
        """Get or create a storage provider instance (singleton pattern).
        
        Args:
            config: Optional storage configuration. If not provided, will use
                   environment variables via create_storage_config_from_env()
            
        Returns:
            StorageProvider: Configured storage provider instance
            
        Raises:
            StorageError: If provider creation fails
        """
        if config is None:
            raise NotImplementedError("Environment-based configuration not implemented yet")

        if cls._instance is None:
            if config is None:
                config = create_storage_config_from_env()
            cls._instance = cls.create_provider(config)
        return cls._instance

    @classmethod
    def reset_provider(cls) -> None:
        """Reset the singleton provider instance.
        
        This is useful for testing or when you need to reinitialize the provider.
        """
        cls._instance = None

# Example usage in your FileHandlerMixin:
class FileHandlerMixin:
    """Mixin class for file handling operations."""

    _storage_provider: Optional[StorageProvider] = None

    @classmethod
    def get_storage_provider(cls) -> StorageProvider:
        """Get the storage provider instance."""
        if cls._storage_provider is None:
            cls._storage_provider = StorageFactory.get_provider()
        return cls._storage_provider

    @classmethod
    def _upload_file(cls, object_name: str, data_stream: str) -> str:
        """Upload a file using the configured storage provider.
        
        Args:
            object_name: Destination path/name for the file
            data_stream: Source file or data stream
            
        Returns:
            str: URL of the uploaded file
        """
        provider = cls.get_storage_provider()
        return provider.upload_file(object_name, data_stream)

    @classmethod
    def _download_file(cls, object_name: str, destination_path: str) -> str:
        """Download a file using the configured storage provider.
        
        Args:
            object_name: Source path/name of the file
            destination_path: Where to save the file
            
        Returns:
            str: Path where the file was saved
        """
        provider = cls.get_storage_provider()
        return provider.download_file(object_name, destination_path)

    @classmethod
    def _get_download_url(cls, object_name: str) -> str:
        """Get a download URL for a file.
        
        Args:
            object_name: Path/name of the file
            
        Returns:
            str: Download URL for the file
        """
        provider = cls.get_storage_provider()
        return provider.get_download_url(object_name)
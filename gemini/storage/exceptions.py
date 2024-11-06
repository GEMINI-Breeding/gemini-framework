# gemini/storage/exceptions.py

class StorageError(Exception):
    """Base exception for storage-related errors."""
    pass

class StorageConnectionError(StorageError):
    """Raised when connection to storage service fails."""
    pass

class StorageAuthError(StorageError):
    """Raised when authentication with storage service fails."""
    pass

class StorageFileNotFoundError(StorageError):
    """Raised when a file is not found in storage."""
    pass

class StorageUploadError(StorageError):
    """Raised when file upload fails."""
    pass

class StorageDownloadError(StorageError):
    """Raised when file download fails."""
    pass

class StorageDeleteError(StorageError):
    """Raised when file deletion fails."""
    pass

class StorageInitializationError(StorageError):
    """Raised when storage provider initialization fails."""
    pass

class StorageConfigurationError(StorageError):
    """Raised when storage configuration is invalid."""
    pass
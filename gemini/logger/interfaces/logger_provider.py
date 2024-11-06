# gemini/logger/interfaces/logger_provider.py

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Generator, List, Optional, Union
from enum import Enum

class LogLevel(Enum):
    """Standard log levels."""
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

class LoggerProvider(ABC):
    """Base interface for all logger providers.
    
    This interface defines the contract that all logger providers must implement.
    It provides a standard set of operations for logging, regardless of the 
    underlying system (local files, Redis, etc.).
    """
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the logger provider and create necessary resources.
        
        Returns:
            bool: True if initialization was successful
            
        Raises:
            LoggerInitializationError: If initialization fails
        """
        pass

    @abstractmethod
    def log(
        self,
        level: Union[LogLevel, str],
        message: str,
        extra: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        **kwargs
    ) -> bool:
        """Log a message with the specified level.
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message: The message to log
            extra: Additional fields to include in the log entry
            timestamp: Optional timestamp (defaults to current time)
            **kwargs: Additional keyword arguments for flexibility
            
        Returns:
            bool: True if logging was successful
            
        Raises:
            LoggerWriteError: If writing the log fails
            LoggerConnectionError: If connection fails
        """
        pass

    @abstractmethod
    def debug(self, message: str, **kwargs) -> bool:
        """Log a debug message.
        
        Args:
            message: The message to log
            **kwargs: Additional arguments passed to log()
            
        Returns:
            bool: True if logging was successful
        """
        pass

    @abstractmethod
    def info(self, message: str, **kwargs) -> bool:
        """Log an info message.
        
        Args:
            message: The message to log
            **kwargs: Additional arguments passed to log()
            
        Returns:
            bool: True if logging was successful
        """
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs) -> bool:
        """Log a warning message.
        
        Args:
            message: The message to log
            **kwargs: Additional arguments passed to log()
            
        Returns:
            bool: True if logging was successful
        """
        pass

    @abstractmethod
    def error(self, message: str, **kwargs) -> bool:
        """Log an error message.
        
        Args:
            message: The message to log
            **kwargs: Additional arguments passed to log()
            
        Returns:
            bool: True if logging was successful
        """
        pass

    @abstractmethod
    def critical(self, message: str, **kwargs) -> bool:
        """Log a critical message.
        
        Args:
            message: The message to log
            **kwargs: Additional arguments passed to log()
            
        Returns:
            bool: True if logging was successful
        """
        pass

    @abstractmethod
    def flush(self) -> bool:
        """Flush any buffered log entries.
        
        Returns:
            bool: True if flush was successful
            
        Raises:
            LoggerFlushError: If flush fails
        """
        pass

    @abstractmethod
    def rotate(self) -> bool:
        """Rotate logs if the provider supports it.
        
        Returns:
            bool: True if rotation was successful
            
        Raises:
            LoggerRotationError: If rotation fails
        """
        pass

    @abstractmethod
    def get_logs(
        self,
        level: Optional[Union[LogLevel, str]] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None,
        **filters
    ) -> Generator[Dict[str, Any], None, None]:
        """Retrieve logs matching the specified criteria.
        
        Args:
            level: Filter by log level
            start_time: Filter logs after this time
            end_time: Filter logs before this time
            limit: Maximum number of logs to return
            **filters: Additional filters to apply
            
        Yields:
            Dict[str, Any]: Log entries matching criteria
            
        Raises:
            LoggerReadError: If reading logs fails
            LoggerConnectionError: If connection fails
        """
        pass

    @abstractmethod
    def clear_logs(
        self,
        older_than: Optional[datetime] = None,
        level: Optional[Union[LogLevel, str]] = None
    ) -> bool:
        """Clear logs matching the specified criteria.
        
        Args:
            older_than: Clear logs older than this time
            level: Clear logs of this level only
            
        Returns:
            bool: True if clearing was successful
            
        Raises:
            LoggerWriteError: If clearing logs fails
        """
        pass

from typing import Dict, Type, Optional
from gemini.logger.interfaces.logger_provider import LoggerProvider
from gemini.logger.providers.local_logger import LocalLogger
from gemini.logger.providers.redis_logger import RedisLogger
from gemini.logger.config.logger_config import (
    LoggerConfig,
    LocalLoggerConfig,
    RedisLoggerConfig,
    create_logger_config_from_env
)
from gemini.logger.exceptions import LoggerError, LoggerInitializationError

class LoggerFactory:
    """Factory for creating logger provider instances.
    
    This class maintains a registry of available logger providers and creates
    instances based on configuration. It ensures providers are properly initialized
    and configured before use.

    Key Features:
    - Provider registry with automatic initialization
    - Environment-based configuration
    - Singleton pattern for consistent logging
    - Support for multiple logger types
    - Thread-safe implementation
    """

    # Registry of available logger providers
    _providers: Dict[str, Type[LoggerProvider]] = {
        'local': LocalLogger,
        'redis': RedisLogger,
        # Add more providers here as they're implemented
        # 'cloudwatch': CloudWatchLogger,
        # 'elasticsearch': ElasticsearchLogger,
    }

    # Singleton instance
    _instance: Optional[LoggerProvider] = None

    # Thread lock for thread safety
    _lock = None

    @classmethod
    def register_provider(cls, provider_name: str, provider_class: Type[LoggerProvider]) -> None:
        """Register a new logger provider.
        
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
    def create_provider(cls, config: LoggerConfig) -> LoggerProvider:
        """Create a new logger provider instance based on configuration.
        
        Args:
            config: Logger configuration
            
        Returns:
            LoggerProvider: Configured logger provider instance
            
        Raises:
            LoggerError: If provider creation fails
            ValueError: If provider type is not supported
        """
        provider_class = cls._providers.get(config.provider.lower())
        if not provider_class:
            raise ValueError(f"Unsupported logger provider: {config.provider}")
        
        try:
            provider = provider_class(config)
            provider.initialize()  # Ensure provider is properly initialized
            return provider
        except Exception as e:
            raise LoggerInitializationError(f"Failed to create logger provider: {e}")

    @classmethod
    def get_provider(cls, config: Optional[LoggerConfig] = None) -> LoggerProvider:
        """Get or create a logger provider instance (singleton pattern).
        
        This method is thread-safe and ensures only one logger instance exists.
        
        Args:
            config: Optional logger configuration. If not provided, will use
                   environment variables via create_logger_config_from_env()
            
        Returns:
            LoggerProvider: Configured logger provider instance
            
        Raises:
            LoggerError: If provider creation fails
        """
        if cls._instance is None:
            # Import threading here to avoid circular imports
            import threading
            if cls._lock is None:
                cls._lock = threading.Lock()
            
            with cls._lock:
                # Double-check pattern for thread safety
                if cls._instance is None:
                    if config is None:
                        config = create_logger_config_from_env()
                    cls._instance = cls.create_provider(config)
        
        return cls._instance

    @classmethod
    def reset_provider(cls) -> None:
        """Reset the singleton provider instance.
        
        This is useful for testing or when you need to reinitialize the provider.
        Thread-safe implementation.
        """
        if cls._lock is None:
            import threading
            cls._lock = threading.Lock()
            
        with cls._lock:
            if cls._instance:
                try:
                    cls._instance.flush()  # Ensure any buffered logs are written
                except Exception:
                    pass  # Ignore flush errors during reset
            cls._instance = None
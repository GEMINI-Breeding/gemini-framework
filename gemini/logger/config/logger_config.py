# gemini/logger/config/logger_config.py

from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime
from gemini.logger.exceptions import LoggerConfigurationError

class LoggerConfig(BaseModel):
    """Base configuration for logger providers."""
    
    provider: str = Field(
        ...,  # Required field
        description="Name of the logger provider (local, redis)"
    )
    level: str = Field(
        "INFO",
        description="Default log level"
    )
    format: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    buffer_size: Optional[int] = Field(
        None,
        description="Size of the log buffer (if buffering is used)"
    )
    extra_fields: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional fields to include in all log entries"
    )

    model_config = {
        "extra": "forbid"  # Prevent additional attributes
    }

class LocalLoggerConfig(LoggerConfig):
    """Configuration for local file logger."""
    
    provider: str = Field(
        "local",
        frozen=True,
        description="Provider name, must be 'local'"
    )
    log_dir: Path = Field(
        ...,
        description="Directory for log files"
    )
    filename_template: str = Field(
        "{name}_{date}.log",
        description="Template for log filenames"
    )
    max_size_mb: Optional[int] = Field(
        None,
        ge=1,
        description="Maximum size of each log file in MB"
    )
    backup_count: int = Field(
        5,
        ge=0,
        description="Number of backup files to keep"
    )
    rotation_time: Optional[str] = Field(
        None,
        description="Time-based rotation (midnight, h1, h12)"
    )
    encoding: str = Field(
        "utf-8",
        description="File encoding"
    )
    
    @field_validator('log_dir')
    @classmethod
    def validate_log_dir(cls, v: Path) -> Path:
        """Validate log directory path."""
        try:
            path = Path(v)
            return path.resolve()
        except Exception as e:
            raise LoggerConfigurationError(f"Invalid log directory path: {e}")
            
    @model_validator(mode='after')
    def validate_rotation_settings(self) -> 'LocalLoggerConfig':
        """Validate that rotation settings are consistent."""
        if self.rotation_time and self.max_size_mb:
            raise LoggerConfigurationError(
                "Cannot specify both size-based and time-based rotation"
            )
        return self

class RedisLoggerConfig(LoggerConfig):
    """Configuration for Redis logger."""
    
    provider: str = Field(
        "redis",
        frozen=True,
        description="Provider name, must be 'redis'"
    )
    host: str = Field(
        ...,
        description="Redis server hostname"
    )
    port: int = Field(
        6379,
        description="Redis server port"
    )
    db: int = Field(
        0,
        ge=0,
        description="Redis database number"
    )
    password: Optional[str] = Field(
        None,
        description="Redis password"
    )
    key_prefix: str = Field(
        "logs:",
        description="Prefix for Redis keys"
    )
    max_entries: Optional[int] = Field(
        None,
        gt=0,
        description="Maximum number of log entries to keep"
    )
    ttl_days: Optional[int] = Field(
        None,
        gt=0,
        description="Time to live for log entries in days"
    )
    use_ssl: bool = Field(
        False,
        description="Use SSL for Redis connection"
    )
    
    @field_validator('host')
    @classmethod
    def validate_host(cls, v: str) -> str:
        """Validate Redis host."""
        if not v:
            raise LoggerConfigurationError("Redis host cannot be empty")
        return v
    
    @model_validator(mode='after')
    def validate_retention_settings(self) -> 'RedisLoggerConfig':
        """Validate retention settings."""
        if self.max_entries and self.ttl_days:
            raise LoggerConfigurationError(
                "Cannot specify both max_entries and ttl_days for retention"
            )
        return self

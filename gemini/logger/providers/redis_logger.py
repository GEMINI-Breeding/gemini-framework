# gemini/logger/providers/redis_logger.py

import json
import redis
from datetime import datetime, timedelta
from typing import Any, Dict, Generator, Optional, Union
from gemini.logger.interfaces.logger_provider import LoggerProvider, LogLevel
from gemini.logger.config.logger_config import RedisLoggerConfig
from gemini.logger.exceptions import (
    LoggerError,
    LoggerInitializationError,
    LoggerWriteError,
    LoggerReadError,
    LoggerConnectionError,
    LoggerAuthError
)

class RedisLogger(LoggerProvider):
    """Redis-based logger implementation."""

    def __init__(self, config: RedisLoggerConfig):
        """Initialize Redis logger with configuration.
        
        Args:
            config: Configuration for Redis logging
            
        Raises:
            LoggerInitializationError: If initialization fails
        """
        self.config = config
        self.redis_client = None
        self._buffer = []

    def initialize(self) -> bool:
        """Initialize Redis connection and verify configuration.
        
        Returns:
            bool: True if initialization successful
            
        Raises:
            LoggerInitializationError: If initialization fails
            LoggerConnectionError: If Redis connection fails
            LoggerAuthError: If Redis authentication fails
        """
        try:
            # Initialize Redis connection
            self.redis_client = redis.Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                ssl=self.config.use_ssl,
                decode_responses=True  # Always decode responses to str
            )
            
            # Test connection
            self.redis_client.ping()
            
            # Create a sorted set for log indexing if it doesn't exist
            self._ensure_index_exists()
            
            return True
            
        except redis.AuthenticationError as e:
            raise LoggerAuthError(f"Redis authentication failed: {e}")
        except redis.ConnectionError as e:
            raise LoggerConnectionError(f"Failed to connect to Redis: {e}")
        except Exception as e:
            raise LoggerInitializationError(f"Failed to initialize Redis logger: {e}")

    def _ensure_index_exists(self):
        """Ensure the log index exists in Redis."""
        index_key = f"{self.config.key_prefix}index"
        if not self.redis_client.exists(index_key):
            self.redis_client.zadd(index_key, {'init': 0})

    def _generate_log_key(self, timestamp: datetime) -> str:
        """Generate a Redis key for a log entry.
        
        Args:
            timestamp: Timestamp for the log entry
            
        Returns:
            str: Redis key for the log entry
        """
        return f"{self.config.key_prefix}{timestamp.isoformat()}"

    def _format_extra(self, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format extra fields including configured extra fields.
        
        Args:
            extra: Additional fields to include
            
        Returns:
            Dict[str, Any]: Combined extra fields
        """
        formatted = self.config.extra_fields or {}
        if extra:
            formatted.update(extra)
        return formatted

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
            level: Log level
            message: Message to log
            extra: Additional fields
            timestamp: Optional timestamp
            **kwargs: Additional arguments
            
        Returns:
            bool: True if successful
            
        Raises:
            LoggerWriteError: If writing fails
            LoggerConnectionError: If connection fails
        """
        try:
            # Convert LogLevel enum to string if needed
            if isinstance(level, LogLevel):
                level = level.name

            # Create timestamp if not provided
            timestamp = timestamp or datetime.now()

            # Format the log entry
            entry = {
                'message': message,
                'timestamp': timestamp.isoformat(),
                'level': level,
                **self._format_extra(extra),
                **kwargs
            }

            # Buffer if configured
            if self.config.buffer_size:
                self._buffer.append(entry)
                if len(self._buffer) >= self.config.buffer_size:
                    self.flush()
                return True

            # Write directly if no buffering
            return self._write_log_entry(entry)
            
        except redis.ConnectionError as e:
            raise LoggerConnectionError(f"Redis connection failed while writing log: {e}")
        except Exception as e:
            raise LoggerWriteError(f"Failed to write log: {e}")

    def _write_log_entry(self, entry: Dict[str, Any]) -> bool:
        """Write a single log entry to Redis.
        
        Args:
            entry: The log entry to write
            
        Returns:
            bool: True if successful
        """
        # Start a Redis pipeline for atomic operations
        pipe = self.redis_client.pipeline()

        try:
            # Generate key and serialize entry
            entry_key = self._generate_log_key(datetime.fromisoformat(entry['timestamp']))
            entry_data = json.dumps(entry)

            # Add to log store
            pipe.set(entry_key, entry_data)

            # Add to index
            pipe.zadd(
                f"{self.config.key_prefix}index",
                {entry_key: datetime.fromisoformat(entry['timestamp']).timestamp()}
            )

            # Set TTL if configured
            if self.config.ttl_days:
                pipe.expire(entry_key, timedelta(days=self.config.ttl_days))

            # Enforce max entries if configured
            if self.config.max_entries:
                index_key = f"{self.config.key_prefix}index"
                count = self.redis_client.zcard(index_key)
                if count > self.config.max_entries:
                    # Remove oldest entries
                    to_remove = count - self.config.max_entries
                    oldest_keys = self.redis_client.zrange(index_key, 0, to_remove - 1)
                    if oldest_keys:
                        pipe.delete(*oldest_keys)
                        pipe.zremrangebyrank(index_key, 0, to_remove - 1)

            # Execute all commands
            pipe.execute()
            return True

        except Exception:
            pipe.reset()
            raise

    def debug(self, message: str, **kwargs) -> bool:
        """Log a debug message."""
        return self.log(LogLevel.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs) -> bool:
        """Log an info message."""
        return self.log(LogLevel.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs) -> bool:
        """Log a warning message."""
        return self.log(LogLevel.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs) -> bool:
        """Log an error message."""
        return self.log(LogLevel.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs) -> bool:
        """Log a critical message."""
        return self.log(LogLevel.CRITICAL, message, **kwargs)

    def flush(self) -> bool:
        """Flush buffered log entries.
        
        Returns:
            bool: True if successful
            
        Raises:
            LoggerWriteError: If flush fails
        """
        if not self._buffer:
            return True

        try:
            pipe = self.redis_client.pipeline()
            
            for entry in self._buffer:
                entry_key = self._generate_log_key(datetime.fromisoformat(entry['timestamp']))
                entry_data = json.dumps(entry)
                
                pipe.set(entry_key, entry_data)
                pipe.zadd(
                    f"{self.config.key_prefix}index",
                    {entry_key: datetime.fromisoformat(entry['timestamp']).timestamp()}
                )
                
                if self.config.ttl_days:
                    pipe.expire(entry_key, timedelta(days=self.config.ttl_days))
            
            pipe.execute()
            self._buffer.clear()
            return True
            
        except redis.ConnectionError as e:
            raise LoggerConnectionError(f"Redis connection failed while flushing: {e}")
        except Exception as e:
            raise LoggerWriteError(f"Failed to flush logs: {e}")

    def rotate(self) -> bool:
        """Rotation is handled automatically by Redis TTL.
        
        Returns:
            bool: Always True as Redis handles rotation
        """
        return True

    def get_logs(
        self,
        level: Optional[Union[LogLevel, str]] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None,
        **filters
    ) -> Generator[Dict[str, Any], None, None]:
        """Retrieve logs matching criteria.
        
        Args:
            level: Filter by log level
            start_time: Filter logs after this time
            end_time: Filter logs before this time
            limit: Maximum number of logs to return
            **filters: Additional filters
            
        Yields:
            Dict[str, Any]: Matching log entries
            
        Raises:
            LoggerReadError: If reading fails
            LoggerConnectionError: If connection fails
        """
        try:
            # Convert level to string if it's an enum
            if isinstance(level, LogLevel):
                level = level.name

            # Convert times to timestamps for Redis
            min_score = start_time.timestamp() if start_time else '-inf'
            max_score = end_time.timestamp() if end_time else '+inf'

            # Get keys in time range
            index_key = f"{self.config.key_prefix}index"
            log_keys = self.redis_client.zrangebyscore(
                index_key,
                min_score,
                max_score,
                start=0,
                num=limit
            )

            if not log_keys:
                return

            # Get log entries
            pipe = self.redis_client.pipeline()
            for key in log_keys:
                pipe.get(key)
            entries = pipe.execute()

            # Filter and yield entries
            count = 0
            for entry_data in entries:
                if not entry_data:
                    continue
                    
                try:
                    entry = json.loads(entry_data)
                    
                    # Apply filters
                    if level and entry.get('level') != level:
                        continue
                        
                    # Apply additional filters
                    skip = False
                    for key, value in filters.items():
                        if entry.get(key) != value:
                            skip = True
                            break
                    if skip:
                        continue
                        
                    yield entry
                    
                    count += 1
                    if limit and count >= limit:
                        return
                        
                except json.JSONDecodeError:
                    continue  # Skip malformed entries
                    
        except redis.ConnectionError as e:
            raise LoggerConnectionError(f"Redis connection failed while reading logs: {e}")
        except Exception as e:
            raise LoggerReadError(f"Failed to read logs: {e}")

    def clear_logs(
        self,
        older_than: Optional[datetime] = None,
        level: Optional[Union[LogLevel, str]] = None
    ) -> bool:
        """Clear logs matching criteria.
        
        Args:
            older_than: Clear logs older than this time
            level: Clear logs of this level only
            
        Returns:
            bool: True if successful
        """
        try:
            pipe = self.redis_client.pipeline()
            index_key = f"{self.config.key_prefix}index"

            if older_than:
                # Get keys older than specified time
                max_score = older_than.timestamp()
                old_keys = self.redis_client.zrangebyscore(index_key, '-inf', max_score)
                
                if old_keys:
                    # Delete log entries and index entries
                    pipe.delete(*old_keys)
                    pipe.zremrangebyscore(index_key, '-inf', max_score)

            elif level:
                # Get all keys and filter by level
                all_keys = self.redis_client.zrange(index_key, 0, -1)
                keys_to_delete = []
                
                for key in all_keys:
                    entry_data = self.redis_client.get(key)
                    if entry_data:
                        try:
                            entry = json.loads(entry_data)
                            if entry.get('level') == level:
                                keys_to_delete.append(key)
                        except json.JSONDecodeError:
                            continue
                
                if keys_to_delete:
                    pipe.delete(*keys_to_delete)
                    pipe.zrem(index_key, *keys_to_delete)

            pipe.execute()
            return True
            
        except redis.ConnectionError as e:
            raise LoggerConnectionError(f"Redis connection failed while clearing logs: {e}")
        except Exception as e:
            raise LoggerWriteError(f"Failed to clear logs: {e}")
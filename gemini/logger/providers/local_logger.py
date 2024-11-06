# gemini/logger/providers/local_logger.py

import os
import json
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generator, Optional, Union
from gemini.logger.interfaces.logger_provider import LoggerProvider, LogLevel
from gemini.logger.config.logger_config import LocalLoggerConfig
from gemini.logger.exceptions import (
    LoggerError,
    LoggerInitializationError,
    LoggerWriteError,
    LoggerReadError,
    LoggerRotationError
)

class LocalLogger(LoggerProvider):
    """Local file-based logger implementation."""

    def __init__(self, config: LocalLoggerConfig):
        """Initialize the local logger with configuration.
        
        Args:
            config: Configuration for local logging
            
        Raises:
            LoggerInitializationError: If initialization fails
        """
        self.config = config
        self.logger = None
        self._buffer = []
        
    def initialize(self) -> bool:
        """Initialize the logger and create necessary directories.
        
        Returns:
            bool: True if initialization successful
            
        Raises:
            LoggerInitializationError: If initialization fails
        """
        try:
            # Create log directory if it doesn't exist
            os.makedirs(self.config.log_dir, exist_ok=True)

            # Create the logger
            self.logger = logging.getLogger('gemini')
            self.logger.setLevel(getattr(logging, self.config.level.upper()))

            # Determine the log file path
            log_file = self.config.log_dir / self.config.filename_template.format(
                name='gemini',
                date=datetime.now().strftime('%Y%m%d')
            )

            # Configure the appropriate handler based on rotation settings
            if self.config.rotation_time:
                handler = TimedRotatingFileHandler(
                    filename=str(log_file),
                    when=self.config.rotation_time,
                    backupCount=self.config.backup_count,
                    encoding=self.config.encoding
                )
            elif self.config.max_size_mb:
                handler = RotatingFileHandler(
                    filename=str(log_file),
                    maxBytes=self.config.max_size_mb * 1024 * 1024,
                    backupCount=self.config.backup_count,
                    encoding=self.config.encoding
                )
            else:
                handler = logging.FileHandler(
                    filename=str(log_file),
                    encoding=self.config.encoding
                )

            # Create formatter and add it to the handler
            formatter = logging.Formatter(self.config.format)
            handler.setFormatter(formatter)
            
            # Add the handler to the logger
            self.logger.addHandler(handler)
            
            return True
            
        except Exception as e:
            raise LoggerInitializationError(f"Failed to initialize local logger: {e}")

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
        """
        try:
            # Convert LogLevel enum to string if needed
            if isinstance(level, LogLevel):
                level = level.name

            # Format the log entry
            entry = {
                'message': message,
                'timestamp': timestamp or datetime.now().isoformat(),
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
            log_func = getattr(self.logger, level.lower())
            log_func(message, extra=self._format_extra(extra))
            return True
            
        except Exception as e:
            raise LoggerWriteError(f"Failed to write log: {e}")

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
        """
        if not self._buffer:
            return True

        try:
            for entry in self._buffer:
                level = entry.pop('level')
                message = entry.pop('message')
                log_func = getattr(self.logger, level.lower())
                log_func(message, extra=entry)
            
            self._buffer.clear()
            return True
            
        except Exception as e:
            raise LoggerWriteError(f"Failed to flush logs: {e}")

    def rotate(self) -> bool:
        """Force log rotation if supported.
        
        Returns:
            bool: True if successful
            
        Raises:
            LoggerRotationError: If rotation fails
        """
        try:
            for handler in self.logger.handlers:
                if isinstance(handler, (RotatingFileHandler, TimedRotatingFileHandler)):
                    handler.doRollover()
            return True
        except Exception as e:
            raise LoggerRotationError(f"Failed to rotate logs: {e}")

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
        """
        try:
            # Convert level to string if it's an enum
            if isinstance(level, LogLevel):
                level = level.name

            count = 0
            log_files = sorted(Path(self.config.log_dir).glob('*.log'))
            
            for log_file in log_files:
                with open(log_file, 'r', encoding=self.config.encoding) as f:
                    for line in f:
                        try:
                            entry = json.loads(line)
                            
                            # Apply filters
                            if level and entry.get('level') != level:
                                continue
                                
                            if start_time:
                                log_time = datetime.fromisoformat(entry['timestamp'])
                                if log_time < start_time:
                                    continue
                                    
                            if end_time:
                                log_time = datetime.fromisoformat(entry['timestamp'])
                                if log_time > end_time:
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
                            continue  # Skip malformed lines
                            
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
            if older_than:
                cutoff = older_than.strftime('%Y%m%d')
                for log_file in Path(self.config.log_dir).glob('*.log'):
                    if log_file.stem[-8:] < cutoff:
                        log_file.unlink()
            return True
        except Exception as e:
            raise LoggerWriteError(f"Failed to clear logs: {e}")
# gemini/logger/exceptions.py

class LoggerError(Exception):
    """Base exception for logger-related errors."""
    pass

class LoggerConnectionError(LoggerError):
    """Raised when connection to logging service fails."""
    pass

class LoggerAuthError(LoggerError):
    """Raised when authentication with logging service fails."""
    pass

class LoggerInitializationError(LoggerError):
    """Raised when logger initialization fails."""
    pass

class LoggerConfigurationError(LoggerError):
    """Raised when logger configuration is invalid."""
    pass

class LoggerWriteError(LoggerError):
    """Raised when writing to log fails."""
    pass

class LoggerReadError(LoggerError):
    """Raised when reading from log fails."""
    pass

class LoggerFlushError(LoggerError):
    """Raised when flushing logs fails."""
    pass

class LoggerRotationError(LoggerError):
    """Raised when log rotation fails."""
    pass
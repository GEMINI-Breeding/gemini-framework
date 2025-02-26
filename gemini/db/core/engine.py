# gemini/server/database/core/engine.py
import asyncio
from datetime import datetime
from typing import Generator, Optional, Any
from contextlib import contextmanager, asynccontextmanager
import logging
from sqlalchemy import create_engine, event, exc
from sqlalchemy.sql import text
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from gemini.db.config import DatabaseConfig

logger = logging.getLogger(__name__)

class DatabaseEngine:
    """
    Database engine manager with connection pooling, health checks, and monitoring.
    
    Features:
    - Connection pooling with configurable settings
    - Health checks and connection verification
    - Query execution monitoring and logging
    - Support for both sync and async operations
    - Automatic retry on connection failures
    - Connection pool monitoring
    """

    def __init__(self, config: Optional[DatabaseConfig] = None, engine: Optional[Engine] = None, async_engine: Optional[Engine] = None):
        """Initialize database engine with configuration."""
        
        if not config:
            raise ValueError("Database configuration is required")
        
        self.config = config 
        self._engine: Optional[Engine] = engine
        self._async_engine = async_engine
        self._session_factory = None
        self._async_session_factory = None
        
        


        # Initialize engines if not provided
        if not self._engine:
            self.setup_engine()
        if not self._async_engine:
            self.setup_async_engine()
        
        # Set up event listeners
        self._setup_engine_events()

    def setup_engine(self) -> None:
        """Set up the SQLAlchemy engine with optimal settings."""
        if self._engine is not None:
            return

        self._engine = create_engine(
            self.config.database_url,
            poolclass=self.config.pool_class,
            pool_size=self.config.pool_size,
            max_overflow=self.config.max_overflow,
            pool_timeout=self.config.pool_timeout,
            pool_recycle=self.config.pool_recycle,
            pool_pre_ping=True,  # Enable connection health checks
            echo=self.config.echo_sql,
            echo_pool=self.config.echo_pool,
            execution_options={
                "isolation_level": self.config.isolation_level
            }
        )

        # Create session factory
        self._session_factory = sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            future=True,
            expire_on_commit=False
        )

    def setup_async_engine(self) -> None:
        """Set up the async SQLAlchemy engine."""
        if self._async_engine is not None:
            return
        
        # Add asyncpg dialect to the database URL
        self.config.database_url = self.config.database_url.replace("postgresql", "postgresql+asyncpg")

        self._async_engine = create_async_engine(
            self.config.database_url,
            poolclass=self.config.async_pool_class,
            pool_size=self.config.pool_size,
            max_overflow=self.config.max_overflow,
            pool_timeout=self.config.pool_timeout,
            pool_recycle=self.config.pool_recycle,
            pool_pre_ping=True,
            echo=self.config.echo_sql,
            echo_pool=self.config.echo_pool
        )

        # Create async session factory
        self._async_session_factory = async_sessionmaker(
            bind=self._async_engine,
            autocommit=False,
            autoflush=True,
            expire_on_commit=False
        )

    def _setup_engine_events(self) -> None:
        """Set up SQLAlchemy event listeners for monitoring."""
        
        @event.listens_for(self._engine, 'before_cursor_execute')
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            conn.info.setdefault('query_start_time', []).append(datetime.now())
            logger.debug("Executing query: %s", statement)

        @event.listens_for(self._engine, 'after_cursor_execute')
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            total = datetime.now() - conn.info['query_start_time'].pop()
            logger.debug("Query execution time: %s", total)

        @event.listens_for(self._engine, 'engine_connect')
        def engine_connect(conn, branch):
            logger.debug("New database connection established")

        @event.listens_for(self._engine.pool, 'close')
        def connection_close(dbapi_connection, connection_record):
            logger.debug("Database connection closed")

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get a database session with automatic cleanup.
        
        Yields:
            Session: Database session
            
        Example:
            with engine.get_session() as session:
                result = session.query(Model).all()
        """
        session = self._session_factory()
        try:
            yield session
            session.flush()
            session.commit()
        except Exception as e:
            session.rollback()
            # logger.exception("Database session error: %s", str(e))
            raise
        finally:
            session.close()

    @asynccontextmanager
    async def get_async_session(self) -> Any:
        """Get an async database session with automatic cleanup.
        
        Yields:
            AsyncSession: Async database session
            
        Example:
            async with engine.get_async_session() as session:
                result = await session.execute(select(Model))
        """
        session = self._async_session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.exception("Database session error: %s", str(e))
            raise
        finally:
            await session.close()

    def check_health(self) -> bool:
        """Check database connection health.
        
        Returns:
            bool: True if database is healthy
            
        Raises:
            DatabaseConnectionError: If connection check fails
        """
        try:
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except exc.DBAPIError as e:
            logger.error("Database health check failed: %s", str(e))
            return False

    async def check_health_async(self) -> bool:
        """Check async database connection health.
        
        Returns:
            bool: True if database is healthy
        """
        try:
            async with self._async_engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except exc.DBAPIError as e:
            logger.error("Async database health check failed: %s", str(e))
            return False

    def get_pool_status(self) -> dict:
        """Get current connection pool status.
        
        Returns:
            dict: Pool statistics
        """
        return {
            "size": self._engine.pool.size(),
            "checkedin": self._engine.pool.checkedin(),
            "checkedout": self._engine.pool.checkedout(),
            "overflow": self._engine.pool.overflow(),
            "checkedout_overflow": self._engine.pool.overflow()
        }

    def dispose(self) -> None:
        """Dispose of the engine and connection pool."""
        if self._engine:
            self._engine.dispose()
        if self._async_engine:
            asyncio.run(self._async_engine.dispose())
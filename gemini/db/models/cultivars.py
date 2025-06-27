"""
SQLAlchemy model for Cultivar entities in the GEMINI database.
"""

from sqlalchemy import JSON, String, TIMESTAMP, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB

from gemini.db.core.base import BaseModel

from datetime import datetime
import uuid


class CultivarModel(BaseModel):
    """
    Represents a cultivar in the GEMINI database.

    Attributes:
        id (uuid.UUID): Unique identifier for the cultivar.
        cultivar_accession (str): The accession identifier for the cultivar.
        cultivar_population (str): The population name of the cultivar.
        cultivar_info (dict): Additional JSONB data for the cultivar.
        created_at (datetime): Timestamp when the record was created.
        updated_at (datetime): Timestamp when the record was last updated.
    """
    __tablename__ = "cultivars"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    cultivar_accession: Mapped[str] = mapped_column(String(255), nullable=False)
    cultivar_population: Mapped[str] = mapped_column(String(255), nullable=False)
    cultivar_info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        UniqueConstraint('cultivar_accession', 'cultivar_population'),
        Index('idx_cultivars_info', 'cultivar_info', postgresql_using='GIN')
    )

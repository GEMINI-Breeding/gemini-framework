from sqlalchemy import JSON, String, TIMESTAMP, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID

from gemini.server.database.models.base_model import BaseModel

from datetime import datetime
import uuid


class CultivarModel(BaseModel):
    __tablename__ = "cultivars"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    cultivar_accession: Mapped[str] = mapped_column(String(255), nullable=False)
    cultivar_population: Mapped[str] = mapped_column(String(255), nullable=False)
    cultivar_info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        UniqueConstraint('cultivar_accession', 'cultivar_population'),
        Index('idx_cultivars_info', 'cultivar_info', postgresql_using='GIN')
    )

from sqlalchemy import (
    JSON,
    String,
    TIMESTAMP,
    UniqueConstraint,
    Index,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB

from gemini.db.core.base import BaseModel

from datetime import datetime
import uuid



class TraitModel(BaseModel):
    __tablename__ = "traits"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    trait_name: Mapped[str] = mapped_column(String(255), nullable=False)
    trait_units: Mapped[str] = mapped_column(String(255), default='units')
    trait_level_id: Mapped[int] = mapped_column(Integer, ForeignKey("gemini.trait_levels.id"), default=0)
    trait_metrics: Mapped[dict] = mapped_column(JSONB, default={})
    trait_info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    __table_args__ = (
        UniqueConstraint('trait_name'),
        Index('idx_traits_info', 'trait_info', postgresql_using='GIN')
    )

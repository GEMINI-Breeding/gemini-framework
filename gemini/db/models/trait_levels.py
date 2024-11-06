from sqlalchemy import JSON, String, TIMESTAMP, UniqueConstraint, Index, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID

from gemini.db.core.base import BaseModel

from datetime import datetime
import uuid


class TraitLevelModel(BaseModel):
    __tablename__ = "trait_levels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trait_level_name: Mapped[str] = mapped_column(String(255), nullable=False)
    trait_level_info: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)

    __table_args__ = (
        UniqueConstraint("trait_level_name", name="trait_level_unique"),
        Index("idx_trait_levels_info", "trait_level_info", postgresql_using="GIN"),
    )


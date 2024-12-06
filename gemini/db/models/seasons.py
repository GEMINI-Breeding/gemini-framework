from sqlalchemy import JSON, String, TIMESTAMP, UniqueConstraint, Index, ForeignKey, CheckConstraint, DATE
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB

from gemini.db.core.base import BaseModel

from datetime import datetime, date
import uuid


class SeasonModel(BaseModel):
    __tablename__ = "seasons"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('gemini.experiments.id'))
    season_name: Mapped[str] = mapped_column(String(255), nullable=False)
    season_info: Mapped[dict] = mapped_column(JSONB, default={})
    season_start_date: Mapped[date] = mapped_column(DATE, nullable=False, default=datetime.now)
    season_end_date: Mapped[date] = mapped_column(DATE)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)

    __table_args__ = (
        UniqueConstraint('experiment_id', 'season_name'),
        CheckConstraint('season_start_date <= season_end_date'),
        CheckConstraint('season_end_date >= season_start_date'),
        Index('idx_seasons_info', 'season_info', postgresql_using='GIN')
    )

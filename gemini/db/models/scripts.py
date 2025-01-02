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
from sqlalchemy.dialects.postgresql import UUID

from gemini.db.core.base import BaseModel

from datetime import datetime
import uuid

class ScriptModel(BaseModel):
    __tablename__ = "scripts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    script_name: Mapped[str] = mapped_column(String(255))
    script_url: Mapped[str] = mapped_column(String(255))
    script_extension: Mapped[str] = mapped_column(String(255))
    script_info: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        UniqueConstraint('script_name', 'script_url'),
        Index('idx_scripts_info', 'script_info', postgresql_using='GIN')
    )

    script_runs = relationship("ScriptRunModel", lazy="subquery", viewonly=True)
    datasets = relationship("DatasetModel", secondary="gemini.script_datasets", lazy="subquery", viewonly=True)

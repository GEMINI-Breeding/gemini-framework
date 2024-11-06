from sqlalchemy import (
    JSON,
    String,
    UniqueConstraint,
    Index,
    Integer,
    Boolean,
    ForeignKey,
    TIMESTAMP,
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from gemini.db.core.base import BaseModel

import uuid
from datetime import datetime


class ScriptRunModel(BaseModel):
    __tablename__ = "script_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    script_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.scripts.id", ondelete="CASCADE"))
    script_run_info: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)

    __table_args__ = (
        UniqueConstraint("script_id", "script_run_info"),
        Index("idx_script_runs_info", "script_run_info", postgresql_using="GIN"),
    )


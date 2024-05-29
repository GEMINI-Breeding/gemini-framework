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
from gemini.models.base_model import BaseModel

import uuid


class ScriptRunModel(BaseModel):
    __tablename__ = "script_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    script_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.scripts.id", ondelete="CASCADE"))
    script_run_info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        UniqueConstraint("script_id", "script_run_info"),
        Index("idx_script_runs_info", "script_run_info", postgresql_using="GIN"),
    )


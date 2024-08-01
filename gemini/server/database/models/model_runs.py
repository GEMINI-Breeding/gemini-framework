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
from sqlalchemy.dialects.postgresql import UUID, JSONB
from gemini.server.database.models.base_model import BaseModel

import uuid


class ModelRunModel(BaseModel):

    __tablename__ = "model_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.models.id", ondelete="CASCADE"))
    model_run_info: Mapped[dict] = mapped_column(JSONB, default={})

    __table_args__ = (
        UniqueConstraint("model_id", "model_run_info"),
        Index("idx_model_runs_info", "model_run_info", postgresql_using="GIN"),
    )


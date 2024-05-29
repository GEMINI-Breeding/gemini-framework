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


class ProcedureRunModel(BaseModel):

    __tablename__ = "procedure_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    procedure_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.procedures.id", ondelete="CASCADE"))
    procedure_run_info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        UniqueConstraint("procedure_id", "procedure_run_info"),
        Index("idx_procedure_runs_info", "procedure_run_info", postgresql_using="GIN"),
    )


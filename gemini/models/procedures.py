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

from gemini.models.base_model import BaseModel

from datetime import datetime
import uuid


class ProcedureModel(BaseModel):
    __tablename__ = "procedures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    procedure_name: Mapped[str] = mapped_column(String(255))
    procedure_info: Mapped[dict] = mapped_column(JSON, default={})
    
    __table_args__ = (
        UniqueConstraint("procedure_name"),
        Index("idx_procedures_info", "procedure_info", postgresql_using="GIN"),
    )

    procedure_runs = relationship("ProcedureRunModel")
    datasets = relationship("DatasetModel", secondary="gemini.procedure_datasets")


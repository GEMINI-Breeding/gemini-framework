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


class ProcedureModel(BaseModel):
    __tablename__ = "procedures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    procedure_name: Mapped[str] = mapped_column(String(255))
    procedure_info: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    __table_args__ = (
        UniqueConstraint("procedure_name"),
        Index("idx_procedures_info", "procedure_info", postgresql_using="GIN"),
    )

    procedure_runs = relationship("ProcedureRunModel", lazy="selectin", cascade="save-update, merge, delete")
    datasets = relationship("DatasetModel", secondary="gemini.procedure_datasets", lazy="selectin", cascade="save-update, merge, delete")

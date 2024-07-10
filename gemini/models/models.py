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


class ModelModel(BaseModel):
    __tablename__ = "models"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    model_name: Mapped[str] = mapped_column(String(255))
    model_url: Mapped[str] = mapped_column(String(255))
    model_info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        UniqueConstraint("model_name", "model_url"),
        Index("idx_models_info", "model_info", postgresql_using="GIN"),
    )

    model_runs = relationship("ModelRunModel")
    datasets = relationship("DatasetModel", secondary="gemini.model_datasets")


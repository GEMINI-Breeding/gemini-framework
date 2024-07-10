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

from datetime import datetime, date
import uuid


class DatasetModel(BaseModel):

    __tablename__ = "datasets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    collection_date: Mapped[date] = mapped_column(TIMESTAMP, default=datetime.now)
    dataset_name: Mapped[str] = mapped_column(String(255))
    dataset_info: Mapped[dict] = mapped_column(JSON, default={})
    dataset_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("gemini.dataset_types.id"), default=0)

    __table_args__ = (
        UniqueConstraint("dataset_name"),
        Index("idx_datasets_info", "dataset_info", postgresql_using="GIN"),
    )

    dataset_type = relationship("DatasetTypeModel")


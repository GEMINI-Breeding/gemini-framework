from sqlalchemy import (
    JSON,
    String,
    TIMESTAMP,
    UniqueConstraint,
    Index,
    Integer
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from gemini.db.core.base import BaseModel
from datetime import datetime

class DatasetTypeModel(BaseModel):
    __tablename__ = "dataset_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dataset_type_name: Mapped[str] = mapped_column(String(255), nullable=False)
    dataset_type_info: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)

    __table_args__ = (
        UniqueConstraint("dataset_type_name"),
        Index("idx_dataset_types_info", "dataset_type_info", postgresql_using="GIN"),
    )
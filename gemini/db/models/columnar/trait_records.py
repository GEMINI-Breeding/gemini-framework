from sqlalchemy.orm import relationship, mapped_column, Mapped, Relationship
from sqlalchemy import (
    UUID,
    REAL,
    JSON,
    String,
    Integer,
    UniqueConstraint,
    Index,
    ForeignKey,
    TIMESTAMP,
    DATE,
)
from sqlalchemy.dialects.postgresql import JSONB
from gemini.db.core.base import ColumnarBaseModel
import uuid
from datetime import datetime, date


class TraitRecordModel(ColumnarBaseModel):

    __tablename__ = "trait_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    collection_date: Mapped[date] = mapped_column(DATE, nullable=False)
    dataset_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    dataset_name: Mapped[str] = mapped_column(String(255))
    trait_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    trait_name: Mapped[str] = mapped_column(String(255))
    trait_value: Mapped[float] = mapped_column(REAL)
    trait_data: Mapped[dict] = mapped_column(JSONB)
    record_info: Mapped[dict] = mapped_column(JSONB)

    __table_args__ = (
        UniqueConstraint(
            "timestamp",
            "collection_date",
            "dataset_id",
            "dataset_name",
            "trait_id",
            "trait_name",
            "record_info",
            name="trait_records_unique"
        ),
    )
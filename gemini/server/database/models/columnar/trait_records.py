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
)
from sqlalchemy.dialects.postgresql import JSONB
from gemini.server.database.models.columnar.columnar_base_model import ColumnarBaseModel
import uuid


class TraitRecordModel(ColumnarBaseModel):

    __tablename__ = "trait_records"

    dataset_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    dataset_name: Mapped[str] = mapped_column(String(255))
    trait_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    trait_name: Mapped[str] = mapped_column(String(255))
    trait_value: Mapped[float] = mapped_column(REAL)

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
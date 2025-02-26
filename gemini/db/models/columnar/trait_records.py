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
    experiment_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    experiment_name: Mapped[str] = mapped_column(String(255))
    season_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    season_name: Mapped[str] = mapped_column(String(255))
    site_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    site_name: Mapped[str] = mapped_column(String(255))
    plot_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    plot_number: Mapped[str] = mapped_column(String(255))
    plot_row_number: Mapped[str] = mapped_column(String(255))
    plot_column_number: Mapped[str] = mapped_column(String(255))
    record_info: Mapped[dict] = mapped_column(JSONB)

    __table_args__ = (
        UniqueConstraint(
            "timestamp",
            "collection_date",
            "trait_id",
            "trait_name",
            "dataset_id",
            "dataset_name",
            "experiment_id",
            "experiment_name",
            "season_id",
            "season_name",
            "site_id",
            "site_name",
            "plot_id",
            "plot_number",
            "plot_row_number",
            "plot_column_number",
        ),
        Index("idx_trait_records_record_info", "record_info", postgresql_using="GIN"),
    )
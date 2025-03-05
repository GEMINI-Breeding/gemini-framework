from sqlalchemy.orm import relationship, mapped_column, Mapped, Relationship
from sqlalchemy import UUID, JSON, String, Integer, UniqueConstraint, Index, ForeignKey, TIMESTAMP, DATE
from sqlalchemy.dialects.postgresql import JSONB

from gemini.db.core.base import ColumnarBaseModel
import uuid
from datetime import datetime, date


class ModelRecordModel(ColumnarBaseModel):

    __tablename__ = "model_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    collection_date: Mapped[date] = mapped_column(DATE, nullable=False)
    dataset_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    dataset_name: Mapped[str] = mapped_column(String(255))
    model_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    model_name: Mapped[str] = mapped_column(String(255))
    model_data : Mapped[dict] = mapped_column(JSONB)
    experiment_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    experiment_name: Mapped[str] = mapped_column(String(255))
    season_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    season_name: Mapped[str] = mapped_column(String(255))
    site_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    site_name: Mapped[str] = mapped_column(String(255))
    record_file : Mapped[str] = mapped_column(String(255))
    record_info: Mapped[dict] = mapped_column(JSONB)

    __table_args__ = (
        UniqueConstraint(
            'timestamp',
            'collection_date', 
            'model_id', 
            'model_name', 
            'dataset_id',
            'dataset_name', 
            'experiment_id',
            'experiment_name', 
            'season_id', 
            'season_name',
            'site_id',
            'site_name',
            name='model_records_unique'
        ),
        Index('idx_model_records_record_info', 'record_info', postgresql_using='GIN'),
    )

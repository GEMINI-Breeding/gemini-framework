from sqlalchemy.orm import relationship, mapped_column, Mapped, Relationship
from sqlalchemy import UUID, JSON, String, Integer, UniqueConstraint, Index, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from gemini.models.columnar.columnar_base_model import ColumnarBaseModel
import uuid


class ModelRecordModel(ColumnarBaseModel):

    __tablename__ = "model_records"

    dataset_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    dataset_name: Mapped[str] = mapped_column(String(255))
    model_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    model_name: Mapped[str] = mapped_column(String(255))
    model_data : Mapped[dict] = mapped_column(JSONB)

    __table_args__ = (
        UniqueConstraint(
            'timestamp',
            'collection_date', 
            'dataset_id', 
            'dataset_name', 
            'model_id', 
            'model_name', 
            'record_info',
            name='model_records_unique'
        ),
    )

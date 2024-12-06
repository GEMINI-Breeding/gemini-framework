from sqlalchemy.orm import relationship, mapped_column, Mapped, Relationship
from sqlalchemy import UUID, JSON, String, Integer, UniqueConstraint, Index, ForeignKey, TIMESTAMP, DATE
from sqlalchemy.dialects.postgresql import JSONB
from gemini.db.core.base import ColumnarBaseModel
import uuid
from datetime import datetime, date


class ProcedureRecordModel(ColumnarBaseModel):

    __tablename__ = "procedure_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    collection_date: Mapped[date] = mapped_column(DATE, nullable=False)
    dataset_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    dataset_name: Mapped[str] = mapped_column(String(255))
    procedure_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    procedure_name: Mapped[str] = mapped_column(String(255))
    procedure_data : Mapped[dict] = mapped_column(JSON)
    record_info: Mapped[dict] = mapped_column(JSONB)

    __table_args__ = (
        UniqueConstraint(
            'timestamp',
            'collection_date', 
            'dataset_id', 
            'dataset_name', 
            'procedure_id', 
            'procedure_name', 
            'record_info',
            name='procedure_records_unique'
        ),
    )


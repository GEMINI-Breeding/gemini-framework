from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import UUID, JSON, String, Integer, REAL
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import TIMESTAMP, DATE
from gemini.models.base_model import _BaseModel
import uuid

from datetime import datetime, date

class TraitRecordsIMMVModel(_BaseModel):
    
    __tablename__ = 'trait_records_immv'
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    collection_date: Mapped[date] = mapped_column(DATE, default=datetime.now)
    record_info: Mapped[dict] = mapped_column(JSONB)
    dataset_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    dataset_name: Mapped[str] = mapped_column(String)
    trait_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    trait_name: Mapped[str] = mapped_column(String)
    trait_value: Mapped[float] = mapped_column(REAL)
    
    
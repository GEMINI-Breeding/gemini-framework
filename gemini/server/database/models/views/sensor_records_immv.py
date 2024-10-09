from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import UUID, JSON, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import TIMESTAMP, DATE
from gemini.server.database.models.views.view_base import _BaseModel
import uuid

from datetime import datetime, date


class SensorRecordsIMMVModel(_BaseModel):
    
    __tablename__ = 'sensor_records_immv'
    
    id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    timestamp : Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    collection_date : Mapped[date] = mapped_column(DATE, default=datetime.now)
    record_info : Mapped[dict] = mapped_column(JSONB)
    dataset_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    dataset_name : Mapped[str] = mapped_column(String)
    sensor_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    sensor_name : Mapped[str] = mapped_column(String)
    sensor_data : Mapped[dict] = mapped_column(JSONB)
    
    
    
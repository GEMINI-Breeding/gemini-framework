from sqlalchemy import (
    JSON,
    String,
    TIMESTAMP,
    UniqueConstraint,
    Index,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID

from gemini.db.core.base import BaseModel

from datetime import datetime
import uuid


class SensorTypeModel(BaseModel):
  __tablename__ = 'sensor_types'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  sensor_type_name: Mapped[str] = mapped_column(String(255), nullable=False)
  sensor_type_info: Mapped[dict] = mapped_column(JSON, default={})
  created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
  updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

  __table_args__ = (
    UniqueConstraint('sensor_type_name'),
    Index('idx_sensor_types_info', 'sensor_type_info', postgresql_using='GIN')
  )



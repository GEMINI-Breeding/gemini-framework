from sqlalchemy import (
    JSON,
    String,
    TIMESTAMP,
    UniqueConstraint,
    Index,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID

from gemini.db.core.base import BaseModel

from datetime import datetime
import uuid


class SensorModel(BaseModel):
    __tablename__ = "sensors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=uuid.uuid4
    )
    sensor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sensor_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("gemini.sensor_types.id"), default=0
    )
    sensor_data_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("gemini.data_types.id"), default=0
    )
    sensor_data_format_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("gemini.data_formats.id"), default=0
    )
    sensor_info: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)

    __table_args__ = (
        UniqueConstraint("sensor_name"),
        Index("idx_sensors_info", "sensor_info", postgresql_using="GIN"),
    )

    sensor_type = relationship("SensorTypeModel", uselist=False)
    data_type = relationship("DataTypeModel", uselist=False)
    data_format = relationship("DataFormatModel", uselist=False)
    datasets = relationship("DatasetModel", secondary="gemini.sensor_datasets")

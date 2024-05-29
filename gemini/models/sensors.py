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

from gemini.models.base_model import BaseModel

from datetime import datetime
import uuid


class SensorModel(BaseModel):
    __tablename__ = "sensors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sensor_platform_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.sensor_platforms.id"))
    sensor_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("gemini.sensor_types.id"), default=0)
    sensor_data_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("gemini.data_types.id"), default=0)
    sensor_data_format_id: Mapped[int] = mapped_column(Integer, ForeignKey("gemini.data_formats.id"), default=0)
    sensor_info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        UniqueConstraint('sensor_name'),
        Index('idx_sensors_info', 'sensor_info', postgresql_using='GIN')
    )

    sensor_type = relationship("SensorTypeModel", uselist=False)
    sensor_platform = relationship("SensorPlatformModel", uselist=False)
    data_type = relationship("DataTypeModel", uselist=False)
    data_format = relationship("DataFormatModel", uselist=False)
    datasets = relationship("DatasetModel", secondary="gemini.sensor_datasets")


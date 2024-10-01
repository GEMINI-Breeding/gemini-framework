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

from gemini.server.database.models.base_model import BaseModel

from datetime import datetime
import uuid


class SensorPlatformModel(BaseModel):
    __tablename__ = "sensor_platforms"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=uuid.uuid4
    )
    sensor_platform_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sensor_platform_info: Mapped[dict] = mapped_column(JSON, default={})

    sensors = relationship("SensorModel", secondary="gemini.sensor_platform_sensors")

    __table_args__ = (
        UniqueConstraint("sensor_platform_name"),
        Index(
            "idx_sensor_platforms_info", "sensor_platform_info", postgresql_using="GIN"
        ),
    )

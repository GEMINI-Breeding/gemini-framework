from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import UUID, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from gemini.db.core.base import ViewBaseModel


class SensorPlatformSensorsViewModel(ViewBaseModel):

    __tablename__ = 'sensor_platform_sensors_view'

    sensor_platform_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    sensor_platform_name: Mapped[str] = mapped_column(String, primary_key=True)
    sensor_platform_info: Mapped[dict] = mapped_column(JSONB)
    sensor_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    sensor_name: Mapped[str] = mapped_column(String, primary_key=True)
    sensor_type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sensor_data_type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sensor_data_format_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sensor_info: Mapped[dict] = mapped_column(JSONB)
    sensor_platform_sensor_info: Mapped[dict] = mapped_column(JSONB)


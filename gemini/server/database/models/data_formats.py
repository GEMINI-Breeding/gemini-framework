from sqlalchemy import JSON, String, TIMESTAMP, UniqueConstraint, Index, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID

from gemini.server.database.models.base_model import BaseModel

from datetime import datetime
import uuid


class DataFormatModel(BaseModel):

    __tablename__ = "data_formats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data_format_name: Mapped[str] = mapped_column(String(255), nullable=False)
    data_format_mime_type: Mapped[str] = mapped_column(String(255), default='application/octet-stream')
    data_format_info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        UniqueConstraint('data_format_name', name='data_format_unique'),
        Index('idx_data_formats_info', 'data_format_info', postgresql_using='GIN')
    )
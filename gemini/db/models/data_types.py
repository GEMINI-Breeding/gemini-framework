from sqlalchemy import (
    JSON,
    String,
    TIMESTAMP,
    UniqueConstraint,
    Index,
    Integer
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from gemini.db.core.base import BaseModel
from datetime import datetime

class DataTypeModel(BaseModel):
    __tablename__ = 'data_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data_type_name: Mapped[str] = mapped_column(String(255), nullable=False)
    data_type_info: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        UniqueConstraint('data_type_name', name='data_type_unique'),
        Index('idx_data_types_info', 'data_type_info', postgresql_using='GIN')
    )

    formats = relationship('DataFormatModel', secondary='gemini.data_type_formats', lazy='selectin', cascade='save-update, merge, delete')
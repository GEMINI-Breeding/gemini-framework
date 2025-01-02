from sqlalchemy import (
    JSON,
    String,
    TIMESTAMP,
    UniqueConstraint,
    Index,
    Integer,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID

from gemini.db.core.base import BaseModel

from datetime import datetime
import uuid


class ResourceModel(BaseModel):
    __tablename__ = "resources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    resource_uri: Mapped[str] = mapped_column(String(255), nullable=False)
    resource_file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_external: Mapped[bool] = mapped_column(Boolean, default=False)
    resource_experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.experiments.id"), default=None)
    resource_data_format_id: Mapped[int] = mapped_column(Integer, ForeignKey("gemini.data_formats.id"), default=0)
    resource_info: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        UniqueConstraint('resource_uri', 'resource_file_name'),
        Index('idx_resources_info', 'resource_info', postgresql_using='GIN')
    )

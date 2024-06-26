from sqlalchemy import (
    JSON,
    String,
    TIMESTAMP,
    UniqueConstraint,
    Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID

from gemini.models.base_model import BaseModel

from datetime import datetime
import uuid



class SiteModel(BaseModel):
  __tablename__ = 'sites'

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  site_name: Mapped[str] = mapped_column(String(255), nullable=False)
  site_city: Mapped[str] = mapped_column(String(255), default='')
  site_state: Mapped[str] = mapped_column(String(255), default='')
  site_country: Mapped[str] = mapped_column(String(255), default='')
  site_info: Mapped[dict] = mapped_column(JSON, default={})

  __table_args__ = (
    UniqueConstraint('site_name', 'site_city', 'site_state', 'site_country'),
    Index('idx_sites_info', 'site_info', postgresql_using='GIN')
  )

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
from sqlalchemy.dialects.postgresql import UUID, JSONB

from gemini.db.core.base import BaseModel

from datetime import datetime
import uuid



class SiteModel(BaseModel):
  __tablename__ = 'sites'

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
  site_name: Mapped[str] = mapped_column(String(255), nullable=False)
  site_city: Mapped[str] = mapped_column(String(255), default='')
  site_state: Mapped[str] = mapped_column(String(255), default='')
  site_country: Mapped[str] = mapped_column(String(255), default='')
  site_info: Mapped[dict] = mapped_column(JSONB, default={})
  created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
  updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)


  __table_args__ = (
    UniqueConstraint('site_name', 'site_city', 'site_state', 'site_country'),
    Index('idx_sites_info', 'site_info', postgresql_using='GIN')
  )

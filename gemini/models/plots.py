from sqlalchemy import (
    UniqueConstraint,
    Index,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB

from gemini.models.base_model import BaseModel

import uuid


class PlotModel(BaseModel):
  __tablename__ = 'plots'

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
  experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('gemini.experiments.id'))
  season_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('gemini.seasons.id'))
  site_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('gemini.sites.id'))
  plot_number: Mapped[int] = mapped_column(Integer)
  plot_row_number: Mapped[int] = mapped_column(Integer)
  plot_column_number: Mapped[int] = mapped_column(Integer)
  plot_geometry_info: Mapped[dict] = mapped_column(JSONB, default={})
  plot_info: Mapped[dict] = mapped_column(JSONB, default={})

  __table_args__ = (
    UniqueConstraint('experiment_id', 'season_id', 'site_id', 'plot_number', 'plot_row_number', 'plot_column_number'),
    Index('idx_plots_info', 'plot_info', postgresql_using='GIN')
  )

  experiment = relationship('ExperimentModel', uselist=False)
  season = relationship('SeasonModel', uselist=False)
  site = relationship('SiteModel', uselist=False)
  cultivars = relationship('CultivarModel', secondary='gemini.plot_cultivars')
  plants = relationship('PlantModel')


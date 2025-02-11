from sqlalchemy import (
    JSON,
    String,
    TIMESTAMP,
    UniqueConstraint,
    CheckConstraint,
    Index,
    DATE,
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB

from gemini.db.core.base import BaseModel

from datetime import datetime, date
import uuid


class ExperimentModel(BaseModel):
    __tablename__ = "experiments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=uuid.uuid4
    )
    experiment_name: Mapped[str] = mapped_column(String(255), nullable=False)
    experiment_info: Mapped[dict] = mapped_column(JSONB, nullable=True)
    experiment_start_date: Mapped[date] = mapped_column(DATE, nullable=False, default=datetime.now)
    experiment_end_date: Mapped[date] = mapped_column(DATE, nullable=False, default=datetime.now)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        UniqueConstraint("experiment_name"),
        CheckConstraint("experiment_start_date <= experiment_end_date"),
        CheckConstraint("experiment_end_date >= experiment_start_date"),
        Index("idx_experiments_info", "experiment_info", postgresql_using="GIN"),
    )

    seasons = relationship("SeasonModel", lazy="subquery")
    resources = relationship("ResourceModel", lazy="subquery")

    sites = relationship("SiteModel", secondary="gemini.experiment_sites", lazy="subquery")
    sensors = relationship("SensorModel", secondary="gemini.experiment_sensors", lazy="subquery")
    cultivars = relationship("CultivarModel", secondary="gemini.experiment_cultivars", lazy="subquery")
    datasets = relationship("DatasetModel", secondary="gemini.experiment_datasets", lazy="subquery")
    traits = relationship("TraitModel", secondary="gemini.experiment_traits", lazy="subquery")
    models = relationship("ModelModel", secondary="gemini.experiment_models", lazy="subquery")
    scripts = relationship("ScriptModel", secondary="gemini.experiment_scripts", lazy="subquery")
    procedures = relationship("ProcedureModel", secondary="gemini.experiment_procedures", lazy="subquery")
    platforms = relationship("SensorPlatformModel", secondary="gemini.experiment_sensor_platforms", lazy="subquery")

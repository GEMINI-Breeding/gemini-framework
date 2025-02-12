from sqlalchemy import Integer, JSON, TIMESTAMP
from sqlalchemy import ForeignKey, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid
from gemini.db.core.base import BaseModel


class DataTypeFormatModel(BaseModel):
    __tablename__ = "data_type_formats"

    data_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("gemini.data_types.id", ondelete="CASCADE"), primary_key=True)
    data_format_id: Mapped[int] = mapped_column(Integer, ForeignKey("gemini.data_formats.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        UniqueConstraint("data_type_id", "data_format_id", name="data_type_format_unique"),
    )


class ExperimentSiteModel(BaseModel):
    __tablename__ = "experiment_sites"

    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.experiments.id", ondelete="CASCADE"), primary_key=True)
    site_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.sites.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (

        UniqueConstraint("experiment_id", "site_id", name="experiment_site_unique"),
    )


class ExperimentSensorModel(BaseModel):
    __tablename__ = "experiment_sensors"

    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.experiments.id", ondelete="CASCADE"), primary_key=True)
    sensor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.sensors.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    __table_args__ = (
        UniqueConstraint("experiment_id", "sensor_id", name="experiment_sensor_unique"),
    )


class ExperimentSensorPlatformModel(BaseModel):
    __tablename__ = "experiment_sensor_platforms"

    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.experiments.id", ondelete="CASCADE"), primary_key=True)
    sensor_platform_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.sensor_platforms.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)



    __table_args__ = (
        UniqueConstraint("experiment_id", "sensor_platform_id", name="experiment_sensor_platform_unique"),
    )

class ExperimentTraitModel(BaseModel):
    __tablename__ = "experiment_traits"

    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.experiments.id", ondelete="CASCADE"), primary_key=True)
    trait_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.traits.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    __table_args__ = (
        UniqueConstraint("experiment_id", "trait_id", name="experiment_trait_unique"),
    )

class ExperimentCultivarModel(BaseModel):
    __tablename__ = "experiment_cultivars"

    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.experiments.id", ondelete="CASCADE"), primary_key=True)
    cultivar_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.cultivars.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    __table_args__ = (
        UniqueConstraint("experiment_id", "cultivar_id", name="experiment_cultivar_unique"),
    )


class ExperimentModelModel(BaseModel):
    __tablename__ = "experiment_models"

    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.experiments.id", ondelete="CASCADE"), primary_key=True)
    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.models.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)



    __table_args__ = (
        UniqueConstraint("experiment_id", "model_id", name="experiment_model_unique"),
    )

class ExperimentProcedureModel(BaseModel):
    __tablename__ = "experiment_procedures"

    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.experiments.id", ondelete="CASCADE"), primary_key=True)
    procedure_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.procedures.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    __table_args__ = (
        UniqueConstraint("experiment_id", "procedure_id", name="experiment_procedure_unique"),
    )

class ExperimentScriptModel(BaseModel):
    __tablename__ = "experiment_scripts"

    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.experiments.id", ondelete="CASCADE"), primary_key=True)
    script_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.scripts.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    __table_args__ = (
        UniqueConstraint("experiment_id", "script_id", name="experiment_script_unique"),
    )

class ExperimentDatasetModel(BaseModel):
    __tablename__ = "experiment_datasets"

    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.experiments.id", ondelete="CASCADE"), primary_key=True)
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.datasets.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        UniqueConstraint("experiment_id", "dataset_id", name="experiment_dataset_unique"),
    )

class PlotCultivarModel(BaseModel):
    __tablename__ = "plot_cultivars"

    plot_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.plots.id", ondelete="CASCADE"), primary_key=True)
    cultivar_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.cultivars.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    __table_args__ = (
        UniqueConstraint("plot_id", "cultivar_id", name="plot_cultivar_unique"),
    )

class TraitSensorModel(BaseModel):
    __tablename__ = "trait_sensors"

    trait_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.traits.id", ondelete="CASCADE"), primary_key=True)
    sensor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.sensors.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    __table_args__ = (
        UniqueConstraint("trait_id", "sensor_id", name="trait_sensor_unique"),
    )

class SensorPlatformSensorModel(BaseModel):
    __tablename__ = "sensor_platform_sensors"

    sensor_platform_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.sensor_platforms.id", ondelete="CASCADE"), primary_key=True)
    sensor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.sensors.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    __table_args__ = (
        UniqueConstraint("sensor_platform_id", "sensor_id", name="sensor_platform_sensor_unique"),
    )

class SensorDatasetModel(BaseModel):
    __tablename__ = "sensor_datasets"

    sensor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.sensors.id", ondelete="CASCADE"), primary_key=True)
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.datasets.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    __table_args__ = (
        UniqueConstraint("sensor_id", "dataset_id", name="sensor_dataset_unique"),
    )

class TraitDatasetModel(BaseModel):
    __tablename__ = "trait_datasets"

    trait_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.traits.id", ondelete="CASCADE"), primary_key=True)
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.datasets.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    __table_args__ = (
        UniqueConstraint("trait_id", "dataset_id", name="trait_dataset_unique"),
    )


class ModelDatasetModel(BaseModel):
    __tablename__ = "model_datasets"

    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.models.id", ondelete="CASCADE"), primary_key=True)
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.datasets.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    __table_args__ = (
        UniqueConstraint("model_id", "dataset_id", name="model_dataset_unique"),
    )


class ScriptDatasetModel(BaseModel):
    __tablename__ = "script_datasets"

    script_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.scripts.id", ondelete="CASCADE"), primary_key=True)
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.datasets.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    __table_args__ = (
        UniqueConstraint("script_id", "dataset_id", name="script_dataset_unique"),
    )


class ProcedureDatasetModel(BaseModel):
    __tablename__ = "procedure_datasets"

    procedure_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.procedures.id", ondelete="CASCADE"), primary_key=True)
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), ForeignKey("gemini.datasets.id", ondelete="CASCADE"), primary_key=True)
    info: Mapped[dict] = mapped_column(JSONB, default={})
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)


    __table_args__ = (
        UniqueConstraint("procedure_id", "dataset_id", name="procedure_dataset_unique"),
    )


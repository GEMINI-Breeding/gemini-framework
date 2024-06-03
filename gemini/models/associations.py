from sqlalchemy import (
    JSON,
    String,
    TIMESTAMP,
    UniqueConstraint,
    Index,
    Integer,
    ForeignKey,
    PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID

from gemini.models.base_model import BaseModel

from datetime import datetime
import uuid


class DataTypeFormatModel(BaseModel):
    __tablename__ = "data_type_formats"

    data_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("gemini.data_types.id", ondelete="CASCADE"))
    data_format_id: Mapped[int] = mapped_column(Integer, ForeignKey("gemini.data_formats.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        PrimaryKeyConstraint("data_type_id", "data_format_id"),
    )



class ExperimentSiteModel(BaseModel):
    __tablename__ = "experiment_sites"

    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.experiments.id", ondelete="CASCADE"))
    site_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.sites.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        PrimaryKeyConstraint("experiment_id", "site_id"),
    )

class ExperimentSensorModel(BaseModel):
    __tablename__ = "experiment_sensors"

    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.experiments.id", ondelete="CASCADE"))
    sensor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.sensors.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        PrimaryKeyConstraint("experiment_id", "sensor_id"),
    )



class ExperimentTraitModel(BaseModel):
    __tablename__ = "experiment_traits"

    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.experiments.id", ondelete="CASCADE"))
    trait_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.traits.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        PrimaryKeyConstraint("experiment_id", "trait_id"),
    )



class ExperimentCultivarModel(BaseModel):
    __tablename__ = "experiment_cultivars"

    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.experiments.id", ondelete="CASCADE"))
    cultivar_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.cultivars.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        PrimaryKeyConstraint("experiment_id", "cultivar_id"),
    )


class ExperimentModelModel(BaseModel):
    __tablename__ = "experiment_models"
    
    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.experiments.id", ondelete="CASCADE"))
    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.models.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})
    
    __table_args__ = (
        PrimaryKeyConstraint("experiment_id", "model_id"),
    )
    
class ExperimentProcedureModel(BaseModel):
    __tablename__ = "experiment_procedures"
    
    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.experiments.id", ondelete="CASCADE"))
    procedure_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.procedures.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})
    
    __table_args__ = (
        PrimaryKeyConstraint("experiment_id", "procedure_id"),
    )

class ExperimentScriptModel(BaseModel):
    __tablename__ = "experiment_scripts"
    
    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.experiments.id", ondelete="CASCADE"))
    script_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.scripts.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})
    
    __table_args__ = (
        PrimaryKeyConstraint("experiment_id", "script_id"),
    )

class ExperimentDatasetModel(BaseModel):
    __tablename__ = "experiment_datasets"

    experiment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.experiments.id", ondelete="CASCADE"))
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.datasets.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        PrimaryKeyConstraint("experiment_id", "dataset_id"),
    )



class PlotCultivarModel(BaseModel):
    __tablename__ = "plot_cultivars"

    plot_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.plots.id", ondelete="CASCADE"))
    cultivar_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.cultivars.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        PrimaryKeyConstraint("plot_id", "cultivar_id"),
    )



class TraitSensorModel(BaseModel):
    __tablename__ = "trait_sensors"

    trait_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.traits.id", ondelete="CASCADE"))
    sensor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.sensors.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        PrimaryKeyConstraint("trait_id", "sensor_id"),
    )



class SensorDatasetModel(BaseModel):
    __tablename__ = "sensor_datasets"

    sensor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.sensors.id", ondelete="CASCADE"))
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.datasets.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        PrimaryKeyConstraint("sensor_id", "dataset_id"),
    )



class TraitDatasetModel(BaseModel):
    __tablename__ = "trait_datasets"

    trait_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.traits.id", ondelete="CASCADE"))
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.datasets.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        PrimaryKeyConstraint("trait_id", "dataset_id"),
    )



class ModelDatasetModel(BaseModel):
    __tablename__ = "model_datasets"

    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.models.id", ondelete="CASCADE"))
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.datasets.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        PrimaryKeyConstraint("model_id", "dataset_id"),
    )



class ScriptDatasetModel(BaseModel):
    __tablename__ = "script_datasets"

    script_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.scripts.id", ondelete="CASCADE"))
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.datasets.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        PrimaryKeyConstraint("script_id", "dataset_id"),
    )



class ProcedureDatasetModel(BaseModel):
    __tablename__ = "procedure_datasets"

    procedure_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.procedures.id", ondelete="CASCADE"))
    dataset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.datasets.id", ondelete="CASCADE"))
    info: Mapped[dict] = mapped_column(JSON, default={})

    __table_args__ = (
        PrimaryKeyConstraint("procedure_id", "dataset_id"),
    )


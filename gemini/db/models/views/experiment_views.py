from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import UUID, JSON, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from gemini.db.core.base import MaterializedViewBaseModel

class ExperimentSeasonsViewModel(MaterializedViewBaseModel):

    __tablename__ = 'experiment_seasons_view'

    experiment_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String)
    season_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    season_name : Mapped[str] = mapped_column(String)
    season_start_date : Mapped[str] = mapped_column(String)
    season_end_date : Mapped[str] = mapped_column(String)
    season_info : Mapped[dict] = mapped_column(JSONB)

class ExperimentSitesViewModel(MaterializedViewBaseModel):

    __tablename__ = 'experiment_sites_view'

    experiment_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String)
    site_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    site_name : Mapped[str] = mapped_column(String)
    site_city : Mapped[str] = mapped_column(String)
    site_state : Mapped[str] = mapped_column(String)
    site_country : Mapped[str] = mapped_column(String)
    site_info : Mapped[dict] = mapped_column(JSONB)


class ExperimentTraitsViewModel(MaterializedViewBaseModel):

    __tablename__ = 'experiment_traits_view'

    experiment_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String)
    trait_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    trait_name : Mapped[str] = mapped_column(String)
    trait_units : Mapped[str] = mapped_column(String)
    trait_metrics : Mapped[str] = mapped_column(String)
    trait_level_id : Mapped[int] = mapped_column(Integer)
    trait_info : Mapped[dict] = mapped_column(JSONB)



class ExperimentSensorsViewModel(MaterializedViewBaseModel):

    __tablename__ = 'experiment_sensors_view'

    experiment_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String)
    sensor_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    sensor_name : Mapped[str] = mapped_column(String)
    sensor_type_id : Mapped[int] = mapped_column(Integer)
    sensor_data_type_id : Mapped[int] = mapped_column(Integer)
    sensor_data_format_id : Mapped[int] = mapped_column(Integer)
    sensor_info : Mapped[dict] = mapped_column(JSONB)
    sensor_platform_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    sensor_platform_name : Mapped[str] = mapped_column(String)
    sensor_platform_info : Mapped[dict] = mapped_column(JSONB)


class ExperimentSensorPlatformsViewModel(MaterializedViewBaseModel):

    __tablename__ = 'experiment_sensor_platforms_view'

    experiment_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String)
    sensor_platform_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    sensor_platform_name : Mapped[str] = mapped_column(String)
    sensor_platform_info : Mapped[dict] = mapped_column(JSONB)
    


class ExperimentCultivarsViewModel(MaterializedViewBaseModel):

    __tablename__ = 'experiment_cultivars_view'

    experiment_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String)
    cultivar_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    cultivar_accession : Mapped[str] = mapped_column(String)
    cultivar_population : Mapped[str] = mapped_column(String)
    cultivar_info : Mapped[dict] = mapped_column(JSONB)




class ExperimentProceduresViewModel(MaterializedViewBaseModel):

    __tablename__ = 'experiment_procedures_view'

    experiment_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String)
    procedure_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    procedure_name : Mapped[str] = mapped_column(String)
    procedure_info : Mapped[dict] = mapped_column(JSONB)


class ExperimentScriptsViewModel(MaterializedViewBaseModel):

    __tablename__ = 'experiment_scripts_view'

    experiment_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String)
    script_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    script_name : Mapped[str] = mapped_column(String)
    script_url : Mapped[str] = mapped_column(String)
    script_extension : Mapped[str] = mapped_column(String)
    script_info : Mapped[dict] = mapped_column(JSONB)


class ExperimentModelsViewModel(MaterializedViewBaseModel):

    __tablename__ = 'experiment_models_view'

    experiment_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String)
    model_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    model_name : Mapped[str] = mapped_column(String)
    model_url : Mapped[str] = mapped_column(String)
    model_info : Mapped[dict] = mapped_column(JSONB)



class ExperimentDatasetsViewModel(MaterializedViewBaseModel):

    __tablename__ = 'experiment_datasets_view'

    experiment_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String)
    dataset_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    collection_date : Mapped[str] = mapped_column(String)
    dataset_name : Mapped[str] = mapped_column(String)
    dataset_type_id : Mapped[int] = mapped_column(Integer)
    dataset_info : Mapped[dict] = mapped_column(JSONB)

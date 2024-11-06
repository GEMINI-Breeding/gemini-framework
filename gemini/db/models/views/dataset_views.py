from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import UUID, JSON, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from gemini.db.core.base import ViewBaseModel

class SensorDatasetsViewModel(ViewBaseModel):

    __tablename__ = 'sensor_datasets_view'

    sensor_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    sensor_name : Mapped[str] = mapped_column(String)
    dataset_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    dataset_name : Mapped[str] = mapped_column(String)
    sensor_dataset_info : Mapped[JSON] = mapped_column(JSON)

class TraitDatasetsViewModel(ViewBaseModel):

    __tablename__ = 'trait_datasets_view'

    trait_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    trait_name : Mapped[str] = mapped_column(String)
    dataset_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    dataset_name : Mapped[str] = mapped_column(String)
    trait_dataset_info : Mapped[JSON] = mapped_column(JSON)


class ProcedureDatasetsViewModel(ViewBaseModel):
    
    __tablename__ = 'procedure_datasets_view'

    procedure_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    procedure_name : Mapped[str] = mapped_column(String)
    dataset_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    dataset_name : Mapped[str] = mapped_column(String)
    procedure_dataset_info : Mapped[JSON] = mapped_column(JSON)


class ScriptDatasetsViewModel(ViewBaseModel):
     
    __tablename__ = 'script_datasets_view'

    script_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    script_name : Mapped[str] = mapped_column(String)
    dataset_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    dataset_name : Mapped[str] = mapped_column(String)
    script_dataset_info : Mapped[JSON] = mapped_column(JSON)



class ModelDatasetsViewModel(ViewBaseModel):
      
    __tablename__ = 'model_datasets_view'

    model_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    model_name : Mapped[str] = mapped_column(String)
    dataset_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    dataset_name : Mapped[str] = mapped_column(String)
    model_dataset_info : Mapped[JSON] = mapped_column(JSON)

    
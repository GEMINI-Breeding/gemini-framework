from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import UUID, JSON, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from gemini.db.core.base import MaterializedViewBaseModel, ViewBaseModel

class ProcedureRunsViewModel(ViewBaseModel):

    __tablename__ = 'procedure_runs_view'

    procedure_run_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    procedure_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    procedure_name: Mapped[str] = mapped_column(String)
    procedure_info: Mapped[dict] = mapped_column(JSONB)
    procedure_run_info: Mapped[dict] = mapped_column(JSONB)


class ScriptRunsViewModel(ViewBaseModel):

    __tablename__ = 'script_runs_view'

    script_run_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    script_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    script_name: Mapped[str] = mapped_column(String)
    script_url: Mapped[str] = mapped_column(String)
    script_extension: Mapped[str] = mapped_column(String)
    script_info: Mapped[dict] = mapped_column(JSONB)
    script_run_info: Mapped[dict] = mapped_column(JSONB)

class ModelRunsViewModel(ViewBaseModel):

    __tablename__ = 'model_runs_view'

    model_run_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    model_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    model_name: Mapped[str] = mapped_column(String)
    model_url: Mapped[str] = mapped_column(String)
    model_info: Mapped[dict] = mapped_column(JSONB)
    model_run_info: Mapped[dict] = mapped_column(JSONB)
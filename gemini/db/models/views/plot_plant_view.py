from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import UUID, JSON, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from gemini.db.core.base import ViewBaseModel


class PlotPlantViewModel(ViewBaseModel):

    __tablename__ = 'plot_plant_view'

    plot_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    plot_number : Mapped[int] = mapped_column(Integer)
    plot_row_number : Mapped[int] = mapped_column(Integer)
    plot_column_number : Mapped[int] = mapped_column(Integer)
    plot_geometry_info : Mapped[dict] = mapped_column(JSONB)
    plot_info : Mapped[dict] = mapped_column(JSONB)
    plant_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    plant_number : Mapped[int] = mapped_column(Integer)
    plant_info : Mapped[dict] = mapped_column(JSONB)
    cultivar_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    cultivar_accession: Mapped[str] = mapped_column(String, primary_key=True)
    cultivar_population: Mapped[str] = mapped_column(String, primary_key=True)

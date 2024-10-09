from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import UUID, JSON, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from gemini.server.database.models.views.view_base import ViewBaseModel
import uuid


class PlotCultivarViewModel(ViewBaseModel):

    __tablename__ = 'plot_cultivar_view'

    plot_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    plot_number : Mapped[int] = mapped_column(Integer)
    plot_row_number : Mapped[int] = mapped_column(Integer)
    plot_column_number : Mapped[int] = mapped_column(Integer)
    plot_info : Mapped[dict] = mapped_column(JSONB)
    cultivar_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    cultivar_accession : Mapped[str] = mapped_column(String)
    cultivar_population : Mapped[str] = mapped_column(String)

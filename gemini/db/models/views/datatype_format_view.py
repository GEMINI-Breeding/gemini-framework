from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import UUID, JSON, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from gemini.db.core.base import ViewBaseModel


class DataTypeFormatsViewModel(ViewBaseModel):

    __tablename__ = 'datatype_formats_view'

    data_type_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    data_type_name: Mapped[str] = mapped_column(String, primary_key=True)
    data_type_info: Mapped[dict] = mapped_column(JSONB)
    data_format_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    data_format_name: Mapped[str] = mapped_column(String, primary_key=True)
    data_format_mime_type: Mapped[str] = mapped_column(String, nullable=True)
    data_format_info: Mapped[dict] = mapped_column(JSONB, nullable=True)



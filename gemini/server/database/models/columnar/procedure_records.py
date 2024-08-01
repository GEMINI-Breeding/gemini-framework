from sqlalchemy.orm import relationship, mapped_column, Mapped, Relationship
from sqlalchemy import UUID, JSON, String, Integer, UniqueConstraint, Index, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from gemini.server.database.models.columnar.columnar_base_model import ColumnarBaseModel
import uuid


class ProcedureRecordModel(ColumnarBaseModel):

    __tablename__ = "procedure_records"

    dataset_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    dataset_name: Mapped[str] = mapped_column(String(255))
    procedure_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    procedure_name: Mapped[str] = mapped_column(String(255))
    procedure_data : Mapped[dict] = mapped_column(JSON)

    __table_args__ = (
        UniqueConstraint(
            'timestamp',
            'collection_date', 
            'dataset_id', 
            'dataset_name', 
            'procedure_id', 
            'procedure_name', 
            'record_info',
            name='procedure_records_unique'
        ),
    )


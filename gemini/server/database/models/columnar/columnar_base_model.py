from gemini.server.database.models.base_model import _BaseModel
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import UUID, TIMESTAMP, DATE, String
from datetime import datetime
import uuid



class ColumnarBaseModel(_BaseModel):

    __abstract__ = True

    id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp : Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    collection_date : Mapped[datetime] = mapped_column(DATE, default=datetime.now)
    record_info : Mapped[dict] = mapped_column(JSONB)



    

    

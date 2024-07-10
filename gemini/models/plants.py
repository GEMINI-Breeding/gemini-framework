from sqlalchemy import (
    JSON,
    String,
    TIMESTAMP,
    UniqueConstraint,
    Index,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB

from gemini.models.base_model import BaseModel

from datetime import datetime
import uuid


class PlantModel(BaseModel):
    __tablename__ = "plants"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    plot_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.plots.id"))
    plant_number: Mapped[int] = mapped_column(Integer)
    plant_info: Mapped[dict] = mapped_column(JSONB, default={})
    cultivar_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gemini.cultivars.id"))

    __table_args__ = (
        UniqueConstraint("plot_id", "plant_number"),
        Index("idx_plants_info", "plant_info", postgresql_using="GIN"),
    )

    cultivar = relationship("CultivarModel")


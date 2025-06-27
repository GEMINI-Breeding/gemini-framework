"""
SQLAlchemy model for columnar TraitRecord entities in the GEMINI database.
"""

from sqlalchemy.orm import relationship, mapped_column, Mapped, Relationship
from sqlalchemy import (
    UUID,
    REAL,
    JSON,
    String,
    Integer,
    UniqueConstraint,
    Index,
    ForeignKey,
    TIMESTAMP,
    DATE,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text, bindparam
from gemini.db.core.base import ColumnarBaseModel, db_engine
import uuid
from datetime import datetime, date
from typing import Optional, List



class TraitRecordModel(ColumnarBaseModel):
    """
    Represents a trait record in the GEMINI database.

    Attributes:
        id (uuid.UUID): Unique identifier for the trait record.
        timestamp (datetime): Timestamp of the record.
        collection_date (date): The date when the data was collected.
        dataset_id (UUID): Foreign key referencing the dataset.
        dataset_name (str): The name of the dataset.
        trait_id (UUID): Foreign key referencing the trait.
        trait_name (str): The name of the trait.
        trait_value (float): The value of the trait.
        experiment_id (UUID): Foreign key referencing the experiment.
        experiment_name (str): The name of the experiment.
        season_id (UUID): Foreign key referencing the season.
        season_name (str): The name of the season.
        site_id (UUID): Foreign key referencing the site.
        site_name (str): The name of the site.
        plot_id (UUID): Foreign key referencing the plot.
        plot_number (str): The number of the plot.
        plot_row_number (str): The row number of the plot.
        plot_column_number (str): The column number of the plot.
        record_info (dict): Additional JSONB data for the record.
    """

    __tablename__ = "trait_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    collection_date: Mapped[date] = mapped_column(DATE, nullable=False)
    dataset_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    dataset_name: Mapped[str] = mapped_column(String(255))
    trait_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    trait_name: Mapped[str] = mapped_column(String(255))
    trait_value: Mapped[float] = mapped_column(REAL)
    experiment_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    experiment_name: Mapped[str] = mapped_column(String(255))
    season_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    season_name: Mapped[str] = mapped_column(String(255))
    site_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    site_name: Mapped[str] = mapped_column(String(255))
    plot_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
    plot_number: Mapped[str] = mapped_column(String(255))
    plot_row_number: Mapped[str] = mapped_column(String(255))
    plot_column_number: Mapped[str] = mapped_column(String(255))
    record_info: Mapped[dict] = mapped_column(JSONB)

    __table_args__ = (
        UniqueConstraint(
            "timestamp",
            "collection_date",
            "trait_id",
            "trait_name",
            "dataset_id",
            "dataset_name",
            "experiment_id",
            "experiment_name",
            "season_id",
            "season_name",
            "site_id",
            "site_name",
            "plot_id",
            "plot_number",
            "plot_row_number",
            "plot_column_number",
            name="trait_records_unique"
        ),
        Index("idx_trait_records_record_info", "record_info", postgresql_using="GIN"),
    )

    @classmethod
    def filter_records(
        cls,
        start_timestamp: Optional[datetime] = None,
        end_timestamp: Optional[datetime] = None,
        trait_names: Optional[List[str]] = None,
        dataset_names: Optional[List[str]] = None,
        experiment_names: Optional[List[str]] = None,
        season_names: Optional[List[str]] = None,
        site_names: Optional[List[str]] = None
    ):
        """
        Filters trait records based on the provided parameters.

        Args:
            start_timestamp (Optional[datetime]): The starting timestamp for the filter.
            end_timestamp (Optional[datetime]): The ending timestamp for the filter.
            trait_names (Optional[List[str]]): A list of trait names to filter by.
            dataset_names (Optional[List[str]]): A list of dataset names to filter by.
            experiment_names (Optional[List[str]]): A list of experiment names to filter by.
            season_names (Optional[List[str]]): A list of season names to filter by.
            site_names (Optional[List[str]]): A list of site names to filter by.

        Yields:
            record: Matching trait records.
        """
        stmt = text(
            """
            SELECT * FROM gemini.filter_trait_records(
                p_start_timestamp => :start_timestamp,
                p_end_timestamp => :end_timestamp,
                p_trait_names => :trait_names,
                p_dataset_names => :dataset_names,
                p_experiment_names => :experiment_names,
                p_season_names => :season_names,
                p_site_names => :site_names
            )
            """
        ).bindparams(
            bindparam("start_timestamp", value=start_timestamp),
            bindparam("end_timestamp", value=end_timestamp),
            bindparam("trait_names", value=trait_names),
            bindparam("dataset_names", value=dataset_names),
            bindparam("experiment_names", value=experiment_names),
            bindparam("season_names", value=season_names),
            bindparam("site_names", value=site_names)
        )

        with db_engine.get_session() as session:
            result = session.execute(stmt, execution_options={"yield_per": 1000})
            for record in result:
                yield record

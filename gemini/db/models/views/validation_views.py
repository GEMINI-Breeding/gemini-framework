from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import UUID, String, Integer, REAL
from sqlalchemy.dialects.postgresql import JSONB
from gemini.db.core.base import ViewBaseModel

class ValidPlotCombinationsViewModel(ViewBaseModel):
    __tablename__ = 'valid_plot_combinations_view'

    experiment_name : Mapped[str] = mapped_column(String, primary_key=True)
    experiment_id : Mapped[UUID] = mapped_column(UUID, primary_key=True)
    season_name : Mapped[str] = mapped_column(String, primary_key=True)
    season_id : Mapped[UUID] = mapped_column(UUID, primary_key=True)
    site_name : Mapped[str] = mapped_column(String, primary_key=True)
    site_id : Mapped[UUID] = mapped_column(UUID, primary_key=True)


class ValidDatasetCombinationsViewModel(ViewBaseModel):
    
    __tablename__ = 'valid_dataset_combinations_view'

    dataset_name : Mapped[str] = mapped_column(String, primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String, primary_key=True)
    season_name : Mapped[str] = mapped_column(String, primary_key=True)
    site_name : Mapped[str] = mapped_column(String, primary_key=True)

class ValidSensorDatasetCombinationsViewModel(ViewBaseModel):

    __tablename__ = 'valid_sensor_dataset_combinations_view'

    dataset_name : Mapped[str] = mapped_column(String, primary_key=True)
    sensor_name : Mapped[str] = mapped_column(String, primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String, primary_key=True)
    season_name : Mapped[str] = mapped_column(String, primary_key=True)
    site_name : Mapped[str] = mapped_column(String, primary_key=True)

class ValidTraitDatasetCombinationsViewModel(ViewBaseModel):
    
    __tablename__ = 'valid_trait_dataset_combinations_view'

    dataset_name : Mapped[str] = mapped_column(String, primary_key=True)
    trait_name : Mapped[str] = mapped_column(String, primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String, primary_key=True)
    season_name : Mapped[str] = mapped_column(String, primary_key=True)
    site_name : Mapped[str] = mapped_column(String, primary_key=True)

class ValidProcedureDatasetCombinationsViewModel(ViewBaseModel):
    
    __tablename__ = 'valid_procedure_dataset_combinations_view'

    dataset_name : Mapped[str] = mapped_column(String, primary_key=True)
    procedure_name : Mapped[str] = mapped_column(String, primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String, primary_key=True)
    season_name : Mapped[str] = mapped_column(String, primary_key=True)
    site_name : Mapped[str] = mapped_column(String, primary_key=True)

class ValidScriptDatasetCombinationsViewModel(ViewBaseModel):
    
    __tablename__ = 'valid_script_dataset_combinations_view'

    dataset_name : Mapped[str] = mapped_column(String, primary_key=True)
    script_name : Mapped[str] = mapped_column(String, primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String, primary_key=True)
    season_name : Mapped[str] = mapped_column(String, primary_key=True)
    site_name : Mapped[str] = mapped_column(String, primary_key=True)

class ValidModelDatasetCombinationsViewModel(ViewBaseModel):
    
    __tablename__ = 'valid_model_dataset_combinations_view'

    dataset_name : Mapped[str] = mapped_column(String, primary_key=True)
    model_name : Mapped[str] = mapped_column(String, primary_key=True)
    experiment_name : Mapped[str] = mapped_column(String, primary_key=True)
    season_name : Mapped[str] = mapped_column(String, primary_key=True)
    site_name : Mapped[str] = mapped_column(String, primary_key=True)



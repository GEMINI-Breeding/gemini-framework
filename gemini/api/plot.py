from typing import Optional, List, Any, Union
from pydantic import Field, BaseModel
from typing import Generator
from gemini.api.base import APIBase
from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site
from gemini.api.cultivar import Cultivar
from gemini.api.plant import Plant
from gemini.models import PlotModel, PlotViewModel, PlotCultivarViewModel
from gemini.models import ExperimentModel, SiteModel, SeasonModel, CultivarModel
from gemini.logger import logger_service

from uuid import UUID

class PlotSearchParameters(BaseModel):
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None

class Plot(APIBase):

    db_model = PlotModel

    plot_id : Union[UUID, int, str] = Field(None, alias="plot_id")
    plot_number: int
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    plot_geometry_info: Optional[dict] = None
    plot_info: Optional[dict] = None

    experiment: Optional[Experiment] = None
    season: Optional[Season] = None
    site: Optional[Site] = None
    cultivars: Optional[List[Cultivar]] = None
    plants: Optional[List[Plant]] = None

    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None

    @classmethod
    def create(
        cls,
        experiment_name: str = 'Default',
        season_name: str = 'Default',
        site_name: str = 'Default',
        plot_number: int = -1,
        plot_row_number: int = -1,
        plot_column_number: int = -1,
        plot_geometry_info: dict = {},
        plot_info: dict = {},
        cultivar_accession: str = 'Default',
        cultivar_population: str = 'Default',
    ):
        experiment = ExperimentModel.get_or_create(experiment_name=experiment_name) 
        season = SeasonModel.get_or_create(experiment_id=experiment.id, season_name=season_name)
        site = SiteModel.get_or_create(site_name=site_name)
        
        cultivar = CultivarModel.get_or_create(
            cultivar_population=cultivar_population,
            cultivar_accession=cultivar_accession,
        )
        
        new_instance = cls.db_model.get_or_create(
            plot_number=plot_number,
            plot_row_number=plot_row_number,
            plot_column_number=plot_column_number,
            plot_geometry_info=plot_geometry_info,
            plot_info=plot_info,
            experiment_id=experiment.id,
            season_id=season.id,
            site_id=site.id,
        )

        if cultivar is not None and cultivar not in new_instance.cultivars:
            new_instance.cultivars.append(cultivar)
            new_instance.save()

        logger_service.info(
            "API",
            f"Created a new plot with number {new_instance.plot_number} in the database",
        )

        new_instance = cls.model_validate(new_instance)
        return new_instance
    
    @classmethod
    def get(
        cls,
        plot_number: int,
        plot_row_number: int = None,
        plot_column_number: int = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None
    ):
        experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        season = SeasonModel.get_by_parameters(experiment_id=experiment.id, season_name=season_name)
        site = SiteModel.get_by_parameters(site_name=site_name)
        
        plot = PlotViewModel.get_by_parameters(
            plot_number=plot_number,
            plot_row_number=plot_row_number,
            plot_column_number=plot_column_number,
            experiment_id=experiment.id,
            season_id=season.id,
            site_id=site.id
        )
        plot = cls.model_validate(plot)
        return plot
    
    @classmethod
    def get_plots(
        cls,
        experiment_name: str,
        season_name: str = None,
        site_name: str = None
    ):
        experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        season = SeasonModel.get_by_parameters(experiment_id=experiment.id, season_name=season_name)
        site = SiteModel.get_by_parameters(site_name=site_name)

        plots = PlotViewModel.search(
            experiment_id=experiment.id,
            season_id=season.id,
            site_id=site.id
        )
        
        plots = [cls.model_validate(plot) for plot in plots]
        return plots
    
    @classmethod
    def get_cultivar_plots(
        cls,
        cultivar_population: str,
        cultivar_accession: str
    ):
        cultivar = CultivarModel.get_by_parameters(
            cultivar_population=cultivar_population,
            cultivar_accession=cultivar_accession
        )
        if not cultivar:
            return []
        plots = PlotCultivarViewModel.search(cultivar_id=cultivar.id)
        plots = [cls.model_validate(plot) for plot in plots]
        return plots
    
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved information about plot {self.plot_number} from the database",
        )
        return self.plot_info
    
    def set_info(self, plot_info: Optional[dict] = None) -> "Plot":
        self.update(plot_info=plot_info)
        logger_service.info(
            "API",
            f"Set information about plot {self.plot_number} in the database",
        )
        return self
    
    def add_info(self, plot_info: Optional[dict] = None) -> "Plot":
        current_info = self.get_info()
        updated_info = {**current_info, **plot_info}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Added information to plot {self.plot_number} in the database",
        )
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Plot":
        current_info = self.get_info()
        updated_info = {k: v for k, v in current_info.items() if k not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Removed information from plot {self.plot_number} in the database",
        )
        return self
    

    def get_geometry_info(self) -> dict:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved geometry information about plot {self.plot_number} from the database",
        )
        return self.plot_geometry_info
    
    def set_geometry_info(self, plot_geometry_info: Optional[dict] = None) -> "Plot":
        self.update(plot_geometry_info=plot_geometry_info)
        logger_service.info(
            "API",
            f"Set geometry information about plot {self.plot_number} in the database",
        )
        return self
    
    def get_experiment(self) -> Experiment:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved experiment of plot {self.plot_number} from the database",
        )
        return self.experiment
    
    def get_season(self) -> Season:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved season of plot {self.plot_number} from the database",
        )
        return self.season
    
    def get_site(self) -> Site:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved site of plot {self.plot_number} from the database",
        )
        return self.site
    
    def get_cultivars(self) -> List[Cultivar]:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved cultivars of plot {self.plot_number} from the database",
        )
        return self.cultivars
    
    def get_plants(self) -> List[Plant]:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved plants of plot {self.plot_number} from the database",
        )
        return self.plants
    
    @classmethod
    def search(cls, search_parameters: PlotSearchParameters) -> Generator["Plot", None, None]:
        plots = PlotViewModel.stream(**search_parameters.model_dump())
        for plot in plots:
            plot = cls.model_validate(plot)
            yield plot



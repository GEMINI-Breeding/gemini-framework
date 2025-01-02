from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
# from gemini.api.plot import Plot
from gemini.api.experiment import Experiment
from gemini.api.site import Site
from gemini.api.season import Season
from gemini.api.cultivar import Cultivar

from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.sites import SiteModel
from gemini.db.models.seasons import SeasonModel
from gemini.db.models.plants import PlantModel
from gemini.db.models.cultivars import CultivarModel
from gemini.db.models.plots import PlotModel

from gemini.db.models.views.plot_cultivar_view import PlotCultivarViewModel
from gemini.db.models.views.plot_view import PlotViewModel

class Plot(APIBase):


    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "plot_id"))
    experiment_id: ID
    season_id: ID
    site_id: ID
    plot_number: int
    plot_row_number: int
    plot_column_number: int
    plot_geometry_info: Optional[dict] = {}
    plot_info: Optional[dict] = {}
    
    experiment: Experiment = None
    season: Season = None
    site: Site = None

    cultivars: List[Cultivar] = []


    @classmethod
    def create(
        cls,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        plot_info: dict = {},
        experiment_name: str = "Default",
        season_name: str = "Default",
        site_name: str = "Default",
        cultivar_accession: str = "Default",
        cultivar_population: str = "Default",
    ) -> "Plot":
        try:
            experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
            site = SiteModel.get_by_parameters(site_name=site_name)
            season = SeasonModel.get_by_parameters(season_name=season_name)

            cultivar = CultivarModel.get_or_create(
                cultivar_accession=cultivar_accession,
                cultivar_population=cultivar_population,
            )

            plot = PlotModel.get_or_create(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                plot_info=plot_info,
                experiment_id=experiment.id,
                site_id=site.id,
                season_id=season.id,
            )

            if cultivar and cultivar not in plot.cultivars:
                plot.cultivars.append(cultivar)

            plot = cls.model_validate(plot)
            return plot
        except Exception as e:
            raise e
        

    @classmethod
    def get(
        cls,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
        experiment_name: str = "Default",
        season_name: str = "Default",
        site_name: str = "Default",
    ) -> List["Plot"]:
        try:
            plots = PlotViewModel.get_by_parameters(
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            plots = [cls.model_validate(plot) for plot in plots]
            return plots
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Plot":
        try:
            plot = PlotModel.get(id)
            plot = cls.model_validate(plot)
            return plot
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["Plot"]:
        try:
            plots = PlotModel.all()
            plots = [cls.model_validate(plot) for plot in plots]
            return plots
        except Exception as e:
            raise e
        

    @classmethod
    def search(cls, **search_parameters) -> List["Plot"]:
        try:
            plots = PlotModel.search(**search_parameters)
            plots = [cls.model_validate(plot) for plot in plots]
            return plots if plots else None
        except Exception as e:
            raise e
        

    def update(self, **kwargs) -> "Plot":
        try:
            curent_id = self.id
            plot = PlotModel.get(curent_id)
            plot = PlotModel.update(plot, **kwargs)
            plot = self.model_validate(plot)
            self.refresh()
            return plot
        except Exception as e:
            raise e
        

    def refresh(self) -> "Plot":
        try:
            db_instance = PlotModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    actual_value = getattr(instance, key)
                    setattr(self, key, actual_value)
            return self
        except Exception as e:
            raise e
        

    def delete(self) -> bool:
        try:
            current_id = self.id
            plot = PlotModel.get(current_id)
            PlotModel.delete(plot)
            return True
        except Exception as e:
            return False
        

    def get_cultivars(self) -> List["Cultivar"]:
        try:
            cultivars = [Cultivar.model_validate(cultivar) for cultivar in self.cultivars]
            return cultivars
        except Exception as e:
            raise e
        
    def get_experiment(self) -> "Experiment":
        try:
            experiment = Experiment.model_validate(self.experiment)
            return experiment
        except Exception as e:
            raise e
        
    def get_site(self) -> "Site":
        try:
            site = Site.model_validate(self.site)
            return site
        except Exception as e:
            raise e
                


        

from typing import Optional, List, Any
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

class PlotSearchParameters(BaseModel):
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None

class Plot(APIBase):

    db_model = PlotModel

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
        experiment_name: str,
        season_name: str,
        site_name: str,
        plot_number: int,
        plot_row_number: int = None,
        plot_column_number: int = None,
        plot_geometry_info: dict = None,
        plot_info: dict = None,
        cultivar_accession: str = None,
        cultivar_population: str = None,
    ):
        experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        season = SeasonModel.get_by_parameters(experiment_id=experiment.id, season_name=season_name)
        site = SiteModel.get_by_parameters(site_name=site_name)

        cultivar = CultivarModel.get_by_parameters(
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
    
    def search(cls, search_parameters: PlotSearchParameters) -> Generator["Plot", None, None]:
        plots = PlotViewModel.stream(**search_parameters.model_dump())
        for plot in plots:
            plot = cls.model_validate(plot)
            yield plot

    # Todo
    # Add plant and get plants for plot
    # Add experiment, season, site, cultivar to plot    


    




# from typing import Optional, List, Any
# from pydantic import Field
# from typing import Generator
# from gemini.api.base import APIBase
# from gemini.models import PlotModel, PlotViewModel
# from gemini.models import ExperimentModel, SiteModel, SeasonModel, CultivarModel
# from gemini.logger import logger_service

# import pandas as pd


# class Plot(APIBase):

#     db_model = PlotModel

#     plot_number: int
#     plot_row_number: Optional[int] = None
#     plot_column_number: Optional[int] = None
#     plot_geometry_info: Optional[dict] = None
#     plot_info: Optional[dict] = None

#     experiment: Optional[dict] = None
#     season: Optional[dict] = None
#     site: Optional[dict] = None
#     cultivars: Optional[List[dict]] = None

#     experiment_name: Optional[str] = None
#     season_name: Optional[str] = None
#     site_name: Optional[str] = None
#     cultivar_accession: Optional[str] = None
#     cultivar_population: Optional[str] = None

#     @classmethod
#     def create(
#         cls,
#         plot_number: int,
#         plot_row_number: int = None,
#         plot_column_number: int = None,
#         experiment_name: str = None,
#         season_name: str = None,
#         site_name: str = None,
#         cultivar_accession: str = None,
#         cultivar_population: str = None,
#         plot_geometry_info: dict = None,
#         plot_info: dict = None,
#     ):
#         """
#         Create a new plot

#         Args:
#         plot_number (int): The number of the plot
#         plot_row_number (int, optional): The row number of the plot. Defaults to None.
#         plot_column_number (int, optional): The column number of the plot. Defaults to None.
#         experiment_name (str, optional): The name of the experiment. Defaults to None.
#         season_name (str, optional): The name of the season. Defaults to None.
#         site_name (str, optional): The name of the site. Defaults to None.
#         cultivar_accession (str, optional): The accession of the cultivar. Defaults to None.
#         cultivar_population (str, optional): The population of the cultivar. Defaults to None.
#         plot_geometry_info (dict, optional): The geometry information of the plot. Defaults to None.
#         plot_info (dict, optional): The information about the plot. Defaults to None.

#         Returns:
#         Plot: The created plot
#         """

#         experiment = ExperimentModel.get_by_parameter(
#             "experiment_name", experiment_name
#         )
#         season = SeasonModel.get_by_parameters(
#             season_name=season_name,
#             experiment_id=experiment.id if experiment else None,
#         )
#         site = SiteModel.get_by_parameter("site_name", site_name)
#         cultivar = CultivarModel.get_or_create(
#             cultivar_population=cultivar_population,
#             cultivar_accession=cultivar_accession,
#         )

#         new_instance = cls.db_model.get_or_create(
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#             plot_geometry_info=plot_geometry_info,
#             plot_info=plot_info,
#             experiment_id=experiment.id if experiment else None,
#             season_id=season.id if season else None,
#             site_id=site.id if site else None,
#         )

#         if cultivar is not None and cultivar not in new_instance.cultivars:
#             new_instance.cultivars.append(cultivar)
#             new_instance.save()

#         logger_service.info(
#             "API",
#             f"Created a new plot with number {new_instance.plot_number} in the database",
#         )

#         new_instance = cls.model_validate(new_instance)
#         return new_instance

#     @classmethod
#     def get(
#         cls,
#         plot_number: int,
#         plot_row_number: int = None,
#         plot_column_number: int = None,
#         experiment_name: str = None,
#         season_name: str = None,
#         site_name: str = None,
#         plot_geometry_info: dict = None,
#         plot_info: dict = None,
#     ):
#         experiment = ExperimentModel.get_by_parameter(
#             "experiment_name", experiment_name
#         )
#         season = SeasonModel.get_by_parameters(
#             season_name=season_name,
#             experiment_id=experiment.id if experiment else None,
#         )
#         site = SiteModel.get_by_parameter("site_name", site_name)
        
#         plot = PlotViewModel.get_by_parameters(
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#             experiment_id=experiment.id if experiment else None,
#             season_id=season.id if season else None,
#             site_id=site.id if site else None,
#             plot_geometry_info=plot_geometry_info,
#             plot_info=plot_info,
#         )
#         plot = cls.model_validate(plot)
#         return plot





#     def get_experiment(self) -> dict:
#         """
#         Get the experiment of a plot

#         Returns:
#         Any: The experiment of the plot
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved experiment of plot {self.plot_number} from the database",
#         )
#         return self.experiment

#     def get_season(self) -> dict:
#         """
#         Get the season of a plot

#         Returns:
#         Any: The season of the plot
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved season of plot {self.plot_number} from the database",
#         )
#         return self.season

#     def get_site(self) -> dict:
#         """
#         Get the site of a plot

#         Returns:
#         Any: The site of the plot
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved site of plot {self.plot_number} from the database",
#         )
#         return self.site

#     def get_cultivars(self) -> List[dict]:
#         """
#         Get the cultivars of a plot

#         Returns:
#         List[Any]: The cultivars of the plot
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved cultivars of plot {self.plot_number} from the database",
#         )
#         return self.cultivars

#     def set_experiment(self, experiment_name: str) -> "Plot":
#         """
#         Set the experiment of a plot

#         Args:
#         experiment_name (str): The name of the experiment

#         Returns:
#         Plot: The plot with the updated experiment
#         """
#         experiment = ExperimentModel.get_by_parameter(
#             "experiment_name", experiment_name
#         )
#         self.update(experiment_id=experiment.id)
#         logger_service.info(
#             "API",
#             f"Set experiment of plot {self.plot_number} in the database",
#         )
#         return self

#     def set_season(self, season_name: str) -> "Plot":
#         """
#         Set the season of a plot

#         Args:
#         season_name (str): The name of the season

#         Returns:
#         Plot: The plot with the updated season
#         """
#         season = SeasonModel.get_by_parameters(
#             season_name=season_name, experiment_id=self.experiment.id
#         )
#         self.update(season_id=season.id)
#         logger_service.info(
#             "API",
#             f"Set season of plot {self.plot_number} in the database",
#         )
#         return self

#     def set_site(self, site_name: str) -> "Plot":
#         """
#         Set the site of a plot

#         Args:
#         site_name (str): The name of the site

#         Returns:
#         Plot: The plot with the updated site
#         """
#         site = SiteModel.get_by_parameter("site_name", site_name)
#         self.update(site_id=site.id)
#         logger_service.info(
#             "API",
#             f"Set site of plot {self.plot_number} in the database",
#         )
#         return self

#     def add_cultivar(self, cultivar_accession: str, cultivar_population: str) -> "Plot":
#         """
#         Add a cultivar to a plot

#         Args:
#         cultivar_accession (str): The accession of the cultivar
#         cultivar_population (str): The population of the cultivar

#         Returns:
#         Plot: The plot with the added cultivar
#         """
#         cultivar = CultivarModel.get_or_create(
#             cultivar_population=cultivar_population,
#             cultivar_accession=cultivar_accession,
#         )
#         plot = self.db_model.get_by_parameter("id", self.id)
#         if cultivar is not None and cultivar not in plot.cultivars:
#             plot.cultivars.append(cultivar)
#             plot.save()
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Added cultivar to plot {self.plot_number} in the database",
#         )
#         return self

#     def remove_cultivar(
#         self, cultivar_accession: str, cultivar_population: str
#     ) -> "Plot":
#         """
#         Remove a cultivar from a plot

#         Args:
#         cultivar_accession (str): The accession of the cultivar
#         cultivar_population (str): The population of the cultivar

#         Returns:
#         Plot: The plot with the removed cultivar
#         """
#         plot = self.db_model.get_by_parameter("id", self.id)
#         cultivar = CultivarModel.get_by_parameters(
#             cultivar_population=cultivar_population,
#             cultivar_accession=cultivar_accession,
#         )
#         if cultivar in plot.cultivars:
#             plot.cultivars.remove(cultivar)
#             plot.save()
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Removed cultivar from plot {self.plot_number} in the database",
#         )
#         return self

#     def set_geometry(self, plot_geometry_info: dict) -> "Plot":
#         """
#         Set the geometry information for a plot

#         Args:
#         plot_geometry_info (dict): The geometry information to set

#         Returns:
#         Plot: The plot with the updated geometry information
#         """
#         self.update(plot_geometry_info=plot_geometry_info)
#         logger_service.info(
#             "API",
#             f"Set geometry information for plot {self.plot_number} in the database",
#         )
#         return self

#     def get_geometry(self) -> dict:
#         """
#         Get the geometry information for a plot

#         Returns:
#         dict: The geometry information for the plot
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved geometry information for plot {self.plot_number} from the database",
#         )
#         return self.plot_geometry_info

#     def set_info(self, plot_info: dict) -> "Plot":
#         """
#         Set the information for a plot

#         Args:
#         plot_info (dict): The information to set

#         Returns:
#         Plot: The plot with the updated information
#         """
#         self.update(plot_info=plot_info)
#         logger_service.info(
#             "API",
#             f"Set information for plot {self.plot_number} in the database",
#         )
#         return self

#     def get_info(self) -> dict:
#         """
#         Get the information for a plot

#         Returns:
#         dict: The information for the plot
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved information for plot {self.plot_number} from the database",
#         )
#         return self.plot_info

#     def add_info(self, plot_info: dict) -> "Plot":
#         """
#         Add information to a plot

#         Args:
#         plot_info (dict): The information to add

#         Returns:
#         Plot: The plot with the added information
#         """
#         current_info = self.get_info()
#         updated_info = {**current_info, **plot_info}
#         self.set_info(updated_info)
#         logger_service.info(
#             "API",
#             f"Added information to plot {self.plot_number} in the database",
#         )
#         return self

#     def remove_info(self, keys_to_remove: List[str]) -> "Plot":
#         """
#         Remove information from a plot

#         Args:
#         keys_to_remove (List[str]): The keys to remove

#         Returns:
#         Plot: The plot with the removed information
#         """
#         current_info = self.get_info()
#         updated_info = {
#             key: value
#             for key, value in current_info.items()
#             if key not in keys_to_remove
#         }
#         self.set_info(updated_info)
#         logger_service.info(
#             "API",
#             f"Removed information from plot {self.plot_number} in the database",
#         )
#         return self

#     @classmethod
#     def search(cls, **search_params) -> Generator["Plot", None, None]:
#         """
#         Search for plots in the database

#         Args:
#         search_params (dict): The parameters to search by

#         Returns:
#         List[Plot]: A list of plots that match the search parameters
#         """
#         plots = PlotViewModel.stream(**search_params)
#         for plot in plots:
#             plot = cls.model_validate(plot.to_dict())
#             yield plot

    

# # Todo: Add plant and get plants for plot

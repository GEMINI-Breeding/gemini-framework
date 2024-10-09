from typing import Optional, List, Any, Union
from pydantic import Field, BaseModel, AliasChoices
from typing import Generator
from gemini.api.base import APIBase
from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site
from gemini.api.cultivar import Cultivar
from gemini.server.database.models import PlotModel, PlotViewModel, PlotCultivarViewModel
from gemini.server.database.models import ExperimentModel, SiteModel, SeasonModel, CultivarModel


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
        """
        Create a new plot instance.

        Args:
            experiment_name (str, optional): Name of the experiment. Defaults to 'Default'.
            season_name (str, optional): Name of the season. Defaults to 'Default'.
            site_name (str, optional): Name of the site. Defaults to 'Default'.
            plot_number (int, optional): Plot number. Defaults to -1.
            plot_row_number (int, optional): Plot row number. Defaults to -1.
            plot_column_number (int, optional): Plot column number. Defaults to -1.
            plot_geometry_info (dict, optional): Plot geometry information. Defaults to {}.
            plot_info (dict, optional): Plot information. Defaults to {}.
            cultivar_accession (str, optional): Cultivar accession. Defaults to 'Default'.
            cultivar_population (str, optional): Cultivar population. Defaults to 'Default'.

        Returns:
            Plot: The newly created plot instance.
        """
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
        """
        Get a plot instance by its parameters.

        Args:
            plot_number (int): Plot number.
            plot_row_number (int, optional): Plot row number. Defaults to None.
            plot_column_number (int, optional): Plot column number. Defaults to None.
            experiment_name (str, optional): Name of the experiment. Defaults to None.
            season_name (str, optional): Name of the season. Defaults to None.
            site_name (str, optional): Name of the site. Defaults to None.

        Returns:
            Plot: The plot instance matching the given parameters.
        """
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
        """
        Get all plots for a specific experiment, season, and site.

        Args:
            experiment_name (str): Name of the experiment.
            season_name (str, optional): Name of the season. Defaults to None.
            site_name (str, optional): Name of the site. Defaults to None.

        Returns:
            List[Plot]: List of plot instances matching the given parameters.
        """
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
        """
        Get all plots for a specific cultivar.

        Args:
            cultivar_population (str): Cultivar population.
            cultivar_accession (str): Cultivar accession.

        Returns:
            List[Plot]: List of plot instances for the given cultivar.
        """
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
        """
        Get the plot information.

        Returns:
            dict: The plot information.
        """
        self.refresh()
        return self.plot_info
    
    def set_info(self, plot_info: Optional[dict] = None) -> "Plot":
        """
        Set the plot information.

        Args:
            plot_info (dict, optional): The plot information. Defaults to None.

        Returns:
            Plot: The updated plot instance.
        """
        self.update(plot_info=plot_info)
        return self
    
    def add_info(self, plot_info: Optional[dict] = None) -> "Plot":
        """
        Add additional information to the plot.

        Args:
            plot_info (dict, optional): Additional plot information. Defaults to None.

        Returns:
            Plot: The updated plot instance.
        """
        current_info = self.get_info()
        updated_info = {**current_info, **plot_info}
        self.set_info(updated_info)
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Plot":
        """
        Remove specific keys from the plot information.

        Args:
            keys_to_remove (List[str]): List of keys to remove from the plot information.

        Returns:
            Plot: The updated plot instance.
        """
        current_info = self.get_info()
        updated_info = {k: v for k, v in current_info.items() if k not in keys_to_remove}
        self.set_info(updated_info)
        return self
    

    def get_geometry_info(self) -> dict:
        """
        Get the plot geometry information.

        Returns:
            dict: The plot geometry information.
        """
        self.refresh()
        return self.plot_geometry_info
    
    def set_geometry_info(self, plot_geometry_info: Optional[dict] = None) -> "Plot":
        """
        Set the plot geometry information.

        Args:
            plot_geometry_info (dict, optional): The plot geometry information. Defaults to None.

        Returns:
            Plot: The updated plot instance.
        """
        self.update(plot_geometry_info=plot_geometry_info)
        return self
    
    def get_experiment(self) -> Experiment:
        """
        Get the experiment associated with the plot.

        Returns:
            Experiment: The experiment instance.
        """
        self.refresh()
        return self.experiment
    
    def get_season(self) -> Season:
        """
        Get the season associated with the plot.

        Returns:
            Season: The season instance.
        """
        self.refresh()
        return self.season
    
    def get_site(self) -> Site:
        """
        Get the site associated with the plot.

        Returns:
            Site: The site instance.
        """
        self.refresh()
        return self.site
    
    def get_cultivars(self) -> List[Cultivar]:
        """
        Get the cultivars associated with the plot.

        Returns:
            List[Cultivar]: List of cultivar instances.
        """
        self.refresh()
        return self.cultivars

    
    @classmethod
    def search(cls, search_parameters: PlotSearchParameters) -> Generator["Plot", None, None]:
        """
        Search for plots based on the given search parameters.

        Args:
            search_parameters (PlotSearchParameters): The search parameters.

        Yields:
            Plot: The plot instances matching the search parameters.
        """
        plots = PlotViewModel.stream(**search_parameters.model_dump())
        for plot in plots:
            plot = cls.model_validate(plot)
            yield plot


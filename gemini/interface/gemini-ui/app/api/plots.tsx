import {isLocal, flaskConfig} from "@/api.config";
import {Plot, Experiment, Season, Site, Cultivar} from "../types";



// Get Plots
async function getPlots(params?: object): Promise<Plot[]> {
    try{
        const queryString = new URLSearchParams(params as Record<string, string>).toString();
        const response = await fetch(`${flaskConfig.baseURL}/plots?${queryString}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/ndjson',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;

    } catch (error) {
        console.log("Error in getPlots: ", error);
        return [];
    }
}

async function testAPI() {
    getPlots().then((data) => {
        console.log("Data: ", data);
    });
}

testAPI();

// class PlotController(Controller):
    
//     # Get Plots
//     @get()
//     async def get_plots(
//         self,
//         experiment_name: Optional[str] = None,
//         season_name: Optional[str] = None,
//         site_name: Optional[str] = None,
//         plot_number: Optional[int] = None,
//         plot_row_number: Optional[int] = None,
//         plot_column_number: Optional[int] = None,
//         plot_geometry_info: Optional[dict] = None,
//         plot_info: Optional[dict] = None
//     ) -> Stream:
//         try:
//             plot_search_parameters = PlotSearch(
//                 experiment_name=experiment_name,
//                 season_name=season_name,
//                 site_name=site_name,
//                 plot_number=plot_number,
//                 plot_row_number=plot_row_number,
//                 plot_column_number=plot_column_number,
//                 plot_geometry_info=plot_geometry_info,
//                 plot_info=plot_info
//             )
//             return Stream(plot_search_generator(plot_search_parameters))
//         except Exception as e:
//             return Response(content=str(e), status_code=500)
    
//     # Create a plot
//     @post()
//     async def create_plot(
//         self,
//         data: Annotated[PlotInput, Body]
//     ) -> PlotOutput:
//         try:
//             plot = Plot.create(
//                 experiment_name=data.experiment_name,
//                 season_name=data.season_name,
//                 site_name=data.site_name,
//                 plot_number=data.plot_number,
//                 plot_row_number=data.plot_row_number,
//                 plot_column_number=data.plot_column_number,
//                 plot_geometry_info=data.plot_geometry_info,
//                 plot_info=data.plot_info,
//                 cultivar_accession=data.cultivar_accession,
//                 cultivar_population=data.cultivar_population
//             )
//             if not plot:
//                 return Response(status_code=400)
//             plot = plot.model_dump()
//             return PlotOutput.model_validate(plot)
//         except Exception as e:
//             return Response(content=str(e), status_code=500)
        
//     # Get Plots given experiment, season and site
//     @get('/experiment/{experiment_name:str}/season/{season_name:str}/site/{site_name:str}')
//     async def get_plots_by_experiment_season_site(
//         self,
//         experiment_name: str,
//         season_name: str,
//         site_name: str
//     ) -> List[PlotOutput]:
//         try:
//             plots = Plot.get_plots(
//                 experiment_name=experiment_name,
//                 season_name=season_name,
//                 site_name=site_name
//             )
//             plots = [plot.model_dump(exclude_none=True) for plot in plots]
//             plots = [PlotOutput.model_validate(plot) for plot in plots]
//             return plots
//         except Exception as e:
//             return Response(content=str(e), status_code=500)
        
//     # Get Plots given cultivar population and accession
//     @get('/cultivar/{cultivar_population:str}/{cultivar_accession:str}')
//     async def get_plots_by_cultivar(
//         self,
//         cultivar_population: str,
//         cultivar_accession: str
//     ) -> List[PlotOutput]:
//         try:
//             plots = Plot.get_cultivar_plots(
//                 cultivar_population=cultivar_population,
//                 cultivar_accession=cultivar_accession
//             )
//             plots = [plot.model_dump(exclude_none=True) for plot in plots]
//             plots = [PlotOutput.model_validate(plot) for plot in plots]
//             return plots
//         except Exception as e:
//             return Response(content=str(e), status_code=500)


//     # Get Plot Info by plot ID
//     @get('/{plot_id:str}/info')
//     async def get_plot_info(
//         self,
//         plot_id: str
//     ) -> dict:
//         try:
//             plot = Plot.get_by_id(plot_id)
//             if not plot:
//                 return Response(status_code=404)
//             return plot.get_info()
//         except Exception as e:
//             return Response(content=str(e), status_code=500)
        
//     # Set Plot Info by plot ID
//     @patch('/{plot_id:str}/info')
//     async def set_plot_info(
//         self,
//         plot_id: str,
//         data: dict
//     ) -> dict:
//         try:
//             plot = Plot.get_by_id(plot_id)
//             if not plot:
//                 return Response(status_code=404)
//             plot.set_info(data)
//             return plot.get_info()
//         except Exception as e:
//             return Response(content=str(e), status_code=500)
        
//     # Get Plot Geometry Info by plot ID
//     @get('/{plot_id:str}/geometry')
//     async def get_plot_geometry_info(
//         self,
//         plot_id: str
//     ) -> dict:
//         try:
//             plot = Plot.get_by_id(plot_id)
//             if not plot:
//                 return Response(status_code=404)
//             return plot.get_geometry_info()
//         except Exception as e:
//             return Response(content=str(e), status_code=500)
        
//     # Set Plot Geometry Info by plot ID
//     @patch('/{plot_id:str}/geometry')
//     async def set_plot_geometry_info(
//         self,
//         plot_id: str,
//         data: dict
//     ) -> dict:
//         try:
//             plot = Plot.get_by_id(plot_id)
//             if not plot:
//                 return Response(status_code=404)
//             plot.set_geometry_info(data)
//             return plot.get_geometry_info()
//         except Exception as e:
//             return Response(content=str(e), status_code=500)
        
    
        
//     # Delete Plot by plot ID
//     @delete('/{plot_id:str}')
//     async def delete_plot(
//         self,
//         plot_id: str
//     ) -> None:
//         try:
//             plot = Plot.get_by_id(plot_id)
//             if not plot:
//                 return Response(status_code=404)
//             plot.delete()
//         except Exception as e:
//             return Response(content=str(e), status_code=500)
        
//     # Get Plot Experiment by plot ID
//     @get('/{plot_id:str}/experiment')
//     async def get_plot_experiment(
//         self,
//         plot_id: str
//     ) -> ExperimentOutput:
//         try:
//             plot = Plot.get_by_id(plot_id)
//             if not plot:
//                 return Response(status_code=404)
//             experiment = plot.get_experiment()
//             experiment = experiment.model_dump(exclude_none=True)
//             return ExperimentOutput.model_validate(experiment)
//         except Exception as e:
//             return Response(content=str(e), status_code=500)
        
//     # Get Plot Season by plot ID
//     @get('/{plot_id:str}/season')
//     async def get_plot_season(
//         self,
//         plot_id: str
//     ) -> SeasonOutput:
//         try:
//             plot = Plot.get_by_id(plot_id)
//             if not plot:
//                 return Response(status_code=404)
//             season = plot.get_season()
//             season = season.model_dump(exclude_none=True)
//             return SeasonOutput.model_validate(season)
//         except Exception as e:
//             return Response(content=str(e), status_code=500)
        
//     # Get Plot Site by plot ID
//     @get('/{plot_id:str}/site')
//     async def get_plot_site(
//         self,
//         plot_id: str
//     ) -> SiteOutput:
//         try:
//             plot = Plot.get_by_id(plot_id)
//             if not plot:
//                 return Response(status_code=404)
//             site = plot.get_site()
//             site = site.model_dump(exclude_none=True)
//             return SiteOutput.model_validate(site)
//         except Exception as e:
//             return Response(content=str(e), status_code=500)
        
//     # Get Plot Cultivars by plot ID
//     @get('/{plot_id:str}/cultivars')
//     async def get_plot_cultivars(
//         self,
//         plot_id: str
//     ) -> List[CultivarOutput]:
//         try:
//             plot = Plot.get_by_id(plot_id)
//             if not plot:
//                 return Response(status_code=404)
//             cultivars = plot.get_cultivars()
//             cultivars = [cultivar.model_dump(exclude_none=True) for cultivar in cultivars]
//             cultivars = [CultivarOutput.model_validate(cultivar) for cultivar in cultivars]
//             return cultivars
//         except Exception as e:
//             return Response(content=str(e), status_code=500)

//     # Todo: Set Plot Number, Row Number, Column Number by plot ID

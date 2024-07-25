import {apiConfig} from "@/api/config";
import { Plot, Season, Site, Cultivar, Experiment } from "@/api/types";

// Create a plot
async function createPlot(params?: object): Promise<Plot[]> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/plots`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json() as Plot[];

    } catch (error) {
        console.log("Error in createPlot: ", error);
        return {} as Plot[];
    }
}

// Get Plots given experiment, season and site
async function getPlotsByExperimentSeasonSite(experimentName: string, seasonName: string, siteName: string): Promise<Plot[]> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/plots/experiment/${experimentName}/season/${seasonName}/site/${siteName}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json() as Plot[];

    } catch (error) {
        console.log("Error in getPlotsByExperimentSeasonSite: ", error);
        return [] as Plot[];
    }
}


// Get Plots given cultivar population and accession
async function getPlotsByCultivar(cultivarPopulation: string, cultivarAccession: string): Promise<Plot[]> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/plots/cultivar/${cultivarPopulation}/${cultivarAccession}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json() as Plot[];

    } catch (error) {
        console.log("Error in getPlotsByCultivar: ", error);
        return [] as Plot[];
    }
}


// Get Plot Info by plot ID
async function getPlotInfo(plotId: string): Promise<object> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/plots/${plotId}/info`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json() as object;

    } catch (error) {
        console.log("Error in getPlotInfo: ", error);
        return {} as object;
    }
}


// Set Plot Info by plot ID
async function setPlotInfo(plotId: string, data: object): Promise<object> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/plots/${plotId}/info`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json() as object;

    } catch (error) {
        console.log("Error in setPlotInfo: ", error);
        return {} as object;
    }
}


// Get Plot Geometry Info by plot ID
async function getPlotGeometryInfo(plotId: string): Promise<object> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/plots/${plotId}/geometry`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json() as object;

    } catch (error) {
        console.log("Error in getPlotGeometryInfo: ", error);
        return {} as object;
    }
}


// Set Plot Geometry Info by plot ID
async function setPlotGeometryInfo(plotId: string, data: object): Promise<object> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/plots/${plotId}/geometry`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json() as object;

    } catch (error) {
        console.log("Error in setPlotGeometryInfo: ", error);
        return {} as object;
    }
}


// Delete Plot by plot ID
async function deletePlot(plotId: string): Promise<void> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/plots/${plotId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

    } catch (error) {
        console.log("Error in deletePlot: ", error);
    }
}


// Get Plot Experiment by plot ID
async function getPlotExperiment(plotId: string): Promise<Experiment> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/plots/${plotId}/experiment`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json() as Experiment;

    } catch (error) {
        console.log("Error in getPlotExperiment: ", error);
        return {} as Experiment;
    }
}


// Get Plot Season by plot ID
async function getPlotSeason(plotId: string): Promise<Season> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/plots/${plotId}/season`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json() as Season;

    } catch (error) {
        console.log("Error in getPlotSeason: ", error);
        return {} as Season;
    }
}


// Get Plot Site by plot ID
async function getPlotSite(plotId: string): Promise<Site> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/plots/${plotId}/site`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json() as Site;

    } catch (error) {
        console.log("Error in getPlotSite: ", error);
        return {} as Site;
    }
}


// Get Plot Cultivars by plot ID
async function getPlotCultivars(plotId: string): Promise<Cultivar[]> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/plots/${plotId}/cultivars`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json() as Cultivar[];

    } catch (error) {
        console.log("Error in getPlotCultivars: ", error);
        return [] as Cultivar[];
    }
}


export default {
    // getPlots,
    createPlot,
    getPlotsByExperimentSeasonSite,
    getPlotsByCultivar,
    getPlotInfo,
    setPlotInfo,
    getPlotGeometryInfo,
    setPlotGeometryInfo,
    deletePlot,
    getPlotExperiment,
    getPlotSeason,
    getPlotSite,
    getPlotCultivars
}

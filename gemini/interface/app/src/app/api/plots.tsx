import { apiSettings } from "./settings";

interface PlotSearchIndex {
    experiment_name: string;
    season_name: string;
    site_name: string;
    plot_number: number;
    plot_row_number: number;
    plot_column_number: number;
    plot_geometry_info: object;
    plot_info: object;
    cultivar_accession: string;
    cultivar_population: string;
}


// Get all plots
async function getAllPlots() {
    const response = await fetch(`${apiSettings.apiEndpoint}plots/all`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get plots for experiment and season
async function getExperimentPlots(experiment_name: string, season_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}plots/${experiment_name}/${season_name}`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get plots for a site
async function getSitePlots(site_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}plots/site/${site_name}`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Create a plot
async function createPlot(
    experiment_name: string,
    season_name: string,
    site_name: string,
    plot_number: number,
    plot_row_number: number,
    plot_column_number: number,
    plot_geometry_info: object,
    plot_info: object,
    cultivar_accession: string,
    cultivar_population: string
) {
    const response = await fetch(`${apiSettings.apiEndpoint}plots`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            experiment_name: experiment_name,
            season_name: season_name,
            site_name: site_name,
            plot_number: plot_number,
            plot_row_number: plot_row_number,
            plot_column_number: plot_column_number,
            plot_geometry_info: plot_geometry_info,
            plot_info: plot_info,
            cultivar_accession: cultivar_accession,
            cultivar_population: cultivar_population
        }),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}


// Search for plots
async function searchPlots(search_index: PlotSearchIndex) {
    const response = await fetch(`${apiSettings.apiEndpoint}plots/search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(search_index),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Set Plot Geometry Info
async function setPlotGeometry(search_index: PlotSearchIndex, plot_geometry_info: object) {
    const response = await fetch(`${apiSettings.apiEndpoint}plots/geometry`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            search_index: search_index,
            plot_geometry_info: plot_geometry_info
        }),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Set Plot Info
async function setPlotInfo(search_index: PlotSearchIndex, plot_info: object) {
    const response = await fetch(`${apiSettings.apiEndpoint}plots/info`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            search_index: search_index,
            plot_info: plot_info
        }),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Add a cultivar to a plot
async function addCultivarToPlot(search_index: PlotSearchIndex, cultivar_accession: string, cultivar_population: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}plots/cultivar`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            search_index: search_index,
            cultivar_accession: cultivar_accession,
            cultivar_population: cultivar_population
        }),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Change Plot Experiment
async function changePlotExperiment(search_index: PlotSearchIndex, experiment_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}plots/experiment`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            search_index: search_index,
            experiment_name: experiment_name
        }),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}


// Change Plot Season
async function changePlotSeason(search_index: PlotSearchIndex, season_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}plots/season`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            search_index: search_index,
            season_name: season_name
        }),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Change Plot Site
async function changePlotSite(search_index: PlotSearchIndex, site_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}plots/site`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            search_index: search_index,
            site_name: site_name
        }),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
} 


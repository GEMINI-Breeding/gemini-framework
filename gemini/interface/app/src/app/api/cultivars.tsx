import { apiSettings } from "./settings";

// Get all cultivars
async function getAllCultivars() {
    const response = await fetch(`${apiSettings.apiEndpoint}cultivars/all`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get cultivar by accession and population names
async function getCultivar(accession_name: string, population_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}cultivars/${population_name}/${accession_name}`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Create a cultivar
async function createCultivar(accession_name: string, population_name: string, cultivar_info: object, experiment_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}cultivars`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            accession_name: accession_name,
            population_name: population_name,
            cultivar_info: cultivar_info,
            experiment_name: experiment_name
        }),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Delete a cultivar
async function deleteCultivar(accession_name: string, population_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}cultivars/${population_name}/${accession_name}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Set Cultivar Info
async function setCultivarInfo(accession_name: string, population_name: string, info: object) {
    const response = await fetch(`${apiSettings.apiEndpoint}cultivars/${population_name}/${accession_name}/info`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(info),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get Cultivar Accessions for a population
async function getCultivarAccessions(population_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}cultivars/${population_name}/accessions`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Search Cultivars
async function searchCultivars(data: any) {
    const response = await fetch(`${apiSettings.apiEndpoint}cultivars/search?${new URLSearchParams(data)}`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get Experiments in which this cultivar is present
async function getExperimentsByCultivar(accession_name: string, population_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}cultivars/${population_name}/${accession_name}/experiments`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get plots in which this cultivar is present
async function getPlotsByCultivar(accession_name: string, population_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}cultivars/${population_name}/${accession_name}/plots`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

const cultivarAPI = {
    getAllCultivars,
    getCultivar,
    createCultivar,
    deleteCultivar,
    setCultivarInfo,
    getCultivarAccessions,
    searchCultivars,
    getExperimentsByCultivar,
    getPlotsByCultivar
};
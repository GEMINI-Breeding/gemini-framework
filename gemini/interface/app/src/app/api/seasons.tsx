import { apiSettings } from "./settings";

// Get all seasons
async function getAllSeasons() {
    const response = await fetch(`${apiSettings.apiEndpoint}seasons/all`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get Season by experiment name and season name
async function getSeason(experiment_name: string, season_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}seasons/${experiment_name}/${season_name}`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get all seasons belonging to an experiment
async function getExperimentSeasons(experiment_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}seasons/experiment/${experiment_name}`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Create a season for an experiment
async function createSeason(experiment_name: string, season_name: string, season_start_date: string, season_end_date: string, season_info: object) {
    const response = await fetch(`${apiSettings.apiEndpoint}seasons`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            experiment_name: experiment_name,
            season_name: season_name,
            season_start_date: season_start_date,
            season_end_date: season_end_date,
            season_info: season_info,
        }),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Update a season for an experiment
async function updateSeason(experiment_name: string, season_name: string, updated_data: object) {
    const response = await fetch(`${apiSettings.apiEndpoint}seasons/${experiment_name}/${season_name}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updated_data),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Delete a season for an experiment
async function deleteSeason(experiment_name: string, season_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}seasons/${experiment_name}/${season_name}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Set Season Info
async function setSeasonInfo(experiment_name: string, season_name: string, info: object) {
    const response = await fetch(`${apiSettings.apiEndpoint}seasons/${experiment_name}/${season_name}/info`, {
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

// Search Seasons
async function searchSeasons(data: any) {
    const response = await fetch(`${apiSettings.apiEndpoint}seasons/search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

const seasonAPI = {
    getAllSeasons,
    getSeason,
    getExperimentSeasons,
    createSeason,
    updateSeason,
    deleteSeason,
    setSeasonInfo,
    searchSeasons,
};

export default seasonAPI;
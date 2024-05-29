import { apiSettings } from "./settings";

// Get all experiments
async function getAllExperiments() {
    const response = await fetch(`${apiSettings.apiEndpoint}experiments/all`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get experiment by name
async function getExperiment(experiment_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}experiments/${experiment_name}`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Create Experiment
async function createExperiment(experiment_name: string, experiment_start_date: string, experiment_end_date: string, experiment_info: object) {
    const response = await fetch(`${apiSettings.apiEndpoint}experiments`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            experiment_name: experiment_name,
            experiment_start_date: experiment_start_date,
            experiment_end_date: experiment_end_date,
            experiment_info: experiment_info,
        }),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Update Experiment by name
async function updateExperiment(experiment_name: string, updated_data: object) {
    const response = await fetch(`${apiSettings.apiEndpoint}experiments/${experiment_name}`, {
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

// Delete Experiment by name
async function deleteExperiment(experiment_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}experiments/${experiment_name}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Search Experiments
async function searchExperiments(data: any) {
    const response = await fetch(`${apiSettings.apiEndpoint}experiments/search`, {
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

// Set experiment Info
async function setExperimentInfo(experiment_name: string, info: object) {
    const response = await fetch(`${apiSettings.apiEndpoint}experiments/${experiment_name}/info`, {
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

// Get Experiment Seasons by experiment name
async function getExperimentSeasons(experiment_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}experiments/${experiment_name}/seasons`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get Experiment Sites
async function getExperimentSites(experiment_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}experiments/${experiment_name}/sites`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get Experiment Traits
async function getExperimentTraits(experiment_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}experiments/${experiment_name}/traits`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get Experiment Sensors
async function getExperimentSensors(experiment_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}experiments/${experiment_name}/sensors`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get Experiment Cultivars
async function getExperimentCultivars(experiment_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}experiments/${experiment_name}/cultivars`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

const experimentAPI = {
    getAllExperiments,
    getExperiment,
    createExperiment,
    updateExperiment,
    deleteExperiment,
    searchExperiments,
    setExperimentInfo,
    getExperimentSeasons,
    getExperimentSites,
    getExperimentTraits,
    getExperimentSensors,
    getExperimentCultivars,
};

export default experimentAPI;
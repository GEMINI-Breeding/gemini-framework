import { isLocal, flaskConfig } from "../api.config";
import { Experiment, Season, Site, Sensor, Trait, Cultivar, Resource, Dataset } from "./types";

// Get Experiments
async function getExperiments(params?:object) : Promise<Experiment[]> {
    try {
        const queryString = new URLSearchParams(params as Record<string, string>).toString();
        const response = await fetch(`${flaskConfig.baseURL}/experiments?${queryString}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            console.log(response.statusText);
            return [];
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.log("Error in getExperiments: ", error);
        return [];
    }
}

// Create Experiment
async function createExperiment(params?:object) : Promise<Experiment> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/experiments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params)
        });
        if (!response.ok) {
            console.log(response.statusText);
            return {} as Experiment;
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.log("Error in createExperiment: ", error);
        return {} as Experiment;
    }
}

// Get Experiment By Experiment Name
async function getExperiment(experimentName:string) : Promise<Experiment> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/experiments/${experimentName}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            console.log(response.statusText);
            return {} as Experiment;
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.log("Error in getExperimentByName: ", error);
        return {} as Experiment;
    }
}

// Get Experiment Info By Experiment Name
async function getExperimentInfo(experimentName:string) : Promise<object> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/experiments/${experimentName}/info`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            console.log(response.statusText);
            return {};
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.log("Error in getExperimentInfoByName: ", error);
        return {};
    }
}

// Set Experiment Info By Experiment Name
async function setExperimentInfo(experimentName:string, params:object) : Promise<object> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/experiments/${experimentName}/info`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params)
        });
        if (!response.ok) {
            console.log(response.statusText);
            return {};
        }
        const data = await response.json();
        return data;
    }
    catch (error) {
        console.log("Error in setExperimentInfoByName: ", error);
        return {};
    }
}


// Get Experiment Seasons By Experiment Name
async function getExperimentSeasons(experimentName:string) : Promise<Season[]> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/experiments/${experimentName}/seasons`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            console.log(response.statusText);
            return [];
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.log("Error in getExperimentSeasonsByName: ", error);
        return [];
    }
}

// Get Experiment Sites By Experiment Name
async function getExperimentSites(experimentName:string) : Promise<Site[]> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/experiments/${experimentName}/sites`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            console.log(response.statusText);
            return [];
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.log("Error in getExperimentSitesByName: ", error);
        return [];
    }
}

// Get Experiment Cultivars By Experiment Name
async function getExperimentCultivars(experimentName:string) : Promise<Cultivar[]> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/experiments/${experimentName}/cultivars`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            console.log(response.statusText);
            return [];
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.log("Error in getExperimentCultivarsByName: ", error);
        return [];
    }
}

// Get Experiment Traits By Experiment Name
async function getExperimentTraits(experimentName:string) : Promise<Trait[]> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/experiments/${experimentName}/traits`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            console.log(response.statusText);
            return [];
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.log("Error in getExperimentTraitsByName: ", error);
        return [];
    }
}

// Get Experiment Sensors By Experiment Name
async function getExperimentSensors(experimentName:string) : Promise<Sensor[]> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/experiments/${experimentName}/sensors`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            console.log(response.statusText);
            return [];
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.log("Error in getExperimentSensorsByName: ", error);
        return [];
    }
}

// Get Experiment Resources By Experiment Name
async function getExperimentResources(experimentName:string) : Promise<Resource[]> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/experiments/${experimentName}/resources`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            console.log(response.statusText);
            return [];
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.log("Error in getExperimentResourcesByName: ", error);
        return [];
    }
}

// Get Experiment Datasets By Experiment Name
async function getExperimentDatasets(experimentName:string) : Promise<Dataset[]> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/experiments/${experimentName}/datasets`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            console.log(response.statusText);
            return [];
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.log("Error in getExperimentDatasetsByName: ", error);
        return [];
    }
}


export default {
    getExperiments,
    createExperiment,
    getExperiment,
    getExperimentInfo,
    setExperimentInfo,
    getExperimentSeasons,
    getExperimentSites,
    getExperimentCultivars,
    getExperimentTraits,
    getExperimentSensors,
    getExperimentResources,
    getExperimentDatasets
}

import { isLocal, flaskConfig } from '@/api.config';
import { Sensor, Dataset } from "../types"

// Get Sensors
async function getSensors(params?: object): Promise<Sensor[]> {
    try {
        const queryString = new URLSearchParams(params as Record<string, string>).toString();
        const response = await fetch(`${flaskConfig.baseURL}/sensors?${queryString}`, {
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
    }
    catch (error) {
        console.log("Error in getSensors: ", error);
        return [];
    }
}

// Create Sensor
async function createSensor(params?: object): Promise<Sensor> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/sensors`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params)
        });
        if (!response.ok) {
            console.log(response.statusText);
            return {} as Sensor;
        }
        const data = await response.json();
        return data;
    }
    catch (error) {
        console.log("Error in createSensor: ", error);
        return {} as Sensor;
    }
}

// Get Sensor by Sensor Name
async function getSensor(sensor_name: string): Promise<Sensor> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/sensors/${sensor_name}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            console.log(response.statusText);
            return {} as Sensor;
        }
        const data = await response.json();
        return data;
    }
    catch (error) {
        console.log("Error in getSensor: ", error);
        return {} as Sensor;
    }
}

// Get Sensor Info by Sensor Name
async function getSensorInfo(sensor_name: string): Promise<object> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/sensors/${sensor_name}/info`, {
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
    }
    catch (error) {
        console.log("Error in getSensorInfo: ", error);
        return {};
    }
}

// Set Sensor Info by Sensor Name
async function setSensorInfo(sensor_name: string, params: object): Promise<object> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/sensors/${sensor_name}/info`, {
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
        console.log("Error in setSensorInfo: ", error);
        return {};
    }
}

// Get Sensor Datasets
async function getSensorDatasets(sensor_name: string): Promise<Dataset[]> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/sensors/${sensor_name}/datasets`, {
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
    }
    catch (error) {
        console.log("Error in getSensorDatasets: ", error);
        return [];
    }
}


export default {
    getSensors,
    createSensor,
    getSensor,
    getSensorInfo,
    setSensorInfo,
    getSensorDatasets
}


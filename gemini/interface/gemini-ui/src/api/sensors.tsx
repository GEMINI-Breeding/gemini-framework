import { apiConfig } from "@/api/config";
import { Sensor, Dataset } from "@/api/types";

// Get Sensors
async function getSensors(params?: object): Promise<Sensor[]> {
    try {
        const queryString = new URLSearchParams(params as Record<string, string>).toString();
        const url = `${apiConfig.baseURL}/sensors?${queryString}`;
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            cache: 'no-store'
        });
        if (!response.ok) {
            console.log(response.statusText);
            return [] as Sensor[];
        }
        const data = await response.json();
        return data as Sensor[];
    }
    catch (error) {
        console.log("Error in getSensors: ", error);
        return [] as Sensor[];
    }
}

// Create Sensor
async function createSensor(params?: object): Promise<Sensor> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/sensors`, {
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
        return data as Sensor;
    }
    catch (error) {
        console.log("Error in createSensor: ", error);
        return {} as Sensor;
    }
}

// Get Sensor by Sensor Name
async function getSensor(sensor_name: string): Promise<Sensor> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/sensors/${sensor_name}`, {
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
        return data as Sensor;
    }
    catch (error) {
        console.log("Error in getSensor: ", error);
        return {} as Sensor;
    }
}

// Get Sensor By ID
async function getSensorById(sensor_id: string): Promise<Sensor> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/sensors/id/${sensor_id}`, {
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
        console.log("Error in getSensorById: ", error);
        return {} as Sensor;
    }
}

// Get Sensor Info by Sensor Name
async function getSensorInfo(sensor_name: string): Promise<object> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/sensors/${sensor_name}/info`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            console.log(response.statusText);
            return {} as object;
        }
        const data = await response.json();
        return data as object;
    }
    catch (error) {
        console.log("Error in getSensorInfo: ", error);
        return {} as object;
    }
}

// Set Sensor Info by Sensor Name
async function setSensorInfo(sensor_name: string, params: object): Promise<object> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/sensors/${sensor_name}/info`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params)
        });
        if (!response.ok) {
            console.log(response.statusText);
            return {} as object;
        }
        const data = await response.json();
        return data as object;
    }
    catch (error) {
        console.log("Error in setSensorInfo: ", error);
        return {} as object;
    }
}

// Get Sensor Datasets
async function getSensorDatasets(sensor_name: string): Promise<Dataset[]> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/sensors/${sensor_name}/datasets`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            console.log(response.statusText);
            return [] as Dataset[];
        }
        const data = await response.json();
        return data as Dataset[];
    }
    catch (error) {
        console.log("Error in getSensorDatasets: ", error);
        return [] as Dataset[];
    }
}


export default {
    getSensors,
    createSensor,
    getSensor,
    getSensorById,
    getSensorInfo,
    setSensorInfo,
    getSensorDatasets
}


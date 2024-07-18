import { apiConfig } from "@/api/config";

// Get Sensors
async function getSensors(params?: object): Promise<any[]> {
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
async function createSensor(params?: object): Promise<any> {
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
            return {}; 
        }
        const data = await response.json();
        return data;
    }
    catch (error) {
        console.log("Error in createSensor: ", error);
        return {}; 
    }
}

// Get Sensor by Sensor Name
async function getSensor(sensor_name: string): Promise<any> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/sensors/${sensor_name}`, {
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
        console.log("Error in getSensor: ", error);
        return {}; 
    }
}

// Get Sensor By ID
async function getSensorById(sensor_id: string): Promise<any> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/sensors/id/${sensor_id}`, {
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
        console.log("Error in getSensorById: ", error);
        return {}; 
    }
}

// Get Sensor Info by Sensor Name
async function getSensorInfo(sensor_name: string): Promise<any> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/sensors/${sensor_name}/info`, {
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
async function setSensorInfo(sensor_name: string, params: object): Promise<any> {
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
async function getSensorDatasets(sensor_name: string): Promise<any> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/sensors/${sensor_name}/datasets`, {
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
    getSensorById,
    getSensorInfo,
    setSensorInfo,
    getSensorDatasets
}


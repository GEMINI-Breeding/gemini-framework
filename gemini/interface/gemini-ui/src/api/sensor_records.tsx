import { apiConfig} from "@/api/config";
import ndjsonStream from "can-ndjson-stream";
import { SensorRecord } from "@/api/types";




async function getSensorRecords(params?: object): Promise<ReadableStream<Object>> {
    try {
        const queryString = new URLSearchParams(params as Record<string, string>).toString();
        const response = await fetch(`${apiConfig.baseURL}/sensor_records?${queryString}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const reader = ndjsonStream(response.body);
        return reader;
    } catch (error) {
        console.log("Error in getSensorRecords: ", error);
        return new ReadableStream();
    }
}

// Get Sensor Records Paginated
async function getPaginatedSensorRecords(page_number?: number, page_limit?: number, params?: object): Promise<any> {

    try {

        // If page_number exists, add it to params
        if (page_number) { params = { ...params, page_number: page_number }; }
        // If page_limit exists, add it to params
        if (page_limit) { params = { ...params, page_limit: page_limit }; }
        
        const queryString = new URLSearchParams(params as Record<string, string>).toString();
        const response = await fetch(`${apiConfig.baseURL}/sensor_records/paginate?${queryString}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    }
    catch (error) {
        console.log("Error in getPaginatedSensorRecords: ", error);
        return {};
    }
}


// Create a sensor record (can also include a file)
async function createSensorRecord(params?: object, fileInput?: File): Promise<any> {
    try{    
        const formData = new FormData();
        if (params) {
            for (const [key, value] of Object.entries(params)) {
                if (typeof value === 'object' && value !== null) {
                    formData.append(key, JSON.stringify(value));
                } else {
                    formData.append(key, value as string);
                }
            }
        }
        if (fileInput) {
            formData.append('file', fileInput);
        }

        const response = await fetch(`${apiConfig.baseURL}/sensor_records`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        let data = await response.json();
        return data;
    } catch (error) {
        console.log("Error in createSensorRecord: ", error);
        return {};
    }
}


// Utility Function to Flatten Sensor Record
function flattenSensorRecord(sensorRecord: any): object {
    let flatRecord: { [key: string]: any } = {
        timestamp : sensorRecord.timestamp,
        collection_date : sensorRecord.collection_date,
        sensor_name : sensorRecord.sensor_name
    };

    if (sensorRecord.sensor_data) {
        for (const [key, value] of Object.entries(sensorRecord.sensor_data)) {
            flatRecord[key] = value;
        }
    }

    return flatRecord;
}

export default {
    getSensorRecords,
    createSensorRecord,
    getPaginatedSensorRecords,
    flattenSensorRecord
}
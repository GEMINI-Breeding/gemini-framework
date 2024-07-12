import {isLocal, flaskConfig} from "@/api.config";
import { Sensor, SensorRecord, JobInfo } from "@/app/api/types";
import ndjsonStream from "can-ndjson-stream";

// Get Sensor Records
async function getSensorRecords(params?: object): Promise<ReadableStream<Object>> {
    try {
        const queryString = new URLSearchParams(params as Record<string, string>).toString();
        const response = await fetch(`${flaskConfig.baseURL}/sensor_records?${queryString}`);
        const reader = ndjsonStream(response.body!);
        return reader
    } catch (error) {
        console.log("Error in getSensorRecords: ", error);
        return {} as ReadableStream<Object>;
    }
}


// Create a sensor record (can also include a file)
async function createSensorRecord(params?: object, fileInput?: File): Promise<SensorRecord> {
    try {
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

        const response = await fetch(`${flaskConfig.baseURL}/sensor_records`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        let data = await response.json();
        return data as SensorRecord;
    } catch (error) {
        console.log("Error in createSensorRecord: ", error);
        return {} as SensorRecord;
    }
}


async function processSensorRecordFiles(files?: File[]): Promise<JobInfo> {
    try {
        const formData = new FormData();
        if (files) {
            files.forEach(file => {
                formData.append('files', file);
            });
        }

        const response = await fetch(`${flaskConfig.baseURL}/process_files`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        let data = await response.json();
        return data as JobInfo;
    }
    catch (error) {
        console.log("Error in processSensorRecordFiles: ", error);
        return {} as JobInfo;
    }
}


// Utility Function to Flatten Sensor Record
function flattenSensorRecord(sensorRecord: SensorRecord): object {
    let flatRecord: { [key: string]: any } = {
        timestamp: sensorRecord.timestamp,
        collection_date: sensorRecord.collection_date,
        sensor_name: sensorRecord.sensor_name,
    };

    Object.entries(sensorRecord.sensor_data).forEach(([key, value]) => {
        flatRecord[key] = value;
    });

    // Attach Record Info
    return flatRecord;
}

export default {
    getSensorRecords,
    createSensorRecord,
    processSensorRecordFiles,
    flattenSensorRecord
}
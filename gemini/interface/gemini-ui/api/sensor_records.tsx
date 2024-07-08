import {isLocal, flaskConfig} from "@/api.config";
import { Sensor, SensorRecord, JobInfo } from "@/api/types";
import exp from "constants";


// Get Sensor Records
async function getSensorRecords(params?: object): Promise<SensorRecord[]> {
    try{
        const queryString = new URLSearchParams(params as Record<string, string>).toString();
        const response = await fetch(`${flaskConfig.baseURL}/sensor_records?${queryString}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/x-ndjson',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const reader = response.body!.getReader();
        const decoder = new TextDecoder();
        let sensorRecords: SensorRecord[] = [];

        while (true) {
            const {done, value} = await reader.read();
            if (done) { break; }
            const chunk = decoder.decode(value, {stream: true});
            const lines = chunk.split('\n').filter(line => line.trim());
            lines.forEach(line => {
                try {
                    const sensorRecord = JSON.parse(line);
                    sensorRecords.push(sensorRecord);
                } catch (error) {
                    debugger;
                    console.error("Error parsing NDJSON: ", error);
                }
            });
        }

        return sensorRecords;

    } catch (error) {
        console.log("Error in getSensorRecords: ", error);
        return [];
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

export default {
    getSensorRecords,
    createSensorRecord,
    processSensorRecordFiles
}
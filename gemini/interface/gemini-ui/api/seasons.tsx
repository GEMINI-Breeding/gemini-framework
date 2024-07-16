import { isLocal, flaskConfig } from "api.config.js";
import { Season } from "./types";

// Get Seasons
async function getSeasons(params?: object): Promise<Season[]> {
    try {
        const queryString = new URLSearchParams(params as Record<string, string>).toString();
        const response = await fetch(`${flaskConfig.baseURL}/seasons?${queryString}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        let data = await response.json();
        return data as Season[];

    } catch (error) {
        console.log("Error in getSeasons: ", error);
        return [] as Season[];
    }
}

// Get Season Info by Season and Experiment
async function getSeasonInfo(experimentName: string, seasonName: string): Promise<object> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/seasons/${seasonName}/experiment/${experimentName}/info`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();

    } catch (error) {
        console.log("Error in getSeasonInfo: ", error);
        return {} as object;
    }
}

// Set Season Info by Season and Experiment
async function setSeasonInfo(experimentName: string, seasonName: string, data: object): Promise<object> {
    try {
        const response = await fetch(`${flaskConfig.baseURL}/seasons/${seasonName}/experiment/${experimentName}/info`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();

    } catch (error) {
        console.log("Error in setSeasonInfo: ", error);
        return {} as object;
    }
}

export default { getSeasons, getSeasonInfo, setSeasonInfo };

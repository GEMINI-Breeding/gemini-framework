import { apiConfig } from "@/api/config";

// Get Seasons
async function getSeasons(params?: object): Promise<any[]> {
    try {
        const queryString = new URLSearchParams(params as Record<string, string>).toString();
        const response = await fetch(`${apiConfig.baseURL}/seasons?${queryString}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        let data = await response.json();
        return data;

    } catch (error) {
        console.log("Error in getSeasons: ", error);
        return [];
    }
}

// Get Season Info by Season and Experiment
async function getSeasonInfo(experimentName: string, seasonName: string): Promise<any> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/seasons/${seasonName}/experiment/${experimentName}/info`, {
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
        return {};
    }
}

// Set Season Info by Season and Experiment
async function setSeasonInfo(experimentName: string, seasonName: string, data: object): Promise<any> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/seasons/${seasonName}/experiment/${experimentName}/info`, {
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
        return {};
    }
}

export default { getSeasons, getSeasonInfo, setSeasonInfo };

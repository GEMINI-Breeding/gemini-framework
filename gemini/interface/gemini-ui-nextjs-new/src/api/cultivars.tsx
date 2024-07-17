import { isLocal, apiConfig } from '@/api/config';
import { Cultivar } from "@/api/types";

// Get Cultivars
async function getCultivars(params?: object): Promise<Cultivar[]> {
    try {
        const queryString = new URLSearchParams(params as Record<string, string>).toString();
        const response = await fetch(`${apiConfig.baseURL}/cultivars?${queryString}`, {
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
        console.log("Error in getCultivars: ", error);
        return [];
    }
}

// Create Cultivar
async function createCultivar(params?: object): Promise<Cultivar> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/cultivars`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params)
        });
        if (!response.ok) {
            console.log(response.statusText);
            return {} as Cultivar;
        }
        const data = await response.json();
        return data;
    }
    catch (error) {
        console.log("Error in createCultivar: ", error);
        return {} as Cultivar;
    }
}


// Get Accessions for a given population
async function getPopulationAccessions(cultivar_population: string): Promise<Cultivar[]> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/cultivars/${cultivar_population}/accessions`, {
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
        console.log("Error in getPopulationAccessions: ", error);
        return [];
    }
}

// Get Cultivar Info from accession and population
async function getCultivarInfo(cultivar_population: string, cultivar_accession: string): Promise<object> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/cultivars/${cultivar_population}/${cultivar_accession}/info`, {
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
        console.log("Error in getCultivarInfo: ", error);
        return {};
    }
}

// Set Cultivar Info from accession and population
async function setCultivarInfo(cultivar_population: string, cultivar_accession: string, params: object): Promise<object> {
    try {
        const response = await fetch(`${apiConfig.baseURL}/cultivars/${cultivar_population}/${cultivar_accession}/info`, {
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
        console.log("Error in setCultivarInfo: ", error);
        return {};
    }
}
    
export default {
    getCultivars,
    createCultivar,
    getPopulationAccessions,
    getCultivarInfo,
    setCultivarInfo
}
import { apiSettings } from "./settings";

// Get all sites
async function getAllSites() {
    const response = await fetch(`${apiSettings.apiEndpoint}sites/all`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get site by site name
async function getSite(site_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}sites/${site_name}`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Create a site
async function createSite(site_name: string, site_city: string, site_country: string, site_info: object, experiment_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}sites`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            site_name: site_name,
            site_city: site_city,
            site_country: site_country,
            site_info: site_info,
            experiment_name: experiment_name
        }),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Update a site
async function updateSite(site_name: string, updated_data: object) {
    const response = await fetch(`${apiSettings.apiEndpoint}sites/${site_name}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updated_data),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Delete a site
async function deleteSite(site_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}sites/${site_name}`, {
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Set Site Info
async function setSiteInfo(site_name: string, info: object) {
    const response = await fetch(`${apiSettings.apiEndpoint}sites/${site_name}/info`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(info),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Search Sites
async function searchSites(data: any) {
    const response = await fetch(`${apiSettings.apiEndpoint}sites/search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get Site Plots
async function getSitePlots(site_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}sites/${site_name}/plots`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

// Get Site Experiments
async function getSiteExperiments(site_name: string) {
    const response = await fetch(`${apiSettings.apiEndpoint}sites/${site_name}/experiments`);
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return await response.json();
}

const siteAPI = {
    getAllSites,
    getSite,
    createSite,
    updateSite,
    deleteSite,
    setSiteInfo,
    searchSites,
    getSitePlots,
    getSiteExperiments
};

export default siteAPI;
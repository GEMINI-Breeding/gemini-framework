import { apiConfig } from "@/api/config";
import { Site } from "@/api/types";

// Get Sites
async function getSites(params?: object): Promise<Site[]> {
  try {
    const queryString = new URLSearchParams(
      params as Record<string, string>
    ).toString();
    const response = await fetch(`${apiConfig.baseURL}/sites?${queryString}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      cache: "no-store",
    });
    if (!response.ok) {
      console.log(response.statusText);
      return [] as Site[];
    }
    const data = await response.json();
    return data as Site[];
  } catch (error) {
    console.log("Error in getSites: ", error);
    return [] as Site[];
  }
}

// Create Site
async function createSite(params?: object): Promise<Site> {
  try {
    const response = await fetch(`${apiConfig.baseURL}/sites`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(params),
    });
    if (!response.ok) {
      console.log(response.statusText);
      return {} as Site;
    }
    const data = await response.json();
    return data as Site;
  } catch (error) {
    console.log("Error in createSite: ", error);
    return {} as Site;
  }
}

// Get Site by Site Name
async function getSite(site_name: string): Promise<Site> {
  try {
    const response = await fetch(`${apiConfig.baseURL}/sites/${site_name}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      console.log(response.statusText);
      return {} as Site;
    }
    const data = await response.json();
    return data as Site;
  } catch (error) {
    console.log("Error in getSite: ", error);
    return {} as Site;
  }
}

// Get Site By ID
async function getSiteById(site_id: string): Promise<Site> {
  try {
    const response = await fetch(`${apiConfig.baseURL}/sites/id/${site_id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      console.log(response.statusText);
      return {} as Site;
    }
    const data = await response.json();
    return data as Site;
  } catch (error) {
    console.log("Error in getSiteById: ", error);
    return {} as Site;
  }
}

// Get Site Info
async function getSiteInfo(site_name: string): Promise<object> {
  try {
    const response = await fetch(
      `${apiConfig.baseURL}/sites/${site_name}/info`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    if (!response.ok) {
      console.log(response.statusText);
      return {} as object;
    }
    const data = await response.json();
    return data as object;
  } catch (error) {
    console.log("Error in getSiteInfo: ", error);
    return {} as object;
  }
}

// Set Site Info
async function setSiteInfo(site_name: string, data: object): Promise<object> {
  try {
    const response = await fetch(
      `${apiConfig.baseURL}/sites/${site_name}/info`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }
    );
    if (!response.ok) {
      console.log(response.statusText);
      return {} as object;
    }
    const responseData = await response.json();
    return responseData as object;
  } catch (error) {
    console.log("Error in setSiteInfo: ", error);
    return {} as object;
  }
}

export default {
  getSites,
  createSite,
  getSite,
  getSiteById,
  getSiteInfo,
  setSiteInfo,
};

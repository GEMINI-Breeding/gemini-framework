import { apiConfig } from "./config";
import { SensorPlatform } from "@/api/types";

// Get Sensor Platforms
async function getPlatforms(params?: object): Promise<SensorPlatform[]> {
  try {
    const queryString = new URLSearchParams(
      params as Record<string, string>
    ).toString();
    const response = await fetch(
      `${apiConfig.baseURL}/sensor_platforms?${queryString}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        cache: "no-store",
      }
    );
    if (!response.ok) {
      console.log(response.statusText);
      return [] as SensorPlatform[];
    }
    const data = await response.json();
    return data as SensorPlatform[];
  } catch (error) {
    console.log("Error in getPlatforms: ", error);
    return [] as SensorPlatform[];
  }
}

// Get Platform by ID
async function getPlatformById(platformID: string): Promise<SensorPlatform> {
  try {
    const response = await fetch(
      `${apiConfig.baseURL}/sensor_platforms/id/${platformID}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    if (!response.ok) {
      console.log(response.statusText);
      return {} as SensorPlatform;
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.log("Error in getPlatform: ", error);
    return {} as SensorPlatform;
  }
}

// Get Platform by Name
async function getPlatformByName(
  platformName: string
): Promise<SensorPlatform> {
  try {
    const response = await fetch(
      `${apiConfig.baseURL}/sensor_platforms/${platformName}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    if (!response.ok) {
      console.log(response.statusText);
      return {} as SensorPlatform;
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.log("Error in getPlatform: ", error);
    return {} as SensorPlatform;
  }
}

// Create Platform
async function createPlatform(params?: object): Promise<SensorPlatform> {
  try {
    const response = await fetch(`${apiConfig.baseURL}/sensor_platforms`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(params),
    });
    if (!response.ok) {
      console.log(response.statusText);
      return {} as SensorPlatform;
    }
    const data = await response.json();
    return data as SensorPlatform;
  } catch (error) {
    console.log("Error in createPlatform: ", error);
    return {} as SensorPlatform;
  }
}

// Update Platform
async function updatePlatform(
  platformID: string,
  params?: object
): Promise<SensorPlatform> {
  try {
    const response = await fetch(
      `${apiConfig.baseURL}/sensor_platforms/id/${platformID}`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(params),
      }
    );
    if (!response.ok) {
      console.log(response.statusText);
      return {} as SensorPlatform;
    }
    const data = await response.json();
    return data as SensorPlatform;
  } catch (error) {
    console.log("Error in updatePlatform: ", error);
    return {} as SensorPlatform;
  }
}

// Delete Platform
async function deletePlatform(platformID: string): Promise<boolean> {
  try {
    const response = await fetch(
      `${apiConfig.baseURL}/sensor_platforms/id/${platformID}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    if (!response.ok) {
      console.log(response.statusText);
      return false;
    }
    return true;
  } catch (error) {
    console.log("Error in deletePlatform: ", error);
    return false;
  }
}

export default {
  getPlatforms,
  getPlatformById,
  getPlatformByName,
  createPlatform,
  updatePlatform,
  deletePlatform,
};

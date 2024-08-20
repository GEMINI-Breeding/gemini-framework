import { apiConfig } from "@/api/config";
import { Dataset, Trait } from "@/api/types";

// Get Traits
async function getTraits(params?: object): Promise<Trait[]> {
  try {
    const queryString = new URLSearchParams(
      params as Record<string, string>
    ).toString();
    const response = await fetch(`${apiConfig.baseURL}/traits?${queryString}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      console.log(response.statusText);
      return [] as Trait[];
    }
    const data = await response.json();
    return data as Trait[];
  } catch (error) {
    console.log("Error in getTraits: ", error);
    return [] as Trait[];
  }
}

// Create Trait
async function createTrait(params?: object): Promise<Trait> {
  try {
    const response = await fetch(`${apiConfig.baseURL}/traits`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(params),
    });
    if (!response.ok) {
      console.log(response.statusText);
      return {} as Trait;
    }
    const data = await response.json();
    return data as Trait;
  } catch (error) {
    console.log("Error in createTrait: ", error);
    return {} as Trait;
  }
}

// Get Trait by ID
async function getTraitById(trait_id: string): Promise<Trait> {
  try {
    const response = await fetch(`${apiConfig.baseURL}/traits/id/${trait_id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      console.log(response.statusText);
      return {} as Trait;
    }
    const data = await response.json();
    return data as Trait;
  } catch (error) {
    console.log("Error in getTraitById: ", error);
    return {} as Trait;
  }
}

// Get Traits by Level
async function getTraitsByLevel(trait_level_id: number): Promise<Trait[]> {
  try {
    const response = await fetch(
      `${apiConfig.baseURL}/traits/level/${trait_level_id}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    if (!response.ok) {
      console.log(response.statusText);
      return [] as Trait[];
    }
    const data = await response.json();
    return data as Trait[];
  } catch (error) {
    console.log("Error in getTraitsByLevel: ", error);
    return [] as Trait[];
  }
}

// Get Trait by Trait Name
async function getTrait(trait_name: string): Promise<Trait> {
  try {
    const response = await fetch(`${apiConfig.baseURL}/traits/${trait_name}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      console.log(response.statusText);
      return {} as Trait;
    }
    const data = await response.json();
    return data as Trait;
  } catch (error) {
    console.log("Error in getTrait: ", error);
    return {} as Trait;
  }
}

// Get Trait Info by Trait Name
async function getTraitInfo(trait_name: string): Promise<object> {
  try {
    const response = await fetch(
      `${apiConfig.baseURL}/traits/${trait_name}/info`,
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
    console.log("Error in getTraitInfo: ", error);
    return {} as object;
  }
}

// Set Trait Info by Trait Name
async function setTraitInfo(trait_name: string, data: object): Promise<object> {
  try {
    const response = await fetch(
      `${apiConfig.baseURL}/traits/${trait_name}/info`,
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
    console.log("Error in setTraitInfo: ", error);
    return {} as object;
  }
}

// Get Trait Datasets
async function getTraitDatasets(trait_name: string): Promise<Dataset[]> {
  try {
    const response = await fetch(
      `${apiConfig.baseURL}/traits/${trait_name}/datasets`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    if (!response.ok) {
      console.log(response.statusText);
      return [] as Dataset[];
    }
    const data = await response.json();
    return data as Dataset[];
  } catch (error) {
    console.log("Error in getTraitDatasets: ", error);
    return [] as Dataset[];
  }
}

export default {
  getTraits,
  createTrait,
  getTraitById,
  getTraitsByLevel,
  getTrait,
  getTraitInfo,
  setTraitInfo,
  getTraitDatasets,
};

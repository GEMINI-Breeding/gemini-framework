import { apiConfig } from "@/api/config";
import { URLResponse, FileInformation } from "@/api/types";

async function getObjectDownloadURL(
  object_name: string,
  bucket_name: string = "gemini"
): Promise<URLResponse> {
  try {
    const response = await fetch(
      `${apiConfig.baseURL}/files/download/url?object_name=${object_name}&bucket_name=${bucket_name}`,
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
      return {} as URLResponse;
    }
    const data = await response.json();
    return data as URLResponse;
  } catch (error) {
    console.log("Error in getObjectDownloadURL: ", error);
    return {} as URLResponse;
  }
}

async function getObjectInfo(
  object_name: string,
  bucket_name: string = "gemini"
): Promise<FileInformation> {
  try {
    const response = await fetch(
      `${apiConfig.baseURL}/files/info?object_name=${object_name}&bucket_name=${bucket_name}`,
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
      return {} as FileInformation;
    }
    const data = await response.json();
    return data as FileInformation;
  } catch (error) {
    console.log("Error in getObjectInfo: ", error);
    return {} as FileInformation;
  }
}

async function getObjectUploadURL(
  object_name: string,
  bucket_name: string = "gemini"
): Promise<URLResponse> {
  try {
    const response = await fetch(
      `${apiConfig.baseURL}/files/upload/url?object_name=${object_name}&bucket_name=${bucket_name}`,
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
      return {} as URLResponse;
    }
    const data = await response.json();
    return data as URLResponse;
  } catch (error) {
    console.log("Error in getObjectUploadURL: ", error);
    return {} as URLResponse;
  }
}

export { getObjectDownloadURL, getObjectInfo, getObjectUploadURL };

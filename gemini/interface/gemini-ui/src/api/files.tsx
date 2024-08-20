import { apiConfig } from "@/api/config";
import { URLResponse, FileInformation } from "@/api/types";

async function getObjectDownloadURL(
  object_name: string,
  bucket_name: string = "gemini"
): Promise<URLResponse> {
  try {
    const response = await fetch(
      `${apiConfig.baseURL}/download/url?object_name=${object_name}&bucket_name=${bucket_name}`,
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

// @get('/download/url')
//     async def get_object_download_url(
//             self,
//             object_name: str,
//             bucket_name: str = 'gemini'
//     ) -> URLResponse:
//         """
//         Get the download URL for a file in the bucket.

//         Args:
//             object_name (str): The name of the object in the bucket.
//             bucket_name (str): The name of the bucket. Defaults to 'gemini'.

//         Returns:
//             URLResponse: The download URL for the object.
//         """
//         download_url = file_handler.get_download_url(object_name, bucket_name)
//         return URLResponse(url=download_url)

//     @get('/info')
//     async def get_object_info(
//             self,
//             object_name: str,
//             bucket_name: str = 'gemini'
//     ) -> FileInformation:
//         """
//         Get the metadata for a file in the bucket.

//         Args:
//             object_name (str): The name of the object in the bucket.
//             bucket_name (str): The name of the bucket. Defaults to 'gemini'.

//         Returns:
//             dict: The metadata for the object.
//         """
//         object_info = file_handler.get_file_info(object_name, bucket_name)
//         return FileInformation(
//             bucket_name=object_info.bucket_name,
//             object_name=object_info.object_name,
//             size=object_info.size,
//             last_modified=object_info.last_modified,
//             etag=object_info.etag,
//             content_type=object_info.content_type,
//             version_id=object_info.version_id,
//         )

//     @get('/upload/url')
//     async def get_object_upload_url(
//             self,
//             object_name: str,
//             bucket_name: str = 'gemini'
//     ) -> URLResponse:
//         """
//         Get the upload URL for a file in the bucket.

//         Args:
//             object_name (str): The name of the object in the bucket.
//             bucket_name (str): The name of the bucket. Defaults to 'gemini'.

//         Returns:
//             URLResponse: The upload URL for the object.
//         """
//         upload_url = file_handler.get_upload_url(object_name, bucket_name)
//         return URLResponse(url=upload_url)

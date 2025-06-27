# Files API

The Files API provides endpoints for managing and interacting with files stored in a Minio storage bucket.

## Get File Metadata

- **Endpoint:** `/metadata/{file_path}`
- **Method:** `GET`
- **Description:** Retrieves metadata for a specific file.
- **Path Parameter:**
  - `file_path`: The full path to the file, including the bucket name (e.g., `my-bucket/my-folder/my-file.txt`).
- **Responses:**
  - `200 OK`: A `FileMetadata` object containing the file's details.
  - `404 Not Found`: If the bucket or file does not exist.
  - `500 Internal Server Error`: If an error occurs during the process.

## List Files

- **Endpoint:** `/list/{file_path}`
- **Method:** `GET`
- **Description:** Lists all files within a specified path.
- **Path Parameter:**
  - `file_path`: The path to list files from, including the bucket name (e.g., `my-bucket/my-folder/`).
- **Responses:**
  - `200 OK`: A list of `FileMetadata` objects for each file in the path.
  - `404 Not Found`: If the bucket does not exist.
  - `500 Internal Server Error`: If an error occurs during the process.

## Download a File

- **Endpoint:** `/download/{file_path}`
- **Method:** `GET`
- **Description:** Downloads a specific file from the storage.
- **Path Parameter:**
  - `file_path`: The full path to the file to download.
- **Responses:**
  - `200 OK`: A file stream for downloading.
  - `404 Not Found`: If the bucket or file does not exist.
  - `500 Internal Server Error`: If an error occurs during the process.

## Upload a File

- **Endpoint:** `/upload`
- **Method:** `POST`
- **Description:** Uploads a new file to the specified bucket and path.
- **Request Body (multipart/form-data):**
  - `bucket_name`: The name of the bucket to upload to.
  - `object_name`: The full path and name for the new file.
  - `file`: The file to upload.
- **Responses:**
  - `200 OK`: A `FileMetadata` object for the newly uploaded file.
  - `404 Not Found`: If the bucket does not exist.
  - `500 Internal Server Error`: If the file cannot be uploaded.

## Delete a File

- **Endpoint:** `/delete/{file_path}`
- **Method:** `DELETE`
- **Description:** Deletes a file from the storage.
- **Path Parameter:**
  - `file_path`: The full path to the file to delete.
- **Responses:**
  - `200 OK`: If the file is successfully deleted.
  - `404 Not Found`: If the bucket or file does not exist.
  - `500 Internal Server Error`: If the file cannot be deleted.

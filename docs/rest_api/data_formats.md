# Data Formats API

The Data Formats API allows you to manage and retrieve data format information.

## Get All Data Formats

- **Endpoint:** `/all`
- **Method:** `GET`
- **Description:** Retrieves a list of all data formats available in the database.
- **Responses:**
  - `200 OK`: A list of data format objects.
  - `404 Not Found`: If no data formats are found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Search for Data Formats

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Searches for data formats based on specified criteria.
- **Query Parameters:**
  - `data_format_name` (optional): The name of the data format.
  - `data_format_mime_type` (optional): The MIME type of the data format.
  - `data_format_info` (optional): Additional information in JSON format.
- **Responses:**
  - `200 OK`: A list of matching data format objects.
  - `404 Not Found`: If no data formats match the criteria.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Data Format by ID

- **Endpoint:** `/id/{data_format_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific data format by its unique ID.
- **Path Parameter:**
  - `data_format_id`: The ID of the data format to retrieve.
- **Responses:**
  - `200 OK`: The requested data format object.
  - `404 Not Found`: If the data format with the given ID is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create a New Data Format

- **Endpoint:** `/`
- **Method:** `POST`
- **Description:** Creates a new data format in the database.
- **Request Body:**
  - `data_format_name`: The name of the data format.
  - `data_format_mime_type`: The MIME type of the data format.
  - `data_format_info`: Additional information about the data format.
- **Responses:**
  - `200 OK`: The newly created data format object.
  - `500 Internal Server Error`: If the data format cannot be created.

## Update an Existing Data Format

- **Endpoint:** `/id/{data_format_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing data format's information.
- **Path Parameter:**
  - `data_format_id`: The ID of the data format to update.
- **Request Body:**
  - `data_format_name` (optional): The new name of the data format.
  - `data_format_mime_type` (optional): The new MIME type.
  - `data_format_info` (optional): New information about the data format.
- **Responses:**
  - `200 OK`: The updated data format object.
  - `404 Not Found`: If the data format with the given ID is not found.
  - `500 Internal Server Error`: If the data format cannot be updated.

## Delete a Data Format

- **Endpoint:** `/id/{data_format_id}`
- **Method:** `DELETE`
- **Description:** Deletes a data format from the database.
- **Path Parameter:**
  - `data_format_id`: The ID of the data format to delete.
- **Responses:**
  - `200 OK`: If the data format is successfully deleted.
  - `404 Not Found`: If the data format with the given ID is not found.
  - `500 Internal Server Error`: If the data format cannot be deleted.

## Get Associated Data Types

- **Endpoint:** `/id/{data_format_id}/data_types`
- **Method:** `GET`
- **Description:** Retrieves all data types associated with a specific data format.
- **Path Parameter:**
  - `data_format_id`: The ID of the data format.
- **Responses:**
  - `200 OK`: A list of associated data type objects.
  - `404 Not Found`: If the data format is not found or has no associated data types.
  - `500 Internal Server Error`: If an error occurs during the process.

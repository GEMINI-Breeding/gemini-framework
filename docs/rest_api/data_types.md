# Data Types API

The Data Types API is used for managing and retrieving data types.

## Get All Data Types

- **Endpoint:** `/all`
- **Method:** `GET`
- **Description:** Retrieves a list of all data types from the database.
- **Responses:**
  - `200 OK`: A list of data type objects.
  - `404 Not Found`: If no data types are found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Search for Data Types

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Searches for data types based on the provided criteria.
- **Query Parameters:**
  - `data_type_name` (optional): The name of the data type.
  - `data_type_info` (optional): Additional information in JSON format.
- **Responses:**
  - `200 OK`: A list of matching data type objects.
  - `404 Not Found`: If no data types match the search criteria.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Data Type by ID

- **Endpoint:** `/id/{data_type_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific data type by its unique ID.
- **Path Parameter:**
  - `data_type_id`: The ID of the data type to retrieve.
- **Responses:**
  - `200 OK`: The requested data type object.
  - `404 Not Found`: If the data type with the given ID is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create a New Data Type

- **Endpoint:** `/`
- **Method:** `POST`
- **Description:** Creates a new data type in the database.
- **Request Body:**
  - `data_type_name`: The name of the data type.
  - `data_type_info`: Additional information about the data type.
- **Responses:**
  - `200 OK`: The newly created data type object.
  - `500 Internal Server Error`: If the data type cannot be created.

## Update an Existing Data Type

- **Endpoint:** `/id/{data_type_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing data type's information.
- **Path Parameter:**
  - `data_type_id`: The ID of the data type to update.
- **Request Body:**
  - `data_type_name` (optional): The new name of the data type.
  - `data_type_info` (optional): New information about the data type.
- **Responses:**
  - `200 OK`: The updated data type object.
  - `404 Not Found`: If the data type with the given ID is not found.
  - `500 Internal Server Error`: If the data type cannot be updated.

## Delete a Data Type

- **Endpoint:** `/id/{data_type_id}`
- **Method:** `DELETE`
- **Description:** Deletes a data type from the database.
- **Path Parameter:**
  - `data_type_id`: The ID of the data type to delete.
- **Responses:**
  - `200 OK`: If the data type is successfully deleted.
  - `404 Not Found`: If the data type with the given ID is not found.
  - `500 Internal Server Error`: If the data type cannot be deleted.

## Get Associated Data Formats

- **Endpoint:** `/id/{data_type_id}/data_formats`
- **Method:** `GET`
- **Description:** Retrieves all data formats associated with a specific data type.
- **Path Parameter:**
  - `data_type_id`: The ID of the data type.
- **Responses:**
  - `200 OK`: A list of associated data format objects.
  - `404 Not Found`: If the data type is not found or has no associated data formats.
  - `500 Internal Server Error`: If an error occurs during the process.

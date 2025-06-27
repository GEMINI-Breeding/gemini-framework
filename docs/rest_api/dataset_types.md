# Dataset Types API

The Dataset Types API is used for managing and retrieving dataset type information.

## Get All Dataset Types

- **Endpoint:** `/all`
- **Method:** `GET`
- **Description:** Retrieves a list of all dataset types from the database.
- **Responses:**
  - `200 OK`: A list of dataset type objects.
  - `404 Not Found`: If no dataset types are found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Search for Dataset Types

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Searches for dataset types based on the provided criteria.
- **Query Parameters:**
  - `dataset_type_name` (optional): The name of the dataset type.
  - `dataset_type_info` (optional): Additional information in JSON format.
- **Responses:**
  - `200 OK`: A list of matching dataset type objects.
  - `404 Not Found`: If no dataset types match the search criteria.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Dataset Type by ID

- **Endpoint:** `/id/{dataset_type_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific dataset type by its unique ID.
- **Path Parameter:**
  - `dataset_type_id`: The ID of the dataset type to retrieve.
- **Responses:**
  - `200 OK`: The requested dataset type object.
  - `404 Not Found`: If the dataset type with the given ID is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create a New Dataset Type

- **Endpoint:** `/`
- **Method:** `POST`
- **Description:** Creates a new dataset type in the database.
- **Request Body:**
  - `dataset_type_name`: The name of the dataset type.
  - `dataset_type_info`: Additional information about the dataset type.
- **Responses:**
  - `200 OK`: The newly created dataset type object.
  - `500 Internal Server Error`: If the dataset type cannot be created.

## Update an Existing Dataset Type

- **Endpoint:** `/id/{dataset_type_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing dataset type's information.
- **Path Parameter:**
  - `dataset_type_id`: The ID of the dataset type to update.
- **Request Body:**
  - `dataset_type_name` (optional): The new name of the dataset type.
  - `dataset_type_info` (optional): New information about the dataset type.
- **Responses:**
  - `200 OK`: The updated dataset type object.
  - `404 Not Found`: If the dataset type with the given ID is not found.
  - `500 Internal Server Error`: If the dataset type cannot be updated.

## Delete a Dataset Type

- **Endpoint:** `/id/{dataset_type_id}`
- **Method:** `DELETE`
- **Description:** Deletes a dataset type from the database.
- **Path Parameter:**
  - `dataset_type_id`: The ID of the dataset type to delete.
- **Responses:**
  - `200 OK`: If the dataset type is successfully deleted.
  - `404 Not Found`: If the dataset type with the given ID is not found.
  - `500 Internal Server Error`: If the dataset type cannot be deleted.

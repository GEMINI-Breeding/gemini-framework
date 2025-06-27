# Datasets API

The Datasets API provides endpoints for managing and retrieving dataset information and records.

## Get All Datasets

- **Endpoint:** `/all`
- **Method:** `GET`
- **Description:** Retrieves a list of all datasets from the database.
- **Responses:**
  - `200 OK`: A list of dataset objects.
  - `404 Not Found`: If no datasets are found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Search for Datasets

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Searches for datasets based on specified criteria.
- **Query Parameters:**
  - `dataset_name` (optional): The name of the dataset.
  - `dataset_info` (optional): Additional information in JSON format.
  - `dataset_type_id` (optional): The ID of the dataset type.
  - `experiment_name` (optional): The name of the associated experiment.
  - `collection_date` (optional): The date when the data was collected.
- **Responses:**
  - `200 OK`: A list of matching dataset objects.
  - `404 Not Found`: If no datasets match the criteria.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Dataset by ID

- **Endpoint:** `/id/{dataset_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific dataset by its unique ID.
- **Path Parameter:**
  - `dataset_id`: The ID of the dataset to retrieve.
- **Responses:**
  - `200 OK`: The requested dataset object.
  - `404 Not Found`: If the dataset with the given ID is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create a New Dataset

- **Endpoint:** `/`
- **Method:** `POST`
- **Description:** Creates a new dataset in the database.
- **Request Body:**
  - `collection_date`: The date when the data was collected.
  - `dataset_name`: The name of the dataset.
  - `dataset_info`: Additional information about the dataset.
  - `dataset_type_id`: The ID of the dataset type.
  - `experiment_name`: The name of the associated experiment.
- **Responses:**
  - `200 OK`: The newly created dataset object.
  - `500 Internal Server Error`: If the dataset cannot be created.

## Update an Existing Dataset

- **Endpoint:** `/id/{dataset_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing dataset's information.
- **Path Parameter:**
  - `dataset_id`: The ID of the dataset to update.
- **Request Body:**
  - `collection_date` (optional): The new collection date.
  - `dataset_name` (optional): The new name of the dataset.
  - `dataset_info` (optional): New information about the dataset.
  - `dataset_type_id` (optional): The new dataset type ID.
- **Responses:**
  - `200 OK`: The updated dataset object.
  - `404 Not Found`: If the dataset with the given ID is not found.
  - `500 Internal Server Error`: If the dataset cannot be updated.

## Delete a Dataset

- **Endpoint:** `/id/{dataset_id}`
- **Method:** `DELETE`
- **Description:** Deletes a dataset from the database.
- **Path Parameter:**
  - `dataset_id`: The ID of the dataset to delete.
- **Responses:**
  - `200 OK`: If the dataset is successfully deleted.
  - `404 Not Found`: If the dataset with the given ID is not found.
  - `500 Internal Server Error`: If the dataset cannot be deleted.

## Get Associated Experiments

- **Endpoint:** `/id/{dataset_id}/experiments`
- **Method:** `GET`
- **Description:** Retrieves all experiments associated with a specific dataset.
- **Path Parameter:**
  - `dataset_id`: The ID of the dataset.
- **Responses:**
  - `200 OK`: A list of associated experiment objects.
  - `404 Not Found`: If the dataset is not found or has no associated experiments.
  - `500 Internal Server Error`: If an error occurs during the process.

## Add a Dataset Record

- **Endpoint:** `/id/{dataset_id}/records`
- **Method:** `POST`
- **Description:** Adds a new record to a specific dataset.
- **Path Parameter:**
  - `dataset_id`: The ID of the dataset.
- **Request Body (multipart/form-data):**
  - `timestamp`: The timestamp of the record.
  - `collection_date`: The date of data collection.
  - `dataset_data`: The data for the record.
  - `experiment_name`: The name of the associated experiment.
  - `season_name`: The name of the season.
  - `site_name`: The name of the site.
  - `record_file` (optional): A file associated with the record.
  - `record_info` (optional): Additional information about the record.
- **Responses:**
  - `200 OK`: The newly added dataset record object.
  - `404 Not Found`: If the dataset is not found.
  - `500 Internal Server Error`: If the record cannot be added.

## Search Dataset Records

- **Endpoint:** `/id/{dataset_id}/records`
- **Method:** `GET`
- **Description:** Searches for records within a specific dataset.
- **Path Parameter:**
  - `dataset_id`: The ID of the dataset.
- **Query Parameters:**
  - `experiment_name` (optional): The name of the experiment.
  - `season_name` (optional): The name of the season.
  - `site_name` (optional): The name of the site.
  - `collection_date` (optional): The collection date.
- **Responses:**
  - `200 OK`: A stream of dataset record objects in NDJSON format.
  - `404 Not Found`: If the dataset is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Filter Dataset Records

- **Endpoint:** `/id/{dataset_id}/records/filter`
- **Method:** `GET`
- **Description:** Filters records within a dataset based on a set of criteria.
- **Path Parameter:**
  - `dataset_id`: The ID of the dataset.
- **Query Parameters:**
  - `start_timestamp` (optional): The start of the time range.
  - `end_timestamp` (optional): The end of the time range.
  - `experiment_names` (optional): A list of experiment names.
  - `season_names` (optional): A list of season names.
  - `site_names` (optional): A list of site names.
- **Responses:**
  - `200 OK`: A stream of filtered dataset record objects in NDJSON format.
  - `404 Not Found`: If the dataset is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Dataset Record by ID

- **Endpoint:** `/records/id/{record_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific dataset record by its unique ID.
- **Path Parameter:**
  - `record_id`: The ID of the dataset record.
- **Responses:**
  - `200 OK`: The requested dataset record object.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Download Dataset Record File

- **Endpoint:** `/records/id/{record_id}/download`
- **Method:** `GET`
- **Description:** Downloads the file associated with a specific dataset record.
- **Path Parameter:**
  - `record_id`: The ID of the dataset record.
- **Responses:**
  - `307 Temporary Redirect`: Redirects to the file download URL.
  - `404 Not Found`: If the record or its associated file is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Update Dataset Record

- **Endpoint:** `/records/id/{record_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing dataset record.
- **Path Parameter:**
  - `record_id`: The ID of the dataset record to update.
- **Request Body:**
  - `dataset_data` (optional): The new data for the record.
  - `record_info` (optional): New information about the record.
- **Responses:**
  - `200 OK`: The updated dataset record object.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If the record cannot be updated.

## Delete Dataset Record

- **Endpoint:** `/records/id/{record_id}`
- **Method:** `DELETE`
- **Description:** Deletes a dataset record from the database.
- **Path Parameter:**
  - `record_id`: The ID of the dataset record to delete.
- **Responses:**
  - `200 OK`: If the record is successfully deleted.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If the record cannot be deleted.

# Scripts API

The Scripts API provides endpoints for managing and retrieving scripts and their associated data, including runs, datasets, and records.

## Get All Scripts

- **Endpoint:** `/all`
- **Method:** `GET`
- **Description:** Retrieves a list of all scripts from the database.
- **Responses:**
  - `200 OK`: A list of script objects.
  - `404 Not Found`: If no scripts are found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Search for Scripts

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Searches for scripts based on specified criteria.
- **Query Parameters:**
  - `script_name` (optional): The name of the script.
  - `script_url` (optional): The URL where the script is stored.
  - `script_extension` (optional): The file extension of the script.
  - `script_info` (optional): Additional information in JSON format.
  - `experiment_name` (optional): The name of the associated experiment.
- **Responses:**
  - `200 OK`: A list of matching script objects.
  - `404 Not Found`: If no scripts match the criteria.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Script by ID

- **Endpoint:** `/id/{script_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific script by its unique ID.
- **Path Parameter:**
  - `script_id`: The ID of the script to retrieve.
- **Responses:**
  - `200 OK`: The requested script object.
  - `404 Not Found`: If the script with the given ID is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create a New Script

- **Endpoint:** `/`
- **Method:** `POST`
- **Description:** Creates a new script in the database.
- **Request Body:**
  - `script_name`: The name of the script.
  - `script_url`: The URL where the script is stored.
  - `script_extension`: The file extension of the script.
  - `script_info`: Additional information about the script.
  - `experiment_name`: The name of the associated experiment.
- **Responses:**
  - `200 OK`: The newly created script object.
  - `500 Internal Server Error`: If the script cannot be created.

## Update an Existing Script

- **Endpoint:** `/id/{script_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing script's information.
- **Path Parameter:**
  - `script_id`: The ID of the script to update.
- **Request Body:**
  - `script_name` (optional): The new name of the script.
  - `script_url` (optional): The new URL for the script.
  - `script_extension` (optional): The new file extension.
  - `script_info` (optional): New information about the script.
- **Responses:**
  - `200 OK`: The updated script object.
  - `404 Not Found`: If the script with the given ID is not found.
  - `500 Internal Server Error`: If the script cannot be updated.

## Delete a Script

- **Endpoint:** `/id/{script_id}`
- **Method:** `DELETE`
- **Description:** Deletes a script from the database.
- **Path Parameter:**
  - `script_id`: The ID of the script to delete.
- **Responses:**
  - `200 OK`: If the script is successfully deleted.
  - `404 Not Found`: If the script with the given ID is not found.
  - `500 Internal Server Error`: If the script cannot be deleted.

## Get Associated Experiments

- **Endpoint:** `/id/{script_id}/experiments`
- **Method:** `GET`
- **Description:** Retrieves all experiments associated with a specific script.
- **Responses:**
  - `200 OK`: A list of associated experiment objects.
  - `404 Not Found`: If the script is not found or has no associated experiments.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Script Runs

- **Endpoint:** `/id/{script_id}/runs`
- **Method:** `GET`
- **Description:** Retrieves all runs associated with a specific script.
- **Responses:**
  - `200 OK`: A list of associated script run objects.
  - `404 Not Found`: If the script is not found or has no associated runs.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Script Datasets

- **Endpoint:** `/id/{script_id}/datasets`
- **Method:** `GET`
- **Description:** Retrieves all datasets associated with a specific script.
- **Responses:**
  - `200 OK`: A list of associated dataset objects.
  - `404 Not Found`: If the script is not found or has no associated datasets.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create Script Run

- **Endpoint:** `/id/{script_id}/runs`
- **Method:** `POST`
- **Description:** Creates a new run for a specific script.
- **Request Body:**
  - `script_run_info`: Additional information about the script run.
- **Responses:**
  - `200 OK`: The newly created script run object.
  - `500 Internal Server Error`: If the run cannot be created.

## Create Script Dataset

- **Endpoint:** `/id/{script_id}/datasets`
- **Method:** `POST`
- **Description:** Creates a new dataset for a specific script.
- **Request Body:**
  - `dataset_name`: The name of the dataset.
  - `dataset_info`: Additional information about the dataset.
  - `collection_date`: The date when the data was collected.
  - `experiment_name`: The name of the associated experiment.
- **Responses:**
  - `200 OK`: The newly created dataset object.
  - `500 Internal Server Error`: If the dataset cannot be created.

## Add a Script Record

- **Endpoint:** `/id/{script_id}/records`
- **Method:** `POST`
- **Description:** Adds a new record to a specific script.
- **Request Body (multipart/form-data):**
  - `timestamp`: The timestamp of the record.
  - `collection_date`: The date of data collection.
  - `script_data`: The data for the record.
  - `dataset_name`: The name of the associated dataset.
  - `experiment_name`: The name of the associated experiment.
  - `season_name`: The name of the season.
  - `site_name`: The name of the site.
  - `record_file` (optional): A file associated with the record.
  - `record_info` (optional): Additional information about the record.
- **Responses:**
  - `200 OK`: The newly added script record object.
  - `404 Not Found`: If the script is not found.
  - `500 Internal Server Error`: If the record cannot be added.

## Search Script Records

- **Endpoint:** `/id/{script_id}/records`
- **Method:** `GET`
- **Description:** Searches for records within a specific script.
- **Query Parameters:**
  - `experiment_name` (optional): The name of the experiment.
  - `season_name` (optional): The name of the season.
  - `site_name` (optional): The name of the site.
  - `collection_date` (optional): The collection date.
- **Responses:**
  - `200 OK`: A stream of script record objects in NDJSON format.
  - `404 Not Found`: If the script is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Filter Script Records

- **Endpoint:** `/id/{script_id}/records/filter`
- **Method:** `GET`
- **Description:** Filters records within a script based on a set of criteria.
- **Query Parameters:**
  - `start_timestamp` (optional): The start of the time range.
  - `end_timestamp` (optional): The end of the time range.
  - `dataset_names` (optional): A list of dataset names.
  - `experiment_names` (optional): A list of experiment names.
  - `season_names` (optional): A list of season names.
  - `site_names` (optional): A list of site names.
- **Responses:**
  - `200 OK`: A stream of filtered script record objects in NDJSON format.
  - `404 Not Found`: If the script is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Script Record by ID

- **Endpoint:** `/records/id/{record_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific script record by its unique ID.
- **Path Parameter:**
  - `record_id`: The ID of the script record.
- **Responses:**
  - `200 OK`: The requested script record object.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Download Script Record File

- **Endpoint:** `/records/id/{record_id}/download`
- **Method:** `GET`
- **Description:** Downloads the file associated with a specific script record.
- **Path Parameter:**
  - `record_id`: The ID of the script record.
- **Responses:**
  - `307 Temporary Redirect`: Redirects to the file download URL.
  - `404 Not Found`: If the record or its associated file is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Update Script Record

- **Endpoint:** `/records/id/{record_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing script record.
- **Path Parameter:**
  - `record_id`: The ID of the script record to update.
- **Request Body:**
  - `script_data` (optional): The new data for the record.
  - `record_info` (optional): New information about the record.
- **Responses:**
  - `200 OK`: The updated script record object.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If the record cannot be updated.

## Delete Script Record

- **Endpoint:** `/records/id/{record_id}`
- **Method:** `DELETE`
- **Description:** Deletes a script record from the database.
- **Path Parameter:**
  - `record_id`: The ID of the script record to delete.
- **Responses:**
  - `200 OK`: If the record is successfully deleted.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If the record cannot be deleted.

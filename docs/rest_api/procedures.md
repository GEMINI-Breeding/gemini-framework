# Procedures API

The Procedures API provides endpoints for managing and retrieving procedural data, including their runs, datasets, and records.

## Get All Procedures

- **Endpoint:** `/all`
- **Method:** `GET`
- **Description:** Retrieves a list of all procedures from the database.
- **Responses:**
  - `200 OK`: A list of procedure objects.
  - `404 Not Found`: If no procedures are found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Search for Procedures

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Searches for procedures based on specified criteria.
- **Query Parameters:**
  - `procedure_name` (optional): The name of the procedure.
  - `procedure_info` (optional): Additional information in JSON format.
  - `experiment_name` (optional): The name of the associated experiment.
- **Responses:**
  - `200 OK`: A list of matching procedure objects.
  - `404 Not Found`: If no procedures match the criteria.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Procedure by ID

- **Endpoint:** `/id/{procedure_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific procedure by its unique ID.
- **Path Parameter:**
  - `procedure_id`: The ID of the procedure to retrieve.
- **Responses:**
  - `200 OK`: The requested procedure object.
  - `404 Not Found`: If the procedure with the given ID is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create a New Procedure

- **Endpoint:** `/`
- **Method:** `POST`
- **Description:** Creates a new procedure in the database.
- **Request Body:**
  - `procedure_name`: The name of the procedure.
  - `procedure_info`: Additional information about the procedure.
  - `experiment_name`: The name of the associated experiment.
- **Responses:**
  - `200 OK`: The newly created procedure object.
  - `500 Internal Server Error`: If the procedure cannot be created.

## Update an Existing Procedure

- **Endpoint:** `/id/{procedure_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing procedure's information.
- **Path Parameter:**
  - `procedure_id`: The ID of the procedure to update.
- **Request Body:**
  - `procedure_name` (optional): The new name of the procedure.
  - `procedure_info` (optional): New information about the procedure.
- **Responses:**
  - `200 OK`: The updated procedure object.
  - `404 Not Found`: If the procedure with the given ID is not found.
  - `500 Internal Server Error`: If the procedure cannot be updated.

## Delete a Procedure

- **Endpoint:** `/id/{procedure_id}`
- **Method:** `DELETE`
- **Description:** Deletes a procedure from the database.
- **Path Parameter:**
  - `procedure_id`: The ID of the procedure to delete.
- **Responses:**
  - `200 OK`: If the procedure is successfully deleted.
  - `404 Not Found`: If the procedure with the given ID is not found.
  - `500 Internal Server Error`: If the procedure cannot be deleted.

## Get Procedure Runs

- **Endpoint:** `/id/{procedure_id}/runs`
- **Method:** `GET`
- **Description:** Retrieves all runs associated with a specific procedure.
- **Responses:**
  - `200 OK`: A list of associated procedure run objects.
  - `404 Not Found`: If the procedure is not found or has no associated runs.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Procedure Experiments

- **Endpoint:** `/id/{procedure_id}/experiments`
- **Method:** `GET`
- **Description:** Retrieves all experiments associated with a specific procedure.
- **Responses:**
  - `200 OK`: A list of associated experiment names.
  - `404 Not Found`: If the procedure is not found or has no associated experiments.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Procedure Datasets

- **Endpoint:** `/id/{procedure_id}/datasets`
- **Method:** `GET`
- **Description:** Retrieves all datasets associated with a specific procedure.
- **Responses:**
  - `200 OK`: A list of associated dataset objects.
  - `404 Not Found`: If the procedure is not found or has no associated datasets.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create Procedure Run

- **Endpoint:** `/id/{procedure_id}/runs`
- **Method:** `POST`
- **Description:** Creates a new run for a specific procedure.
- **Request Body:**
  - `procedure_run_info`: Additional information about the procedure run.
- **Responses:**
  - `200 OK`: The newly created procedure run object.
  - `500 Internal Server Error`: If the run cannot be created.

## Create Procedure Dataset

- **Endpoint:** `/id/{procedure_id}/datasets`
- **Method:** `POST`
- **Description:** Creates a new dataset for a specific procedure.
- **Request Body:**
  - `dataset_name`: The name of the dataset.
  - `dataset_info`: Additional information about the dataset.
  - `collection_date`: The date when the data was collected.
  - `experiment_name`: The name of the associated experiment.
- **Responses:**
  - `200 OK`: The newly created dataset object.
  - `500 Internal Server Error`: If the dataset cannot be created.

## Add a Procedure Record

- **Endpoint:** `/id/{procedure_id}/records`
- **Method:** `POST`
- **Description:** Adds a new record to a specific procedure.
- **Request Body (multipart/form-data):**
  - `timestamp`: The timestamp of the record.
  - `collection_date`: The date of data collection.
  - `procedure_data`: The data for the record.
  - `dataset_name`: The name of the associated dataset.
  - `experiment_name`: The name of the associated experiment.
  - `season_name`: The name of the season.
  - `site_name`: The name of the site.
  - `record_file` (optional): A file associated with the record.
  - `record_info` (optional): Additional information about the record.
- **Responses:**
  - `200 OK`: The newly added procedure record object.
  - `404 Not Found`: If the procedure is not found.
  - `500 Internal Server Error`: If the record cannot be added.

## Search Procedure Records

- **Endpoint:** `/id/{procedure_id}/records`
- **Method:** `GET`
- **Description:** Searches for records within a specific procedure.
- **Query Parameters:**
  - `experiment_name` (optional): The name of the experiment.
  - `season_name` (optional): The name of the season.
  - `site_name` (optional): The name of the site.
  - `collection_date` (optional): The collection date.
- **Responses:**
  - `200 OK`: A stream of procedure record objects in NDJSON format.
  - `404 Not Found`: If the procedure is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Filter Procedure Records

- **Endpoint:** `/id/{procedure_id}/records/filter`
- **Method:** `GET`
- **Description:** Filters records within a procedure based on a set of criteria.
- **Query Parameters:**
  - `start_timestamp` (optional): The start of the time range.
  - `end_timestamp` (optional): The end of the time range.
  - `dataset_names` (optional): A list of dataset names.
  - `experiment_names` (optional): A list of experiment names.
  - `season_names` (optional): A list of season names.
  - `site_names` (optional): A list of site names.
- **Responses:**
  - `200 OK`: A stream of filtered procedure record objects in NDJSON format.
  - `404 Not Found`: If the procedure is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Procedure Record by ID

- **Endpoint:** `/records/id/{procedure_record_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific procedure record by its unique ID.
- **Path Parameter:**
  - `procedure_record_id`: The ID of the procedure record.
- **Responses:**
  - `200 OK`: The requested procedure record object.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Download Procedure Record File

- **Endpoint:** `/records/id/{record_id}/download`
- **Method:** `GET`
- **Description:** Downloads the file associated with a specific procedure record.
- **Path Parameter:**
  - `record_id`: The ID of the procedure record.
- **Responses:**
  - `307 Temporary Redirect`: Redirects to the file download URL.
  - `404 Not Found`: If the record or its associated file is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Update Procedure Record

- **Endpoint:** `/records/id/{procedure_record_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing procedure record.
- **Path Parameter:**
  - `procedure_record_id`: The ID of the procedure record to update.
- **Request Body:**
  - `procedure_data` (optional): The new data for the record.
  - `record_info` (optional): New information about the record.
- **Responses:**
  - `200 OK`: The updated procedure record object.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If the record cannot be updated.

## Delete Procedure Record

- **Endpoint:** `/records/id/{procedure_record_id}`
- **Method:** `DELETE`
- **Description:** Deletes a procedure record from the database.
- **Path Parameter:**
  - `procedure_record_id`: The ID of the procedure record to delete.
- **Responses:**
  - `200 OK`: If the record is successfully deleted.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If the record cannot be deleted.

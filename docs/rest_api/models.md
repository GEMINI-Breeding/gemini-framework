# Models API

The Models API provides endpoints for managing and retrieving machine learning models and their associated data.

## Get All Models

- **Endpoint:** `/all`
- **Method:** `GET`
- **Description:** Retrieves a list of all models from the database.
- **Responses:**
  - `200 OK`: A list of model objects.
  - `404 Not Found`: If no models are found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Search for Models

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Searches for models based on specified criteria.
- **Query Parameters:**
  - `model_name` (optional): The name of the model.
  - `model_url` (optional): The URL where the model is stored.
  - `model_info` (optional): Additional information in JSON format.
  - `experiment_name` (optional): The name of the associated experiment.
- **Responses:**
  - `200 OK`: A list of matching model objects.
  - `404 Not Found`: If no models match the criteria.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Model by ID

- **Endpoint:** `/id/{model_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific model by its unique ID.
- **Path Parameter:**
  - `model_id`: The ID of the model to retrieve.
- **Responses:**
  - `200 OK`: The requested model object.
  - `404 Not Found`: If the model with the given ID is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create a New Model

- **Endpoint:** `/`
- **Method:** `POST`
- **Description:** Creates a new model in the database.
- **Request Body:**
  - `model_name`: The name of the model.
  - `model_url`: The URL where the model is stored.
  - `model_info`: Additional information about the model.
  - `experiment_name`: The name of the associated experiment.
- **Responses:**
  - `200 OK`: The newly created model object.
  - `500 Internal Server Error`: If the model cannot be created.

## Update an Existing Model

- **Endpoint:** `/id/{model_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing model's information.
- **Path Parameter:**
  - `model_id`: The ID of the model to update.
- **Request Body:**
  - `model_name` (optional): The new name of the model.
  - `model_url` (optional): The new URL for the model.
  - `model_info` (optional): New information about the model.
- **Responses:**
  - `200 OK`: The updated model object.
  - `404 Not Found`: If the model with the given ID is not found.
  - `500 Internal Server Error`: If the model cannot be updated.

## Delete a Model

- **Endpoint:** `/id/{model_id}`
- **Method:** `DELETE`
- **Description:** Deletes a model from the database.
- **Path Parameter:**
  - `model_id`: The ID of the model to delete.
- **Responses:**
  - `200 OK`: If the model is successfully deleted.
  - `404 Not Found`: If the model with the given ID is not found.
  - `500 Internal Server Error`: If the model cannot be deleted.

## Get Model Experiments

- **Endpoint:** `/id/{model_id}/experiments`
- **Method:** `GET`
- **Description:** Retrieves all experiments associated with a specific model.
- **Responses:**
  - `200 OK`: A list of associated experiment names.
  - `404 Not Found`: If the model is not found or has no associated experiments.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Model Runs

- **Endpoint:** `/id/{model_id}/runs`
- **Method:** `GET`
- **Description:** Retrieves all runs associated with a specific model.
- **Responses:**
  - `200 OK`: A list of associated model run objects.
  - `404 Not Found`: If the model is not found or has no associated runs.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Model Datasets

- **Endpoint:** `/id/{model_id}/datasets`
- **Method:** `GET`
- **Description:** Retrieves all datasets associated with a specific model.
- **Responses:**
  - `200 OK`: A list of associated dataset objects.
  - `404 Not Found`: If the model is not found or has no associated datasets.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create Model Run

- **Endpoint:** `/id/{model_id}/runs`
- **Method:** `POST`
- **Description:** Creates a new run for a specific model.
- **Request Body:**
  - `model_run_info`: Additional information about the model run.
- **Responses:**
  - `200 OK`: The newly created model run object.
  - `500 Internal Server Error`: If the model run cannot be created.

## Create Model Dataset

- **Endpoint:** `/id/{model_id}/datasets`
- **Method:** `POST`
- **Description:** Creates a new dataset for a specific model.
- **Request Body:**
  - `dataset_name`: The name of the dataset.
  - `dataset_info`: Additional information about the dataset.
  - `collection_date`: The date when the data was collected.
  - `experiment_name`: The name of the associated experiment.
- **Responses:**
  - `200 OK`: The newly created dataset object.
  - `500 Internal Server Error`: If the dataset cannot be created.

## Add a Model Record

- **Endpoint:** `/id/{model_id}/records`
- **Method:** `POST`
- **Description:** Adds a new record to a specific model.
- **Request Body (multipart/form-data):**
  - `timestamp`: The timestamp of the record.
  - `collection_date`: The date of data collection.
  - `model_data`: The data for the record.
  - `dataset_name`: The name of the associated dataset.
  - `experiment_name`: The name of the associated experiment.
  - `season_name`: The name of the season.
  - `site_name`: The name of the site.
  - `record_file` (optional): A file associated with the record.
  - `record_info` (optional): Additional information about the record.
- **Responses:**
  - `200 OK`: The newly added model record object.
  - `404 Not Found`: If the model is not found.
  - `500 Internal Server Error`: If the record cannot be added.

## Search Model Records

- **Endpoint:** `/id/{model_id}/records`
- **Method:** `GET`
- **Description:** Searches for records within a specific model.
- **Query Parameters:**
  - `experiment_name` (optional): The name of the experiment.
  - `season_name` (optional): The name of the season.
  - `site_name` (optional): The name of the site.
  - `collection_date` (optional): The collection date.
- **Responses:**
  - `200 OK`: A stream of model record objects in NDJSON format.
  - `404 Not Found`: If the model is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Filter Model Records

- **Endpoint:** `/id/{model_id}/records/filter`
- **Method:** `GET`
- **Description:** Filters records within a model based on a set of criteria.
- **Query Parameters:**
  - `start_timestamp` (optional): The start of the time range.
  - `end_timestamp` (optional): The end of the time range.
  - `dataset_names` (optional): A list of dataset names.
  - `experiment_names` (optional): A list of experiment names.
  - `season_names` (optional): A list of season names.
  - `site_names` (optional): A list of site names.
- **Responses:**
  - `200 OK`: A stream of filtered model record objects in NDJSON format.
  - `404 Not Found`: If the model is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Model Record by ID

- **Endpoint:** `/records/id/{record_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific model record by its unique ID.
- **Path Parameter:**
  - `record_id`: The ID of the model record.
- **Responses:**
  - `200 OK`: The requested model record object.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Download Model Record File

- **Endpoint:** `/records/id/{record_id}/download`
- **Method:** `GET`
- **Description:** Downloads the file associated with a specific model record.
- **Path Parameter:**
  - `record_id`: The ID of the model record.
- **Responses:**
  - `307 Temporary Redirect`: Redirects to the file download URL.
  - `404 Not Found`: If the record or its associated file is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Update Model Record

- **Endpoint:** `/records/id/{record_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing model record.
- **Path Parameter:**
  - `record_id`: The ID of the model record to update.
- **Request Body:**
  - `model_data` (optional): The new data for the record.
  - `record_info` (optional): New information about the record.
- **Responses:**
  - `200 OK`: The updated model record object.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If the record cannot be updated.

## Delete Model Record

- **Endpoint:** `/records/id/{record_id}`
- **Method:** `DELETE`
- **Description:** Deletes a model record from the database.
- **Path Parameter:**
  - `record_id`: The ID of the model record to delete.
- **Responses:**
  - `200 OK`: If the record is successfully deleted.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If the record cannot be deleted.

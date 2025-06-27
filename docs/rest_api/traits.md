# Traits API

The Traits API provides endpoints for managing and retrieving trait data, including their records, experiments, and associated datasets.

## Get All Traits

- **Endpoint:** `/all`
- **Method:** `GET`
- **Description:** Retrieves a list of all traits from the database.
- **Responses:**
  - `200 OK`: A list of trait objects.
  - `404 Not Found`: If no traits are found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Search for Traits

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Searches for traits based on specified criteria.
- **Query Parameters:**
  - `trait_name` (optional): The name of the trait.
  - `trait_units` (optional): The units of the trait.
  - `trait_level_id` (optional): The ID of the trait level.
  - `trait_info` (optional): Additional information in JSON format.
  - `trait_metrics` (optional): Metrics associated with the trait in JSON format.
  - `experiment_name` (optional): The name of the associated experiment.
- **Responses:**
  - `200 OK`: A list of matching trait objects.
  - `404 Not Found`: If no traits match the criteria.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Trait by ID

- **Endpoint:** `/id/{trait_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific trait by its unique ID.
- **Path Parameter:**
  - `trait_id`: The ID of the trait to retrieve.
- **Responses:**
  - `200 OK`: The requested trait object.
  - `404 Not Found`: If the trait with the given ID is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create a New Trait

- **Endpoint:** `/`
- **Method:** `POST`
- **Description:** Creates a new trait in the database.
- **Request Body:**
  - `trait_name`: The name of the trait.
  - `trait_units`: The units of the trait.
  - `trait_level_id`: The ID of the trait level.
  - `trait_info`: Additional information about the trait.
  - `trait_metrics`: Metrics associated with the trait.
  - `experiment_name`: The name of the associated experiment.
- **Responses:**
  - `200 OK`: The newly created trait object.
  - `500 Internal Server Error`: If the trait cannot be created.

## Update an Existing Trait

- **Endpoint:** `/id/{trait_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing trait's information.
- **Path Parameter:**
  - `trait_id`: The ID of the trait to update.
- **Request Body:**
  - `trait_name` (optional): The new name of the trait.
  - `trait_units` (optional): The new units for the trait.
  - `trait_level_id` (optional): The new ID of the trait level.
  - `trait_info` (optional): New information about the trait.
  - `trait_metrics` (optional): New metrics for the trait.
- **Responses:**
  - `200 OK`: The updated trait object.
  - `404 Not Found`: If the trait with the given ID is not found.
  - `500 Internal Server Error`: If the trait cannot be updated.

## Delete a Trait

- **Endpoint:** `/id/{trait_id}`
- **Method:** `DELETE`
- **Description:** Deletes a trait from the database.
- **Path Parameter:**
  - `trait_id`: The ID of the trait to delete.
- **Responses:**
  - `204 No Content`: If the trait is successfully deleted.
  - `404 Not Found`: If the trait with the given ID is not found.
  - `500 Internal Server Error`: If the trait cannot be deleted.

## Get Trait Experiments

- **Endpoint:** `/id/{trait_id}/experiments`
- **Method:** `GET`
- **Description:** Retrieves all experiments associated with a specific trait.
- **Responses:**
  - `200 OK`: A list of associated experiment names.
  - `404 Not Found`: If the trait is not found or has no associated experiments.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Trait Datasets

- **Endpoint:** `/id/{trait_id}/datasets`
- **Method:** `GET`
- **Description:** Retrieves all datasets associated with a specific trait.
- **Responses:**
  - `200 OK`: A list of associated dataset objects.
  - `404 Not Found`: If the trait is not found or has no associated datasets.
  - `500 Internal Server Error`: If an error occurs during the process.

## Add a Trait Record

- **Endpoint:** `/id/{trait_id}/records`
- **Method:** `POST`
- **Description:** Adds a new record to a specific trait.
- **Request Body (multipart/form-data):**
  - `timestamp`: The timestamp of the record.
  - `collection_date`: The date of data collection.
  - `trait_value`: The value of the trait for the record.
  - `dataset_name`: The name of the associated dataset.
  - `experiment_name`: The name of the associated experiment.
  - `season_name`: The name of the season.
  - `site_name`: The name of the site.
  - `plot_number`: The number of the plot.
  - `plot_row_number`: The row number of the plot.
  - `plot_column_number`: The column number of the plot.
  - `record_info` (optional): Additional information about the record.
- **Responses:**
  - `200 OK`: The newly added trait record object.
  - `404 Not Found`: If the trait is not found.
  - `500 Internal Server Error`: If the record cannot be added.

## Search Trait Records

- **Endpoint:** `/id/{trait_id}/records`
- **Method:** `GET`
- **Description:** Searches for records within a specific trait.
- **Query Parameters:**
  - `experiment_name` (optional): The name of the experiment.
  - `season_name` (optional): The name of the season.
  - `site_name` (optional): The name of the site.
  - `plot_number` (optional): The number of the plot.
  - `plot_row_number` (optional): The row number of the plot.
  - `plot_column_number` (optional): The column number of the plot.
  - `collection_date` (optional): The collection date.
- **Responses:**
  - `200 OK`: A stream of trait record objects in NDJSON format.
  - `404 Not Found`: If the trait is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Filter Trait Records

- **Endpoint:** `/id/{trait_id}/records/filter`
- **Method:** `GET`
- **Description:** Filters records within a trait based on a set of criteria.
- **Query Parameters:**
  - `start_timestamp` (optional): The start of the time range.
  - `end_timestamp` (optional): The end of the time range.
  - `dataset_names` (optional): A list of dataset names.
  - `experiment_names` (optional): A list of experiment names.
  - `season_names` (optional): A list of season names.
  - `site_names` (optional): A list of site names.
- **Responses:**
  - `200 OK`: A stream of filtered trait record objects in NDJSON format.
  - `404 Not Found`: If the trait is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Trait Record by ID

- **Endpoint:** `/records/id/{trait_record_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific trait record by its unique ID.
- **Path Parameter:**
  - `trait_record_id`: The ID of the trait record.
- **Responses:**
  - `200 OK`: The requested trait record object.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Update Trait Record

- **Endpoint:** `/records/id/{trait_record_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing trait record.
- **Path Parameter:**
  - `trait_record_id`: The ID of the trait record to update.
- **Request Body:**
  - `trait_value` (optional): The new value for the trait.
  - `record_info` (optional): New information about the record.
- **Responses:**
  - `200 OK`: The updated trait record object.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If the record cannot be updated.

## Delete Trait Record

- **Endpoint:** `/records/id/{trait_record_id}`
- **Method:** `DELETE`
- **Description:** Deletes a trait record from the database.
- **Path Parameter:**
  - `trait_record_id`: The ID of the trait record to delete.
- **Responses:**
  - `204 No Content`: If the record is successfully deleted.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If the record cannot be deleted.

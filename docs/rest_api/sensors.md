# Sensors API

The Sensors API provides endpoints for managing and retrieving sensor data, including their records, experiments, and associated platforms.

## Get All Sensors

- **Endpoint:** `/all`
- **Method:** `GET`
- **Description:** Retrieves a list of all sensors from the database.
- **Responses:**
  - `200 OK`: A list of sensor objects.
  - `404 Not Found`: If no sensors are found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Search for Sensors

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Searches for sensors based on specified criteria.
- **Query Parameters:**
  - `sensor_name` (optional): The name of the sensor.
  - `sensor_type_id` (optional): The ID of the sensor type.
  - `sensor_data_type_id` (optional): The ID of the sensor's data type.
  - `sensor_data_format_id` (optional): The ID of the sensor's data format.
  - `sensor_info` (optional): Additional information in JSON format.
  - `experiment_name` (optional): The name of the associated experiment.
- **Responses:**
  - `200 OK`: A list of matching sensor objects.
  - `404 Not Found`: If no sensors match the criteria.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Sensor by ID

- **Endpoint:** `/id/{sensor_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific sensor by its unique ID.
- **Path Parameter:**
  - `sensor_id`: The ID of the sensor to retrieve.
- **Responses:**
  - `200 OK`: The requested sensor object.
  - `404 Not Found`: If the sensor with the given ID is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create a New Sensor

- **Endpoint:** `/`
- **Method:** `POST`
- **Description:** Creates a new sensor in the database.
- **Request Body:**
  - `sensor_name`: The name of the sensor.
  - `sensor_type_id`: The ID of the sensor type.
  - `sensor_data_type_id`: The ID of the sensor's data type.
  - `sensor_data_format_id`: The ID of the sensor's data format.
  - `sensor_info`: Additional information about the sensor.
  - `experiment_name`: The name of the associated experiment.
- **Responses:**
  - `200 OK`: The newly created sensor object.
  - `500 Internal Server Error`: If the sensor cannot be created.

## Update an Existing Sensor

- **Endpoint:** `/id/{sensor_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing sensor's information.
- **Path Parameter:**
  - `sensor_id`: The ID of the sensor to update.
- **Request Body:**
  - `sensor_name` (optional): The new name of the sensor.
  - `sensor_type_id` (optional): The new ID of the sensor type.
  - `sensor_data_type_id` (optional): The new ID of the sensor's data type.
  - `sensor_data_format_id` (optional): The new ID of the sensor's data format.
  - `sensor_info` (optional): New information about the sensor.
- **Responses:**
  - `200 OK`: The updated sensor object.
  - `404 Not Found`: If the sensor with the given ID is not found.
  - `500 Internal Server Error`: If the sensor cannot be updated.

## Delete a Sensor

- **Endpoint:** `/id/{sensor_id}`
- **Method:** `DELETE`
- **Description:** Deletes a sensor from the database.
- **Path Parameter:**
  - `sensor_id`: The ID of the sensor to delete.
- **Responses:**
  - `204 No Content`: If the sensor is successfully deleted.
  - `404 Not Found`: If the sensor with the given ID is not found.
  - `500 Internal Server Error`: If the sensor cannot be deleted.

## Get Sensor Experiments

- **Endpoint:** `/id/{sensor_id}/experiments`
- **Method:** `GET`
- **Description:** Retrieves all experiments associated with a specific sensor.
- **Responses:**
  - `200 OK`: A list of associated experiment objects.
  - `404 Not Found`: If the sensor is not found or has no associated experiments.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Sensor Platforms

- **Endpoint:** `/id/{sensor_id}/sensor_platforms`
- **Method:** `GET`
- **Description:** Retrieves all sensor platforms associated with a specific sensor.
- **Responses:**
  - `200 OK`: A list of associated sensor platform objects.
  - `404 Not Found`: If the sensor is not found or has no associated platforms.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Sensor Datasets

- **Endpoint:** `/id/{sensor_id}/datasets`
- **Method:** `GET`
- **Description:** Retrieves all datasets associated with a specific sensor.
- **Responses:**
  - `200 OK`: A list of associated dataset objects.
  - `404 Not Found`: If the sensor is not found or has no associated datasets.
  - `500 Internal Server Error`: If an error occurs during the process.

## Add a Sensor Record

- **Endpoint:** `/id/{sensor_id}/records`
- **Method:** `POST`
- **Description:** Adds a new record to a specific sensor.
- **Request Body (multipart/form-data):**
  - `timestamp`: The timestamp of the record.
  - `collection_date`: The date of data collection.
  - `sensor_data`: The data for the record.
  - `dataset_name`: The name of the associated dataset.
  - `experiment_name`: The name of the associated experiment.
  - `season_name`: The name of the season.
  - `site_name`: The name of the site.
  - `plot_number`: The number of the plot.
  - `plot_row_number`: The row number of the plot.
  - `plot_column_number`: The column number of the plot.
  - `record_file` (optional): A file associated with the record.
  - `record_info` (optional): Additional information about the record.
- **Responses:**
  - `200 OK`: The newly added sensor record object.
  - `404 Not Found`: If the sensor is not found.
  - `500 Internal Server Error`: If the record cannot be added.

## Search Sensor Records

- **Endpoint:** `/id/{sensor_id}/records`
- **Method:** `GET`
- **Description:** Searches for records within a specific sensor.
- **Query Parameters:**
  - `experiment_name` (optional): The name of the experiment.
  - `season_name` (optional): The name of the season.
  - `site_name` (optional): The name of the site.
  - `plot_number` (optional): The number of the plot.
  - `plot_row_number` (optional): The row number of the plot.
  - `plot_column_number` (optional): The column number of the plot.
  - `collection_date` (optional): The collection date.
- **Responses:**
  - `200 OK`: A stream of sensor record objects in NDJSON format.
  - `404 Not Found`: If the sensor is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Filter Sensor Records

- **Endpoint:** `/id/{sensor_id}/records/filter`
- **Method:** `GET`
- **Description:** Filters records within a sensor based on a set of criteria.
- **Query Parameters:**
  - `start_timestamp` (optional): The start of the time range.
  - `end_timestamp` (optional): The end of the time range.
  - `dataset_names` (optional): A list of dataset names.
  - `experiment_names` (optional): A list of experiment names.
  - `season_names` (optional): A list of season names.
  - `site_names` (optional): A list of site names.
- **Responses:**
  - `200 OK`: A stream of filtered sensor record objects in NDJSON format.
  - `404 Not Found`: If the sensor is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Sensor Record by ID

- **Endpoint:** `/records/id/{record_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific sensor record by its unique ID.
- **Path Parameter:**
  - `record_id`: The ID of the sensor record.
- **Responses:**
  - `200 OK`: The requested sensor record object.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Download Sensor Record File

- **Endpoint:** `/records/id/{record_id}/download`
- **Method:** `GET`
- **Description:** Downloads the file associated with a specific sensor record.
- **Path Parameter:**
  - `record_id`: The ID of the sensor record.
- **Responses:**
  - `307 Temporary Redirect`: Redirects to the file download URL.
  - `404 Not Found`: If the record or its associated file is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Update Sensor Record

- **Endpoint:** `/records/id/{record_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing sensor record.
- **Path Parameter:**
  - `record_id`: The ID of the sensor record to update.
- **Request Body:**
  - `sensor_data` (optional): The new data for the record.
  - `record_info` (optional): New information about the record.
- **Responses:**
  - `200 OK`: The updated sensor record object.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If the record cannot be updated.

## Delete Sensor Record

- **Endpoint:** `/records/id/{record_id}`
- **Method:** `DELETE`
- **Description:** Deletes a sensor record from the database.
- **Path Parameter:**
  - `record_id`: The ID of the sensor record to delete.
- **Responses:**
  - `204 No Content`: If the record is successfully deleted.
  - `404 Not Found`: If the record is not found.
  - `500 Internal Server Error`: If the record cannot be deleted.

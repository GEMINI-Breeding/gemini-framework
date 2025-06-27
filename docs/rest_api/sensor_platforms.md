# Sensor Platforms API

The Sensor Platforms API provides endpoints for managing and retrieving sensor platform data and their associations.

## Get All Sensor Platforms

- **Endpoint:** `/all`
- **Method:** `GET`
- **Description:** Retrieves a list of all sensor platforms in the database.
- **Responses:**
  - `200 OK`: A list of sensor platform objects.
  - `404 Not Found`: If no sensor platforms are found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Search for Sensor Platforms

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Searches for sensor platforms based on the provided criteria.
- **Query Parameters:**
  - `sensor_platform_name` (optional): The name of the sensor platform.
  - `sensor_platform_info` (optional): Additional information about the sensor platform in JSON format.
  - `experiment_name` (optional): The name of the associated experiment.
- **Responses:**
  - `200 OK`: A list of matching sensor platform objects.
  - `404 Not Found`: If no sensor platforms match the search criteria.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Sensor Platform by ID

- **Endpoint:** `/id/{sensor_platform_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific sensor platform by its unique ID.
- **Path Parameter:**
  - `sensor_platform_id`: The ID of the sensor platform to retrieve.
- **Responses:**
  - `200 OK`: The requested sensor platform object.
  - `404 Not Found`: If the sensor platform with the given ID is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create a New Sensor Platform

- **Endpoint:** `/`
- **Method:** `POST`
- **Description:** Creates a new sensor platform in the database.
- **Request Body:**
  - `sensor_platform_name`: The name of the sensor platform.
  - `sensor_platform_info`: Additional information about the sensor platform.
  - `experiment_name`: The name of the associated experiment.
- **Responses:**
  - `200 OK`: The newly created sensor platform object.
  - `500 Internal Server Error`: If the sensor platform cannot be created.

## Update an Existing Sensor Platform

- **Endpoint:** `/id/{sensor_platform_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing sensor platform's information.
- **Path Parameter:**
  - `sensor_platform_id`: The ID of the sensor platform to update.
- **Request Body:**
  - `sensor_platform_name` (optional): The new name of the sensor platform.
  - `sensor_platform_info` (optional): New information about the sensor platform.
- **Responses:**
  - `200 OK`: The updated sensor platform object.
  - `404 Not Found`: If the sensor platform with the given ID is not found.
  - `500 Internal Server Error`: If the sensor platform cannot be updated.

## Delete a Sensor Platform

- **Endpoint:** `/id/{sensor_platform_id}`
- **Method:** `DELETE`
- **Description:** Deletes a sensor platform from the database.
- **Path Parameter:**
  - `sensor_platform_id`: The ID of the sensor platform to delete.
- **Responses:**
  - `204 No Content`: If the sensor platform is successfully deleted.
  - `404 Not Found`: If the sensor platform with the given ID is not found.
  - `500 Internal Server Error`: If the sensor platform cannot be deleted.

## Get Experiments for Sensor Platform

- **Endpoint:** `/id/{sensor_platform_id}/experiments`
- **Method:** `GET`
- **Description:** Retrieves all experiments associated with a specific sensor platform.
- **Responses:**
  - `200 OK`: A list of associated experiment objects.
  - `404 Not Found`: If the sensor platform is not found or has no associated experiments.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Sensors for Sensor Platform

- **Endpoint:** `/id/{sensor_platform_id}/sensors`
- **Method:** `GET`
- **Description:** Retrieves all sensors associated with a specific sensor platform.
- **Responses:**
  - `200 OK`: A list of associated sensor objects.
  - `404 Not Found`: If the sensor platform is not found or has no associated sensors.
  - `500 Internal Server Error`: If an error occurs during the process.

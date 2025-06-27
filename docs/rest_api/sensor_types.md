# Sensor Types API

The Sensor Types API provides endpoints for managing and retrieving sensor type data.

## Get All Sensor Types

- **Endpoint:** `/all`
- **Method:** `GET`
- **Description:** Retrieves a list of all sensor types in the database.
- **Responses:**
  - `200 OK`: A list of sensor type objects.
  - `404 Not Found`: If no sensor types are found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Search for Sensor Types

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Searches for sensor types based on the provided criteria.
- **Query Parameters:**
  - `sensor_type_name` (optional): The name of the sensor type.
  - `sensor_type_info` (optional): Additional information about the sensor type in JSON format.
- **Responses:**
  - `200 OK`: A list of matching sensor type objects.
  - `404 Not Found`: If no sensor types match the search criteria.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Sensor Type by ID

- **Endpoint:** `/id/{sensor_type_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific sensor type by its unique ID.
- **Path Parameter:**
  - `sensor_type_id`: The ID of the sensor type to retrieve.
- **Responses:**
  - `200 OK`: The requested sensor type object.
  - `404 Not Found`: If the sensor type with the given ID is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create a New Sensor Type

- **Endpoint:** `/`
- **Method:** `POST`
- **Description:** Creates a new sensor type in the database.
- **Request Body:**
  - `sensor_type_name`: The name of the sensor type.
  - `sensor_type_info`: Additional information about the sensor type.
- **Responses:**
  - `200 OK`: The newly created sensor type object.
  - `500 Internal Server Error`: If the sensor type cannot be created.

## Update an Existing Sensor Type

- **Endpoint:** `/id/{sensor_type_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing sensor type's information.
- **Path Parameter:**
  - `sensor_type_id`: The ID of the sensor type to update.
- **Request Body:**
  - `sensor_type_name` (optional): The new name of the sensor type.
  - `sensor_type_info` (optional): New information about the sensor type.
- **Responses:**
  - `200 OK`: The updated sensor type object.
  - `404 Not Found`: If the sensor type with the given ID is not found.
  - `500 Internal Server Error`: If the sensor type cannot be updated.

## Delete a Sensor Type

- **Endpoint:** `/id/{sensor_type_id}`
- **Method:** `DELETE`
- **Description:** Deletes a sensor type from the database.
- **Path Parameter:**
  - `sensor_type_id`: The ID of the sensor type to delete.
- **Responses:**
  - `204 No Content`: If the sensor type is successfully deleted.
  - `404 Not Found`: If the sensor type with the given ID is not found.
  - `500 Internal Server Error`: If the sensor type cannot be deleted.

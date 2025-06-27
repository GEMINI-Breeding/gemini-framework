# Cultivars API

The Cultivars API provides endpoints for managing and retrieving cultivar data.

## Get All Cultivars

- **Endpoint:** `/all`
- **Method:** `GET`
- **Description:** Retrieves a list of all cultivars in the database.
- **Responses:**
  - `200 OK`: A list of cultivar objects.
  - `404 Not Found`: If no cultivars are found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Search for Cultivars

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Searches for cultivars based on the provided criteria.
- **Query Parameters:**
  - `cultivar_population` (optional): The population of the cultivar.
  - `cultivar_accession` (optional): The accession number of the cultivar.
  - `cultivar_info` (optional): Additional information about the cultivar in JSON format.
  - `experiment_name` (optional): The name of the associated experiment.
- **Responses:**
  - `200 OK`: A list of matching cultivar objects.
  - `404 Not Found`: If no cultivars match the search criteria.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Cultivar by ID

- **Endpoint:** `/id/{cultivar_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific cultivar by its unique ID.
- **Path Parameter:**
  - `cultivar_id`: The ID of the cultivar to retrieve.
- **Responses:**
  - `200 OK`: The requested cultivar object.
  - `404 Not Found`: If the cultivar with the given ID is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create a New Cultivar

- **Endpoint:** `/`
- **Method:** `POST`
- **Description:** Creates a new cultivar in the database.
- **Request Body:**
  - `cultivar_population`: The population of the cultivar.
  - `cultivar_accession`: The accession number of the cultivar.
  - `cultivar_info`: Additional information about the cultivar.
  - `experiment_name`: The name of the associated experiment.
- **Responses:**
  - `200 OK`: The newly created cultivar object.
  - `500 Internal Server Error`: If the cultivar cannot be created.

## Update an Existing Cultivar

- **Endpoint:** `/id/{cultivar_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing cultivar's information.
- **Path Parameter:**
  - `cultivar_id`: The ID of the cultivar to update.
- **Request Body:**
  - `cultivar_population` (optional): The new population of the cultivar.
  - `cultivar_accession` (optional): The new accession number of the cultivar.
  - `cultivar_info` (optional): New information about the cultivar.
- **Responses:**
  - `200 OK`: The updated cultivar object.
  - `404 Not Found`: If the cultivar with the given ID is not found.
  - `500 Internal Server Error`: If the cultivar cannot be updated.

## Delete a Cultivar

- **Endpoint:** `/id/{cultivar_id}`
- **Method:** `DELETE`
- **Description:** Deletes a cultivar from the database.
- **Path Parameter:**
  - `cultivar_id`: The ID of the cultivar to delete.
- **Responses:**
  - `200 OK`: If the cultivar is successfully deleted.
  - `404 Not Found`: If the cultivar with the given ID is not found.
  - `500 Internal Server Error`: If the cultivar cannot be deleted.

## Get Associated Experiments

- **Endpoint:** `/id/{cultivar_id}/experiments`
- **Method:** `GET`
- **Description:** Retrieves all experiments associated with a specific cultivar.
- **Path Parameter:**
  - `cultivar_id`: The ID of the cultivar.
- **Responses:**
  - `200 OK`: A list of associated experiment objects.
  - `404 Not Found`: If the cultivar is not found or has no associated experiments.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Associated Plots

- **Endpoint:** `/id/{cultivar_id}/plots`
- **Method:** `GET`
- **Description:** Retrieves all plots associated with a specific cultivar.
- **Path Parameter:**
  - `cultivar_id`: The ID of the cultivar.
- **Responses:**
  - `200 OK`: A list of associated plot objects.
  - `404 Not Found`: If the cultivar is not found or has no associated plots.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Associated Plants

- **Endpoint:** `/id/{cultivar_id}/plants`
- **Method:** `GET`
- **Description:** Retrieves all plants associated with a specific cultivar.
- **Path Parameter:**
  - `cultivar_id`: The ID of the cultivar.
- **Responses:**
  - `200 OK`: A list of associated plant objects.
  - `404 Not Found`: If the cultivar is not found or has no associated plants.
  - `500 Internal Server Error`: If an error occurs during the process.

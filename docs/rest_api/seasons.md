# Seasons API

The Seasons API provides endpoints for managing and retrieving season data and their associations.

## Get All Seasons

- **Endpoint:** `/all`
- **Method:** `GET`
- **Description:** Retrieves a list of all seasons in the database.
- **Responses:**
  - `200 OK`: A list of season objects.
  - `404 Not Found`: If no seasons are found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Search for Seasons

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Searches for seasons based on the provided criteria.
- **Query Parameters:**
  - `season_name` (optional): The name of the season.
  - `season_info` (optional): Additional information about the season in JSON format.
  - `season_start_date` (optional): The start date of the season.
  - `season_end_date` (optional): The end date of the season.
  - `experiment_name` (optional): The name of the associated experiment.
- **Responses:**
  - `200 OK`: A list of matching season objects.
  - `404 Not Found`: If no seasons match the search criteria.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Season by ID

- **Endpoint:** `/id/{season_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific season by its unique ID.
- **Path Parameter:**
  - `season_id`: The ID of the season to retrieve.
- **Responses:**
  - `200 OK`: The requested season object.
  - `404 Not Found`: If the season with the given ID is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create a New Season

- **Endpoint:** `/`
- **Method:** `POST`
- **Description:** Creates a new season in the database.
- **Request Body:**
  - `season_name`: The name of the season.
  - `season_info`: Additional information about the season.
  - `season_start_date`: The start date of the season.
  - `season_end_date`: The end date of the season.
  - `experiment_name`: The name of the associated experiment.
- **Responses:**
  - `200 OK`: The newly created season object.
  - `500 Internal Server Error`: If the season cannot be created.

## Update an Existing Season

- **Endpoint:** `/id/{season_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing season's information.
- **Path Parameter:**
  - `season_id`: The ID of the season to update.
- **Request Body:**
  - `season_name` (optional): The new name of the season.
  - `season_info` (optional): New information about the season.
  - `season_start_date` (optional): The new start date of the season.
  - `season_end_date` (optional): The new end date of the season.
- **Responses:**
  - `200 OK`: The updated season object.
  - `404 Not Found`: If the season with the given ID is not found.
  - `500 Internal Server Error`: If the season cannot be updated.

## Delete a Season

- **Endpoint:** `/id/{season_id}`
- **Method:** `DELETE`
- **Description:** Deletes a season from the database.
- **Path Parameter:**
  - `season_id`: The ID of the season to delete.
- **Responses:**
  - `204 No Content`: If the season is successfully deleted.
  - `404 Not Found`: If the season with the given ID is not found.
  - `500 Internal Server Error`: If the season cannot be deleted.

## Get Associated Experiment

- **Endpoint:** `/id/{season_id}/experiment`
- **Method:** `GET`
- **Description:** Retrieves the experiment associated with a specific season.
- **Responses:**
  - `200 OK`: The associated experiment object.
  - `404 Not Found`: If the season or its associated experiment is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

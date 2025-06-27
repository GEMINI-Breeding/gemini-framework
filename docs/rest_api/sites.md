# Sites API

The Sites API provides endpoints for managing and retrieving site data and their associations.

## Get All Sites

- **Endpoint:** `/all`
- **Method:** `GET`
- **Description:** Retrieves a list of all sites in the database.
- **Responses:**
  - `200 OK`: A list of site objects.
  - `404 Not Found`: If no sites are found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Search for Sites

- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Searches for sites based on the provided criteria.
- **Query Parameters:**
  - `site_name` (optional): The name of the site.
  - `site_city` (optional): The city where the site is located.
  - `site_state` (optional): The state where the site is located.
  - `site_country` (optional): The country where the site is located.
  - `site_info` (optional): Additional information about the site in JSON format.
  - `experiment_name` (optional): The name of the associated experiment.
- **Responses:**
  - `200 OK`: A list of matching site objects.
  - `404 Not Found`: If no sites match the search criteria.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Site by ID

- **Endpoint:** `/id/{site_id}`
- **Method:** `GET`
- **Description:** Retrieves a specific site by its unique ID.
- **Path Parameter:**
  - `site_id`: The ID of the site to retrieve.
- **Responses:**
  - `200 OK`: The requested site object.
  - `404 Not Found`: If the site with the given ID is not found.
  - `500 Internal Server Error`: If an error occurs during the process.

## Create a New Site

- **Endpoint:** `/`
- **Method:** `POST`
- **Description:** Creates a new site in the database.
- **Request Body:**
  - `site_name`: The name of the site.
  - `site_city`: The city where the site is located.
  - `site_state`: The state where the site is located.
  - `site_country`: The country where the site is located.
  - `site_info`: Additional information about the site.
  - `experiment_name`: The name of the associated experiment.
- **Responses:**
  - `200 OK`: The newly created site object.
  - `500 Internal Server Error`: If the site cannot be created.

## Update an Existing Site

- **Endpoint:** `/id/{site_id}`
- **Method:** `PATCH`
- **Description:** Updates an existing site's information.
- **Path Parameter:**
  - `site_id`: The ID of the site to update.
- **Request Body:**
  - `site_name` (optional): The new name of the site.
  - `site_city` (optional): The new city for the site.
  - `site_state` (optional): The new state for the site.
  - `site_country` (optional): The new country for the site.
  - `site_info` (optional): New information about the site.
- **Responses:**
  - `200 OK`: The updated site object.
  - `404 Not Found`: If the site with the given ID is not found.
  - `500 Internal Server Error`: If the site cannot be updated.

## Delete a Site

- **Endpoint:** `/id/{site_id}`
- **Method:** `DELETE`
- **Description:** Deletes a site from the database.
- **Path Parameter:**
  - `site_id`: The ID of the site to delete.
- **Responses:**
  - `204 No Content`: If the site is successfully deleted.
  - `404 Not Found`: If the site with the given ID is not found.
  - `500 Internal Server Error`: If the site cannot be deleted.

## Get Associated Experiments

- **Endpoint:** `/id/{site_id}/experiments`
- **Method:** `GET`
- **Description:** Retrieves all experiments associated with a specific site.
- **Responses:**
  - `200 OK`: A list of associated experiment objects.
  - `404 Not Found`: If the site is not found or has no associated experiments.
  - `500 Internal Server Error`: If an error occurs during the process.

## Get Associated Plots

- **Endpoint:** `/id/{site_id}/plots`
- **Method:** `GET`
- **Description:** Retrieves all plots associated with a specific site.
- **Responses:**
  - `200 OK`: A list of associated plot objects.
  - `404 Not Found`: If the site is not found or has no associated plots.
  - `500 Internal Server Error`: If an error occurs during the process.

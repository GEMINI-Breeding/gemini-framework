# Sensor Records

The `sensor_records` table stores individual data records collected by sensors, designed for columnar storage.

## Table Schema

| Column Name       | Data Type   | Description                                                                                      |
| ----------------- | ----------- | ------------------------------------------------------------------------------------------------ |
| `id`              | `UUID`      | **Primary Key.** Unique identifier for the sensor record.                                        |
| `timestamp`       | `TIMESTAMP` | Timestamp of the record.                                                                         |
| `sensor_id`       | `UUID`      | Foreign key referencing the sensor.                                                              |
| `sensor_name`     | `String(255)` | The name of the sensor.                                                                          |
| `sensor_type_id`  | `Integer`   | Foreign key referencing the sensor type.                                                         |
| `sensor_type_name`| `String(255)` | The name of the sensor type.                                                                     |
| `sensor_data`     | `JSONB`     | Additional JSONB data for the sensor.                                                            |
| `experiment_id`   | `UUID`      | Foreign key referencing the experiment.                                                          |
| `experiment_name` | `String(255)` | The name of the experiment.                                                                      |
| `season_id`       | `UUID`      | Foreign key referencing the season.                                                              |
| `season_name`     | `String(255)` | The name of the season.                                                                          |
| `site_id`         | `UUID`      | Foreign key referencing the site.                                                                |
| `site_name`       | `String(255)` | The name of the site.                                                                            |
| `record_file`     | `String(255)` | The file where the record is stored.                                                             |
| `record_info`     | `JSONB`     | Additional JSONB data for the record.                                                            |

## Constraints and Indexes

- **Unique Constraint:** A `UniqueConstraint` on `timestamp`, `sensor_id`, `sensor_name`, `sensor_type_id`, `sensor_type_name`, `experiment_id`, `experiment_name`, `season_id`, `season_name`, `site_id`, and `site_name` ensures uniqueness for each record.
- **GIN Index:** A GIN index named `idx_sensor_records_record_info` is applied to the `record_info` column to optimize queries on the JSONB data.

## Methods

- **`filter_records`**: A class method that allows filtering sensor records based on various parameters such as `start_timestamp`, `end_timestamp`, `sensor_names`, `sensor_type_names`, `experiment_names`, `season_names`, and `site_names`. This method leverages a PostgreSQL function `gemini.filter_sensor_records` for efficient filtering.

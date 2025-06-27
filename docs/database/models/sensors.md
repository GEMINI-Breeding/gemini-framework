# Sensors

The `sensors` table stores information about the individual sensors used to collect data.

## Table Schema

| Column Name             | Data Type   | Description                                                                                      |
| ----------------------- | ----------- | ------------------------------------------------------------------------------------------------ |
| `id`                    | `UUID`      | **Primary Key.** A unique identifier for the sensor.                                             |
| `sensor_name`           | `String(255)` | The name of the sensor. This column has a unique constraint.                                     |
| `sensor_type_id`        | `Integer`   | **Foreign Key.** References the `id` of the sensor type in the `sensor_types` table.             |
| `sensor_data_type_id`   | `Integer`   | **Foreign Key.** References the `id` of the data type in the `data_types` table.                 |
| `sensor_data_format_id` | `Integer`   | **Foreign Key.** References the `id` of the data format in the `data_formats` table.             |
| `sensor_info`           | `JSONB`     | A JSONB column for storing additional, unstructured information about the sensor.                |
| `created_at`            | `TIMESTAMP` | The timestamp when the record was created. Defaults to the current time.                         |
| `updated_at`            | `TIMESTAMP` | The timestamp when the record was last updated. Automatically updates on any modification.       |

## Constraints and Indexes

- **Unique Constraint:** A `UniqueConstraint` on `sensor_name` ensures that each sensor has a unique name.
- **GIN Index:** A GIN index named `idx_sensors_info` is applied to the `sensor_info` column to optimize queries on the JSONB data.

## Relationships

- **`sensor_type`:** A many-to-one relationship with the `sensor_types` table.
- **`data_type`:** A many-to-one relationship with the `data_types` table.
- **`data_format`:** A many-to-one relationship with the `data_formats` table.
- **Association Tables:** The `sensors` table is linked to `sensor_platforms`, `experiments`, and `datasets` through association tables.

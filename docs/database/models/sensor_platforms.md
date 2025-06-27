# Sensor Platforms

The `sensor_platforms` table stores information about the platforms on which sensors are mounted.

## Table Schema

| Column Name            | Data Type      | Description                                                                                      |
| ---------------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `id`                   | `UUID`         | **Primary Key.** A unique identifier for the sensor platform.                                    |
| `sensor_platform_name` | `String(255)`  | The name of the sensor platform. This column has a unique constraint.                            |
| `sensor_platform_info` | `JSONB`        | A JSONB column for storing additional, unstructured information about the sensor platform.       |
| `created_at`           | `TIMESTAMP`    | The timestamp when the record was created. Defaults to the current time.                         |
| `updated_at`           | `TIMESTAMP`    | The timestamp when the record was last updated. Automatically updates on any modification.       |

## Constraints and Indexes

- **Unique Constraint:** A `UniqueConstraint` on `sensor_platform_name` ensures that each sensor platform has a unique name.
- **GIN Index:** A GIN index named `idx_sensor_platforms_info` is applied to the `sensor_platform_info` column to optimize queries on the JSONB data.

## Relationships

- **Association Tables:** The `sensor_platforms` table is linked to `sensors` and `experiments` through association tables.

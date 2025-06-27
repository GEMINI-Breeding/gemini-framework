# Seasons

The `seasons` table defines the different growing seasons or time periods for experiments.

## Table Schema

| Column Name       | Data Type   | Description                                                                                      |
| ----------------- | ----------- | ------------------------------------------------------------------------------------------------ |
| `id`              | `UUID`      | **Primary Key.** A unique identifier for the season.                                             |
| `experiment_id`   | `UUID`      | **Foreign Key.** References the `id` of the experiment to which the season belongs.              |
| `season_name`     | `String(255)` | The name of the season.                                                                          |
| `season_info`     | `JSONB`     | A JSONB column for storing additional, unstructured information about the season.                |
| `season_start_date` | `DATE`      | The start date of the season.                                                                    |
| `season_end_date`   | `DATE`      | The end date of the season.                                                                      |
| `created_at`      | `TIMESTAMP` | The timestamp when the record was created. Defaults to the current time.                         |
| `updated_at`      | `TIMESTAMP` | The timestamp when the record was last updated. Automatically updates on any modification.       |

## Constraints and Indexes

- **Unique Constraint:** A `UniqueConstraint` on `experiment_id` and `season_name` ensures that each season name is unique within an experiment.
- **Check Constraint:** Ensures that `season_start_date` is less than or equal to `season_end_date`.
- **GIN Index:** A GIN index named `idx_seasons_info` is applied to the `season_info` column to optimize queries on the JSONB data.

## Relationships

- **`experiment`:** A many-to-one relationship with the `experiments` table.
- **`plots`:** A one-to-many relationship with the `plots` table, where one season can have multiple plots.

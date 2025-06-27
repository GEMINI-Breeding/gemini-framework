# Model Runs

The `model_runs` table stores information about each execution of a model.

## Table Schema

| Column Name      | Data Type   | Description                                                                                      |
| ---------------- | ----------- | ------------------------------------------------------------------------------------------------ |
| `id`             | `UUID`      | **Primary Key.** A unique identifier for the model run.                                          |
| `model_id`       | `UUID`      | **Foreign Key.** References the `id` of the model in the `models` table.                         |
| `model_run_info` | `JSONB`     | A JSONB column for storing additional, unstructured information about the model run.             |
| `created_at`     | `TIMESTAMP` | The timestamp when the record was created. Defaults to the current time.                         |
| `updated_at`     | `TIMESTAMP` | The timestamp when the record was last updated. Automatically updates on any modification.       |

## Constraints and Indexes

- **Unique Constraint:** A `UniqueConstraint` on `model_id` and `model_run_info` ensures that each combination is unique.
- **GIN Index:** A GIN index named `idx_model_runs_info` is applied to the `model_run_info` column to optimize queries on the JSONB data.

## Relationships

- **`model`:** A many-to-one relationship with the `models` table, linking each model run to the model that was executed.

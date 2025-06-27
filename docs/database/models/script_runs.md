# Script Runs

The `script_runs` table logs every execution of a script.

## Table Schema

| Column Name     | Data Type   | Description                                                                                      |
| --------------- | ----------- | ------------------------------------------------------------------------------------------------ |
| `id`            | `UUID`      | **Primary Key.** A unique identifier for the script run.                                         |
| `script_id`     | `UUID`      | **Foreign Key.** References the `id` of the script in the `scripts` table.                       |
| `script_run_info` | `JSONB`     | A JSONB column for storing additional, unstructured information about the script run.            |
| `created_at`    | `TIMESTAMP` | The timestamp when the record was created. Defaults to the current time.                         |
| `updated_at`    | `TIMESTAMP` | The timestamp when the record was last updated. Automatically updates on any modification.       |

## Constraints and Indexes

- **Unique Constraint:** A `UniqueConstraint` on `script_id` and `script_run_info` ensures that each combination is unique.
- **GIN Index:** A GIN index named `idx_script_runs_info` is applied to the `script_run_info` column to optimize queries on the JSONB data.

## Relationships

- **`script`:** A many-to-one relationship with the `scripts` table, linking each script run to the script that was executed.

# Procedure Runs

The `procedure_runs` table tracks every execution of a procedure.

## Table Schema

| Column Name          | Data Type   | Description                                                                                      |
| -------------------- | ----------- | ------------------------------------------------------------------------------------------------ |
| `id`                 | `UUID`      | **Primary Key.** A unique identifier for the procedure run.                                      |
| `procedure_id`       | `UUID`      | **Foreign Key.** References the `id` of the procedure in the `procedures` table.                 |
| `procedure_run_info` | `JSONB`     | A JSONB column for storing additional, unstructured information about the procedure run.         |
| `created_at`         | `TIMESTAMP` | The timestamp when the record was created. Defaults to the current time.                         |
| `updated_at`         | `TIMESTAMP` | The timestamp when the record was last updated. Automatically updates on any modification.       |

## Constraints and Indexes

- **Unique Constraint:** A `UniqueConstraint` on `procedure_id` and `procedure_run_info` ensures that each combination is unique.
- **GIN Index:** A GIN index named `idx_procedure_runs_info` is applied to the `procedure_run_info` column to optimize queries on the JSONB data.

## Relationships

- **`procedure`:** A many-to-one relationship with the `procedures` table, linking each procedure run to the procedure that was executed.

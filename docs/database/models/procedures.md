# Procedures

The `procedures` table stores information about the standard operating procedures (SOPs) or protocols followed in the experiments.

## Table Schema

| Column Name      | Data Type      | Description                                                                                      |
| ---------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `id`             | `UUID`         | **Primary Key.** A unique identifier for the procedure.                                          |
| `procedure_name` | `String(255)`  | The name of the procedure. This column has a unique constraint.                                  |
| `procedure_info` | `JSONB`        | A JSONB column for storing additional, unstructured information about the procedure.             |
| `created_at`     | `TIMESTAMP`    | The timestamp when the record was created. Defaults to the current time.                         |
| `updated_at`     | `TIMESTAMP`    | The timestamp when the record was last updated. Automatically updates on any modification.       |

## Constraints and Indexes

- **Unique Constraint:** A `UniqueConstraint` on `procedure_name` ensures that each procedure has a unique name.
- **GIN Index:** A GIN index named `idx_procedures_info` is applied to the `procedure_info` column to optimize queries on the JSONB data.

## Relationships

- **`procedure_runs`:** A one-to-many relationship with the `procedure_runs` table, where one procedure can have multiple runs.
- **Association Tables:** The `procedures` table is linked to other entities like `experiments` and `datasets` through association tables.

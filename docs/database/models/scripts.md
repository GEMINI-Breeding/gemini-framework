# Scripts

The `scripts` table stores information about scripts used for data processing, analysis, or other tasks.

## Table Schema

| Column Name      | Data Type      | Description                                                                                      |
| ---------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `id`             | `UUID`         | **Primary Key.** A unique identifier for the script.                                             |
| `script_name`    | `String(255)`  | The name of the script.                                                                          |
| `script_url`     | `String(255)`  | The URL where the script can be accessed.                                                        |
| `script_extension` | `String(255)`  | The file extension of the script.                                                                |
| `script_info`    | `JSONB`        | A JSONB column for storing additional, unstructured information about the script.                |
| `created_at`     | `TIMESTAMP`    | The timestamp when the record was created. Defaults to the current time.                         |
| `updated_at`     | `TIMESTAMP`    | The timestamp when the record was last updated. Automatically updates on any modification.       |

## Constraints and Indexes

- **Unique Constraint:** A `UniqueConstraint` on `script_name` and `script_url` ensures that each combination is unique.
- **GIN Index:** A GIN index named `idx_scripts_info` is applied to the `script_info` column to optimize queries on the JSONB data.

## Relationships

- **`script_runs`:** A one-to-many relationship with the `script_runs` table, where one script can have multiple runs.
- **Association Tables:** The `scripts` table is linked to other entities like `experiments` and `datasets` through association tables.

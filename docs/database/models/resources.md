# Resources

The `resources` table stores information about data files and other resources associated with experiments.

## Table Schema

| Column Name               | Data Type   | Description                                                                                      |
| ------------------------- | ----------- | ------------------------------------------------------------------------------------------------ |
| `id`                      | `UUID`      | **Primary Key.** A unique identifier for the resource.                                           |
| `resource_uri`            | `String(255)` | The URI of the resource.                                                                         |
| `resource_file_name`      | `String(255)` | The file name of the resource.                                                                   |
| `is_external`             | `Boolean`   | A flag indicating whether the resource is external.                                              |
| `resource_experiment_id`  | `UUID`      | **Foreign Key.** References the `id` of the experiment to which the resource belongs.            |
| `resource_data_format_id` | `Integer`   | **Foreign Key.** References the `id` of the data format in the `data_formats` table.             |
| `resource_info`           | `JSONB`     | A JSONB column for storing additional, unstructured information about the resource.              |
| `created_at`              | `TIMESTAMP` | The timestamp when the record was created. Defaults to the current time.                         |
| `updated_at`              | `TIMESTAMP` | The timestamp when the record was last updated. Automatically updates on any modification.       |

## Constraints and Indexes

- **Unique Constraint:** A `UniqueConstraint` on `resource_uri` and `resource_file_name` ensures that each resource has a unique combination of URI and file name.
- **GIN Index:** A GIN index named `idx_resources_info` is applied to the `resource_info` column to optimize queries on the JSONB data.

## Relationships

- **`experiment`:** A many-to-one relationship with the `experiments` table.
- **`data_format`:** A many-to-one relationship with the `data_formats` table.

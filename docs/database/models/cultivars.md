# Cultivars

The `cultivars` table stores information about different plant cultivars used in experiments. Each row represents a unique cultivar, identified by its accession and population.

## Table Schema

| Column Name           | Data Type      | Description                                                                                      |
| --------------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `id`                  | `UUID`         | **Primary Key.** A unique identifier for the cultivar.                                           |
| `cultivar_accession`  | `String(255)`  | The accession identifier for the cultivar. This is part of a composite unique key.               |
| `cultivar_population` | `String(255)`  | The population name of the cultivar. This is part of a composite unique key.                     |
| `cultivar_info`       | `JSONB`        | A JSONB column for storing additional, unstructured information about the cultivar.              |
| `created_at`          | `TIMESTAMP`    | The timestamp when the record was created. Defaults to the current time.                         |
| `updated_at`          | `TIMESTAMP`    | The timestamp when the record was last updated. Automatically updates on any modification.       |

## Constraints and Indexes

- **Unique Constraint:** A `UniqueConstraint` on `cultivar_accession` and `cultivar_population` ensures that each combination of accession and population is unique within the table.
- **GIN Index:** A GIN index named `idx_cultivars_info` is applied to the `cultivar_info` column to optimize queries on the JSONB data.

## Relationships

The `cultivars` table is related to other tables in the database, such as `experiments` and `plots`, to associate experimental data with specific cultivars. These relationships are defined in the corresponding association tables.

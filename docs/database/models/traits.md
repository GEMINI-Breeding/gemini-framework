# Traits

The `traits` table stores information about the various traits being measured or observed.

## Table Schema

| Column Name    | Data Type      | Description                                                                                      |
| -------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `id`           | `UUID`         | **Primary Key.** A unique identifier for the trait.                                              |
| `trait_name`   | `String(255)`  | The name of the trait. This column has a unique constraint.                                      |
| `trait_units`  | `String(255)`  | The units in which the trait is measured.                                                        |
| `trait_level_id` | `Integer`   | **Foreign Key.** References the `id` of the trait level in the `trait_levels` table.             |
| `trait_metrics`| `JSONB`        | A JSONB column for storing additional, unstructured information about the trait metrics.         |
| `trait_info`   | `JSONB`        | A JSONB column for storing additional, unstructured information about the trait.                 |
| `created_at`   | `TIMESTAMP`    | The timestamp when the record was created. Defaults to the current time.                         |
| `updated_at`   | `TIMESTAMP`    | The timestamp when the record was last updated. Automatically updates on any modification.       |

## Constraints and Indexes

- **Unique Constraint:** A `UniqueConstraint` on `trait_name` ensures that each trait has a unique name.
- **GIN Index:** A GIN index named `idx_traits_info` is applied to the `trait_info` column to optimize queries on the JSONB data.

## Relationships

- **`trait_level`:** A many-to-one relationship with the `trait_levels` table.
- **Association Tables:** The `traits` table is linked to `experiments` and `datasets` through association tables.

# Trait Levels

The `trait_levels` table stores information about the different levels or categories for categorical traits.

## Table Schema

| Column Name      | Data Type      | Description                                                                                      |
| ---------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| `id`             | `Integer`      | **Primary Key.** A unique identifier for the trait level.                                        |
| `trait_level_name` | `String(255)`  | The name of the trait level. This column has a unique constraint.                                |
| `trait_level_info` | `JSONB`        | A JSONB column for storing additional, unstructured information about the trait level.           |
| `created_at`     | `TIMESTAMP`    | The timestamp when the record was created. Defaults to the current time.                         |
| `updated_at`     | `TIMESTAMP`    | The timestamp when the record was last updated. Automatically updates on any modification.       |

## Constraints and Indexes

- **Unique Constraint:** A `UniqueConstraint` on `trait_level_name` ensures that each trait level has a unique name.
- **GIN Index:** A GIN index named `idx_trait_levels_info` is applied to the `trait_level_info` column to optimize queries on the JSONB data.

## Relationships

- **`traits`:** A one-to-many relationship with the `traits` table, where one trait level can be associated with multiple traits.

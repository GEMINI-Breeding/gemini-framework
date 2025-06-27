# Sites

The `sites` table stores information about the physical locations where experiments are conducted.

## Table Schema

| Column Name  | Data Type      | Description                                                                                      |
| ------------ | -------------- | ------------------------------------------------------------------------------------------------ |
| `id`         | `UUID`         | **Primary Key.** A unique identifier for the site.                                               |
| `site_name`  | `String(255)`  | The name of the site.                                                                            |
| `site_city`  | `String(255)`  | The city where the site is located.                                                              |
| `site_state` | `String(255)`  | The state where the site is located.                                                             |
| `site_country` | `String(255)`  | The country where the site is located.                                                           |
| `site_info`  | `JSONB`        | A JSONB column for storing additional, unstructured information about the site.                  |
| `created_at` | `TIMESTAMP`    | The timestamp when the record was created. Defaults to the current time.                         |
| `updated_at` | `TIMESTAMP`    | The timestamp when the record was last updated. Automatically updates on any modification.       |

## Constraints and Indexes

- **Unique Constraint:** A `UniqueConstraint` on `site_name`, `site_city`, `site_state`, and `site_country` ensures that each site is unique.
- **GIN Index:** A GIN index named `idx_sites_info` is applied to the `site_info` column to optimize queries on the JSONB data.

## Relationships

- **Association Tables:** The `sites` table is linked to `experiments` through the `experiment_sites` association table.

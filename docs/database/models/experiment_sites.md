# Experiment Sites

The `experiment_sites` table links experiments to the sites where they are conducted.

## Table Schema

| Column Name     | Data Type | Description                                             |
| --------------- | --------- | ------------------------------------------------------- |
| `experiment_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `experiments.id`. |
| `site_id`       | `UUID`    | **Primary Key, Foreign Key.** Links to `sites.id`.       |

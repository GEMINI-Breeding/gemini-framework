# Experiment Datasets

The `experiment_datasets` table links experiments with their associated datasets.

## Table Schema

| Column Name     | Data Type | Description                                             |
| --------------- | --------- | ------------------------------------------------------- |
| `experiment_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `experiments.id`. |
| `dataset_id`    | `UUID`    | **Primary Key, Foreign Key.** Links to `datasets.id`.    |

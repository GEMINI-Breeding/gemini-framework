# Script Datasets

The `script_datasets` table links scripts to the datasets they process.

## Table Schema

| Column Name  | Data Type | Description                                           |
| ------------ | --------- | ----------------------------------------------------- |
| `script_id`  | `UUID`    | **Primary Key, Foreign Key.** Links to `scripts.id`.   |
| `dataset_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `datasets.id`.  |

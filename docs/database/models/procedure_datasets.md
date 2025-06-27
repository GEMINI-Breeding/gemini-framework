# Procedure Datasets

The `procedure_datasets` table links procedures to the datasets they are associated with.

## Table Schema

| Column Name    | Data Type | Description                                             |
| -------------- | --------- | ------------------------------------------------------- |
| `procedure_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `procedures.id`.  |
| `dataset_id`   | `UUID`    | **Primary Key, Foreign Key.** Links to `datasets.id`.   |

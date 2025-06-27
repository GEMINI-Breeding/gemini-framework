# Model Datasets

The `model_datasets` table links models to the datasets they use.

## Table Schema

| Column Name  | Data Type | Description                                          |
| ------------ | --------- | ---------------------------------------------------- |
| `model_id`   | `UUID`    | **Primary Key, Foreign Key.** Links to `models.id`.   |
| `dataset_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `datasets.id`. |

# Trait Datasets

The `trait_datasets` table links traits to the datasets that contain measurements for them.

## Table Schema

| Column Name  | Data Type | Description                                          |
| ------------ | --------- | ---------------------------------------------------- |
| `trait_id`   | `UUID`    | **Primary Key, Foreign Key.** Links to `traits.id`.   |
| `dataset_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `datasets.id`. |

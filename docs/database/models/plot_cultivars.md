# Plot Cultivars

The `plot_cultivars` table links plots to the cultivars planted in them.

## Table Schema

| Column Name   | Data Type | Description                                           |
| ------------- | --------- | ----------------------------------------------------- |
| `plot_id`     | `UUID`    | **Primary Key, Foreign Key.** Links to `plots.id`.     |
| `cultivar_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `cultivars.id`. |

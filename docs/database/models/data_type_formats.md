# Data Type Formats

The `data_type_formats` table links data types with their supported data formats.

## Table Schema

| Column Name    | Data Type | Description                                           |
| -------------- | --------- | ----------------------------------------------------- |
| `data_type_id` | `Integer` | **Primary Key, Foreign Key.** Links to `data_types.id`. |
| `data_format_id` | `Integer` | **Primary Key, Foreign Key.** Links to `data_formats.id`. |

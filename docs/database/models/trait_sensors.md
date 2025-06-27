# Trait Sensors

The `trait_sensors` table links traits to the sensors used to measure them.

## Table Schema

| Column Name | Data Type | Description                                         |
| ----------- | --------- | --------------------------------------------------- |
| `trait_id`  | `UUID`    | **Primary Key, Foreign Key.** Links to `traits.id`.  |
| `sensor_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `sensors.id`. |

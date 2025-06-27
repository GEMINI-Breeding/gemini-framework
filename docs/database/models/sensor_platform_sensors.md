# Sensor Platform Sensors

The `sensor_platform_sensors` table links sensor platforms to the sensors they carry.

## Table Schema

| Column Name        | Data Type | Description                                                  |
| ------------------ | --------- | ------------------------------------------------------------ |
| `sensor_platform_id` | `UUID`    | **Primary Key, Foreign Key.** Links to `sensor_platforms.id`. |
| `sensor_id`        | `UUID`    | **Primary Key, Foreign Key.** Links to `sensors.id`.          |

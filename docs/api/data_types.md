# Data Types API

### Description

A data type defines the type of data that is emitted and stored by the [Sensor](sensors.md). A data type can be associated with multiple [Data Formats](data_formats.md).

The following data types are pre-defined, along with their `data_type_id`:

| Data Type      | `data_type_id` |
| :------------- | :------------- |
| Default        | 0              |
| RGB            | 1              |
| NIR            | 2              |
| Thermal        | 3              |
| Multispectral  | 4              |
| Weather        | 5              |
| GPS            | 6              |
| Calibration    | 7              |
| Depth          | 8              |
| IMU            | 9              |
| Disparity      | 10             |
| Confidence     | 11             |


### Module

::: gemini.api.data_type
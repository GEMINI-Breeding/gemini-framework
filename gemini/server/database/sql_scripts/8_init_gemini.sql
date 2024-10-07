------------------------------------------------------------------------------
-- GEMINI Specific Data
------------------------------------------------------------------------------

-- Insert GEMINI Experiment
INSERT INTO gemini.experiments (
    experiment_name,
    experiment_info,
    experiment_start_date,
    experiment_end_date
)
VALUES (
    'GEMINI',
    '{"description": "GEMINI Experiment"}',
    '2020-01-01',
    '2025-12-31'
);

--- Insert 5 Seasons for GEMINI
INSERT INTO gemini.seasons (
    season_name,
    season_info,
    season_start_date,
    season_end_date,
    experiment_id
)
VALUES
    ('Season 1', '{"description": "Season 1"}', '2020-01-01', '2020-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
    ('Season 2', '{"description": "Season 2"}', '2021-01-01', '2021-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
    ('Season 3', '{"description": "Season 3"}', '2022-01-01', '2022-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
    ('Season 4', '{"description": "Season 4"}', '2023-01-01', '2023-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
    ('Season 5', '{"description": "Season 5"}', '2024-01-01', '2024-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'));

INSERT INTO gemini.sites (
    site_name,
    site_city,
    site_state,
    site_country,
    site_info
)
VALUES
    ('Davis', 'Davis', 'CA', 'USA', '{"description": "Davis Site for the GEMINI Project"}'),
    ('Kearney', 'Kearney', 'CA', 'USA', '{"description": "Kearney Site for the GEMINI Project"}');

--- Add the GEMINI Sites to the experiment
INSERT INTO gemini.experiment_sites (
    experiment_id,
    site_id
)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'), (SELECT id FROM gemini.sites WHERE site_name = 'Davis')),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'), (SELECT id FROM gemini.sites WHERE site_name = 'Kearney'));


--- Insert Sensor PLatforms
INSERT INTO gemini.sensor_platforms (
    sensor_platform_name,
    sensor_platform_info
)
VALUES
    ('Mineral T4 Rover', '{"manufacturer": "Mineral", "description": "Mineral T4 Rover"}'),
    ('Drone', '{"manufacturer": "Internal", "description": "Internal Drone"}'),
    ('AMIGA', '{"manufacturer": "farm-ng", "description": "Amiga is an all-electric micro-tractor designed to automate tasks in farms"}');

--- Add the Sensor Platforms to the experiment
INSERT INTO gemini.experiment_sensor_platforms (
    experiment_id,
    sensor_platform_id
)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'), (SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Mineral T4 Rover')),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'), (SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Drone')),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'), (SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'));

--- Create Sensors for T4 Rover
INSERT INTO gemini.sensors (
    sensor_name,
    sensor_type_id,
    sensor_data_type_id,
    sensor_data_format_id,
    sensor_info
)
VALUES 
    ('T4 Camera A', 1, 4, 9, '{"description": "camA"}'),
    ('T4 Camera B', 1, 4, 9, '{"description": "camB"}'),
    ('T4 Camera C', 1, 4, 9, '{"description": "camC"}'),
    ('T4 Camera D', 1, 4, 9, '{"description": "camD"}'),
    ('T4 Camera E', 1, 4, 9, '{"description": "camE"}'),
    ('T4 Camera F', 1, 4, 9, '{"description": "camF"}'),
    ('T4 Camera G', 1, 4, 9, '{"description": "camG"}'),
    ('T4 Camera H', 1, 4, 9, '{"description": "camH"}'),
    ('T4 Camera T', 1, 4, 9, '{"description": "camT"}');

INSERT INTO gemini.sensors (
    sensor_name,
    sensor_type_id,
    sensor_data_type_id,
    sensor_data_format_id,
    sensor_info
)
VALUES
    ('T4 IMU', 9, 1, 2, '{"description": "IMU Sensor on the T4 Rover"}'),
    ('T4 GPS', 6, 1, 2, '{"description": "GPS Sensor on the T4 Rover"}');

--- Add the Sensors to the T4 Rover
INSERT INTO gemini.sensor_platform_sensors (
    sensor_platform_id,
    sensor_id
)
VALUES
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Mineral T4 Rover'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'T4 Camera A')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Mineral T4 Rover'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'T4 Camera B')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Mineral T4 Rover'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'T4 Camera C')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Mineral T4 Rover'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'T4 Camera D')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Mineral T4 Rover'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'T4 Camera E')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Mineral T4 Rover'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'T4 Camera F')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Mineral T4 Rover'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'T4 Camera G')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Mineral T4 Rover'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'T4 Camera H')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Mineral T4 Rover'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'T4 Camera T')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Mineral T4 Rover'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'T4 IMU')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Mineral T4 Rover'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'T4 GPS'));

--- Create Sensors for Drone
INSERT INTO gemini.sensors (
    sensor_name,
    sensor_type_id,
    sensor_data_type_id,
    sensor_data_format_id,
    sensor_info
)
VALUES
    ('Drone iPhone RGB Camera', 1, 4, 8, '{"description": "iPhone RGB Camera on the Drone"}'),
    ('Drone iPhone Thermal Camera', 3, 4, 8, '{"description": "iPhone Thermal Camera on the Drone"}'),
    ('Drone iPhone Depth Sensor', 8, 4, 8, '{"description": "iPhone Depth Sensor on the Drone"}'),
    ('Drone iPhone Confidence', 0, 0, 0, '{"description": "iPhone Depth Confidence on the Drone"}');
    

--- Add the Sensors to the Drone
INSERT INTO gemini.sensor_platform_sensors (
    sensor_platform_id,
    sensor_id
)
VALUES
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Drone'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Drone iPhone RGB Camera')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Drone'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Drone iPhone Thermal Camera')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Drone'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Drone iPhone Depth Sensor')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Drone'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Drone iPhone Confidence'));


--- Create Sensors for AMIGA
INSERT INTO  gemini.sensors (
    sensor_name,
    sensor_type_id,
    sensor_data_type_id,
    sensor_data_format_id,
    sensor_info
)
VALUES 
    ('Oak1 RGB', 1, 4, 8, '{"description": "RGB source of Oak-D Camera on the AMIGA"}'),
    ('Oak2 RGB', 1, 4, 8, '{"description": "RGB source of Oak-D Camera on the AMIGA"}'),
    ('Oak1 Disparity', 10, 0, 0, '{"description": "Disparity Map source for the Oak-D Camera"}'),
    ('Oak2 Disparity', 10, 0, 0, '{"description": "Disparity Map source for the Oak-D Camera"}'),
    ('GPS Relative', 6, 1, 1, '{"description": "GPS Relative to the AMIGA"}'),
    ('GPS PVT', 6, 1, 1, '{"description": "Absolute GPS for the AMIGA"}');

--- Add the Sensors to the AMIGA
INSERT INTO gemini.sensor_platform_sensors (
    sensor_platform_id,
    sensor_id
)
VALUES
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Oak1 RGB')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Oak2 RGB')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Oak1 Disparity')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Oak2 Disparity')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'GPS Relative')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'GPS PVT'));


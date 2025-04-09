------------------------------------------------------------------------------
-- GEMINI Specific Data
------------------------------------------------------------------------------

-- Add GEMINI Experiment and Seasons
INSERT INTO gemini.experiments (experiment_name, experiment_info, experiment_start_date, experiment_end_date)
VALUES
    ('GEMINI', '{"description": "GEMINI Experiment"}', '2020-01-01', '2025-12-31');

-- Insert 5 Seasons for GEMINI
INSERT INTO gemini.seasons (season_name, season_info, season_start_date, season_end_date, experiment_id)
VALUES
    ('2020', '{"description": "Season 1"}', '2020-01-01', '2020-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
    ('2021', '{"description": "Season 2"}', '2021-01-01', '2021-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
    ('2022', '{"description": "Season 3"}', '2022-01-01', '2022-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
    ('2023', '{"description": "Season 4"}', '2023-01-01', '2023-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
    ('2024', '{"description": "Season 5"}', '2024-01-01', '2024-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'));

-- Insert GEMINI Sites
INSERT INTO gemini.sites (site_name, site_city, site_state, site_country, site_info)
VALUES
    ('Davis', 'Davis', 'CA', 'USA', '{"description": "Davis Site for the GEMINI Project"}'),
    ('Kearney', 'Kearney', 'CA', 'USA', '{"description": "Kearney Site for the GEMINI Project"}');

-- Add the GEMINI Sites to the experiment
INSERT INTO gemini.experiment_sites (experiment_id, site_id)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'), (SELECT id FROM gemini.sites WHERE site_name = 'Davis')),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'), (SELECT id FROM gemini.sites WHERE site_name = 'Kearney'));


-- Insert AMIGA Sensor Platform
INSERT INTO gemini.sensor_platforms (sensor_platform_name, sensor_platform_info)
VALUES
        ('AMIGA', '{"manufacturer": "farm-ng", "description": "Amiga is an all-electric micro-tractor designed to automate tasks in farms"}');

-- Add the AMIGA Sensor Platform to the experiment
INSERT INTO gemini.experiment_sensor_platforms (experiment_id, sensor_platform_id)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'), (SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'));


-- Add AMIGA Phone Sensors
INSERT INTO gemini.sensors (sensor_name, sensor_type_id, sensor_data_type_id, sensor_data_format_id, sensor_info)
VALUES
    ('AMIGA Phone Camera Metadata', 0, 1, 2, '{"description": "Camera Metadata on the AMIGA Phone"}'),
    ('AMIGA Phone RGB Camera', 1, 4, 8, '{"description": "RGB Camera on the AMIGA Phone"}'),
    ('AMIGA Phone Thermal Camera', 3, 4, 8, '{"description": "Thermal Camera on the AMIGA Phone"}'),
    ('AMIGA Phone Depth Sensor', 8, 4, 12, '{"description": "Depth Sensor on the AMIGA Phone"}'),
    ('AMIGA Phone Confidence', 11, 4, 12, '{"description": "Depth Confidence on the AMIGA Phone"}');


-- Add the AMIGA Phone Sensors to the AMIGA Sensor Platform
INSERT INTO gemini.sensor_platform_sensors (sensor_platform_id, sensor_id)
VALUES
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'AMIGA Phone Camera Metadata')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'AMIGA Phone RGB Camera')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'AMIGA Phone Thermal Camera')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'AMIGA Phone Depth Sensor')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'AMIGA Phone Confidence'));

-- Add the AMIGA Sensors to the Experiment
INSERT INTO gemini.experiment_sensors (experiment_id, sensor_id)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'AMIGA Phone Camera Metadata')),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'AMIGA Phone RGB Camera')),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'AMIGA Phone Thermal Camera')),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'AMIGA Phone Depth Sensor')),
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'AMIGA Phone Confidence'));


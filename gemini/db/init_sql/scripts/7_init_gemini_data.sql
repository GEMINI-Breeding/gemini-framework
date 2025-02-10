------------------------------------------------------------
-- Create the initial data for the database
------------------------------------------------------------

-- Insert Data Types
INSERT INTO gemini.data_types (id, data_type_name, data_type_info)
VALUES
    (0, 'Default', '{"description": "Default Data Type"}'), -- just values
    (1, 'Text', '{"description": "Text Data Type"}'),
    (2, 'Web', '{"description": "HTML Data Type"}'),
    (3, 'Document', '{"description": "Represents PDF, DOCX, DOC etc"}'),
    (4, 'Image', '{"description": "Image Data Type"}'),
    (5, 'Audio', '{"description": "Audio Data Type"}'),
    (6, 'Video', '{"description": "Video Data Type"}'),
    (7, 'Binary', '{"description": "Binary Data Type"}'),
    (8, 'Other', '{"description": "Other Data Type"}');

-- Insert Data Formats
INSERT INTO gemini.data_formats (id, data_format_name, data_format_mime_type, data_format_info)
VALUES
    (0, 'Default', 'application/octet-stream', '{"description": "Default Data Format"}'),
    (1, 'TXT', 'text/plain', '{"description": "Text Data Format"}'),
    (2, 'JSON', 'application/json', '{"description": "JSON Data Format"}'),
    (3, 'CSV', 'text/csv', '{"description": "CSV Data Format"}'),
    (4, 'TSV', 'text/tab-separated-values', '{"description": "TSV Data Format"}'),
    (5, 'XML', 'application/xml', '{"description": "XML Data Format"}'),
    (6, 'HTML', 'text/html', '{"description": "HTML Data Format"}'),
    (7, 'PDF', 'application/pdf', '{"description": "PDF Data Format"}'),
    (8, 'JPEG', 'image/jpeg', '{"description": "JPEG Data Format"}'),
    (9, 'PNG', 'image/png', '{"description": "PNG Data Format"}'),
    (10, 'GIF', 'image/gif', '{"description": "GIF Data Format"}'),
    (11, 'BMP', 'image/bmp', '{"description": "BMP Data Format"}'),
    (12, 'TIFF', 'image/tiff', '{"description": "TIFF Data Format"}'),
    (13, 'WAV', 'audio/wav', '{"description": "WAV Data Format"}'),
    (14, 'MP3', 'audio/mpeg', '{"description": "MP3 Data Format"}'),
    (15, 'MPEG', 'video/mpeg', '{"description": "MPEG Data Format"}'),
    (16, 'AVI', 'video/x-msvideo', '{"description": "AVI Data Format"}'),
    (17, 'MP4', 'video/mp4', '{"description": "MP4 Data Format"}'),
    (18, 'OGG', 'video/ogg', '{"description": "OGG Data Format"}'),
    (19, 'WEBM', 'video/webm', '{"description": "WEBM Data Format"}'),
    (20, 'NPY', 'application/octet-stream', '{"description": "Numpy Data Format"}');

-- Create Datatype Formats associations
INSERT INTO gemini.data_type_formats (data_type_id, data_format_id)
VALUES
    (0, 0), -- Default
    (1, 1), -- Text
    (1, 2), -- JSON
    (1, 3), -- CSV
    (1, 4), -- TSV
    (1, 5), -- XML
    (2, 6), -- HTML
    (3, 7), -- PDF
    (4, 8), -- JPEG
    (4, 9), -- PNG
    (4, 10), -- GIF
    (4, 11), -- BMP
    (4, 12), -- TIFF
    (5, 13), -- WAV
    (5, 14), -- MP3
    (6, 15), -- MPEG
    (6, 16), -- AVI
    (6, 17), -- MP4
    (6, 18), -- OGG
    (6, 19), -- WEBM
    (8, 20); -- Other

-- Insert Trait Levels
INSERT INTO gemini.trait_levels (id, trait_level_name, trait_level_info)
VALUES
    (0, 'Default', '{"description": "Default Trait Level"}'),
    (1, 'Plot', '{"description": "Default Plot Level"}'),
    (2, 'Plant', '{"description": "Default Plant Level"}');


-- Insert Predefined Sensor Types
INSERT INTO gemini.sensor_types (id, sensor_type_name, sensor_type_info)
VALUES
    (0, 'Default', '{"description": "Default Sensor Type"}'),
    (1, 'RGB', '{"description": "RGB Sensor"}'),
    (2, 'NIR', '{"description": "NIR Sensor"}'),
    (3, 'Thermal', '{"description": "Thermal Sensor"}'),
    (4, 'Multispectral', '{"description": "Multispectral Sensor"}'),
    (5, 'Weather', '{"description": "Weather Sensor"}'),
    (6, 'GPS', '{"description": "GPS Sensor"}'),
    (7, 'Calibration', '{"description": "Calibration Sensor"}'),
    (8, 'Depth', '{"description": "Depth Sensor"}'),
    (9, 'IMU', '{"description": "IMU Sensor"}'),
    (10, 'Disparity', '{"description": "Disparity Maps Source"}');


-- Insert Dataset Types
INSERT INTO gemini.dataset_types (id, dataset_type_name, dataset_type_info)
VALUES
    (0, 'Default', '{"description": "Default Dataset Type"}'),
    (1, 'Sensor', '{"description": "Sensor Dataset Type"}'),
    (2, 'Trait', '{"description": "Trait Dataset Type"}'),
    (3, 'Procedure', '{"description": "Procedure Dataset Type"}'),
    (4, 'Script', '{"description": "Script Dataset Type"}'),
    (5, 'Model', '{"description": "Model Dataset Type"}'),
    (6, 'Other', '{"description": "Other Dataset Type"}');


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
    ('2020', '{"description": "Season 1"}', '2020-01-01', '2020-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
    ('2021', '{"description": "Season 2"}', '2021-01-01', '2021-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
    ('2022', '{"description": "Season 3"}', '2022-01-01', '2022-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
    ('2023', '{"description": "Season 4"}', '2023-01-01', '2023-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
    ('2024', '{"description": "Season 5"}', '2024-01-01', '2024-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'));

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
    ('Oak0 Calibration', 7, 1, 2, '{"description": "Calibration for Oak-D Camera on the AMIGA"}'),
    ('Oak1 Calibration', 7, 1, 2, '{"description": "Calibration for Oak-D Camera on the AMIGA"}'),
    ('Oak2 Calibration', 7, 1, 2, '{"description": "Calibration for Oak-D Camera on the AMIGA"}'),
    ('Oak0 RGB', 1, 4, 8, '{"description": "RGB source of Oak-D Camera on the AMIGA"}'),
    ('Oak1 RGB', 1, 4, 8, '{"description": "RGB source of Oak-D Camera on the AMIGA"}'),
    ('Oak2 RGB', 1, 4, 8, '{"description": "RGB source of Oak-D Camera on the AMIGA"}'),
    ('Oak0 Disparity', 10, 0, 0, '{"description": "Disparity Map source for the Oak-D Camera"}'),
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
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Oak0 Calibration')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Oak1 Calibration')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Oak2 Calibration')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Oak0 RGB')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Oak1 RGB')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Oak2 RGB')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Oak0 Disparity')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Oak1 Disparity')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Oak2 Disparity')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'GPS Relative')),
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'AMIGA'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'GPS PVT'));


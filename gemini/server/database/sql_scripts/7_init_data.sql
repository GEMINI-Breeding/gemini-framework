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

------------------------------------------------------------
--- Dummy Data
------------------------------------------------------------

-- Insert Generic Experiment
INSERT INTO gemini.experiments (experiment_name, experiment_info, experiment_start_date, experiment_end_date)
VALUES
    ('Default', '{"description": "Default Experiment"}', '2020-01-01', '2025-12-31');

-- Insert Generic Seasons for each year of the Generic Experiment
INSERT INTO gemini.seasons (season_name, season_start_date, season_end_date, experiment_id)
VALUES
    ('2020', '2020-01-01', '2020-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'Default')),
    ('2021', '2021-01-01', '2021-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'Default')),
    ('2022', '2022-01-01', '2022-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'Default')),
    ('2023', '2023-01-01', '2023-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'Default')),
    ('2024', '2024-01-01', '2024-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'Default')),
    ('2025', '2025-01-01', '2025-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'Default'));

-- Insert Generic Sites
INSERT INTO gemini.sites (site_name, site_city, site_state, site_country, site_info)
VALUES
    ('Default', 'Default', 'Default', 'Default', '{"description": "Default Site"}');

INSERT INTO gemini.experiment_sites (experiment_id, site_id)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Default'), (SELECT id FROM gemini.sites WHERE site_name = 'Default'));

-- Insert Default Cultivar
INSERT INTO gemini.cultivars (cultivar_accession, cultivar_population, cultivar_info)
VALUES
    ('Default', 'Default', '{"description": "Default Cultivar"}');

INSERT INTO gemini.experiment_cultivars (experiment_id, cultivar_id)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Default'), (SELECT id FROM gemini.cultivars WHERE cultivar_accession = 'Default'));

-- Insert 100 Plots for Default Site and Default Experiment, each season with 50 plots all of Default Cultivar
DO $$
DECLARE
    ex_id UUID;
    se_id UUID;
    si_id UUID;
    cu_id UUID;
    plot_number INT;
    plot_row_number INT;
    plot_column_number INT;
BEGIN
    ex_id := (SELECT id FROM gemini.experiments WHERE experiment_name = 'Default');
    si_id := (SELECT id FROM gemini.sites WHERE site_name = 'Default');
    cu_id := (SELECT id FROM gemini.cultivars WHERE cultivar_accession = 'Default' AND cultivar_population = 'Default');
    plot_number := 1;
    plot_row_number := 1;
    plot_column_number := 1;

    FOR se_id IN SELECT id FROM gemini.seasons WHERE experiment_id = ex_id
    LOOP
        FOR plot_number IN 1..50
        LOOP
            INSERT INTO gemini.plots (plot_number, plot_row_number, plot_column_number, experiment_id, site_id, season_id, plot_info)
            VALUES
                (plot_number, plot_row_number, plot_column_number, ex_id, si_id, se_id, '{"description": "Default Plot"}');
            plot_column_number := plot_column_number + 1;
            
            IF plot_column_number > 10 THEN
                plot_column_number := 1;
                plot_row_number := plot_row_number + 1;
            END IF;

            plot_row_number := plot_row_number + 1;

            IF plot_row_number > 10 THEN
                plot_row_number := 1;
            END IF;
        END LOOP;
    END LOOP;
END $$;

-- For each of the above plots, create a plot_cultivars entry that associates the plot with the default cultivar
INSERT INTO gemini.plot_cultivars (plot_id, cultivar_id)
SELECT p.id, (SELECT id FROM gemini.cultivars WHERE cultivar_accession = 'Default' AND cultivar_population = 'Default')
FROM gemini.plots p
WHERE p.experiment_id = (SELECT id FROM gemini.experiments WHERE experiment_name = 'Default');

-- Insert Generic Models
INSERT INTO gemini.models (model_name, model_info)
VALUES
    ('Default', '{"description": "Default Model"}');

-- Insert Generic Model Runs
INSERT INTO gemini.model_runs (model_id, model_run_info)
VALUES
    ((SELECT id FROM gemini.models WHERE model_name = 'Default'), '{"description": "Default Model Run 1"}'),
    ((SELECT id FROM gemini.models WHERE model_name = 'Default'), '{"description": "Default Model Run 2"}'),
    ((SELECT id FROM gemini.models WHERE model_name = 'Default'), '{"description": "Default Model Run 3"}'),
    ((SELECT id FROM gemini.models WHERE model_name = 'Default'), '{"description": "Default Model Run 4"}'),
    ((SELECT id FROM gemini.models WHERE model_name = 'Default'), '{"description": "Default Model Run 5"}');

INSERT INTO gemini.experiment_models (experiment_id, model_id)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Default'), (SELECT id FROM gemini.models WHERE model_name = 'Default'));

-- Insert Generic Default Trait
INSERT INTO gemini.traits (trait_name, trait_info, trait_units, trait_level_id)
VALUES
    ('Default', '{"description": "Default Trait"}', 'Default Units', (SELECT id FROM gemini.trait_levels WHERE trait_level_name = 'Default'));

INSERT INTO gemini.experiment_traits (experiment_id, trait_id)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Default'), (SELECT id FROM gemini.traits WHERE trait_name = 'Default'));

-- Insert Default Sensor Platform
INSERT INTO gemini.sensor_platforms (sensor_platform_name, sensor_platform_info)
VALUES
    ('Default', '{"description": "Default Sensor Platform"}');

INSERT INTO gemini.experiment_sensor_platforms (experiment_id, sensor_platform_id)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Default'), (SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Default'));

-- Insert Default Sensor
INSERT INTO gemini.sensors (sensor_name, sensor_info, sensor_type_id)
VALUES
    ('Default', '{"description": "Default Sensor"}', (SELECT id FROM gemini.sensor_types WHERE sensor_type_name = 'Default'));

INSERT INTO gemini.experiment_sensors (experiment_id, sensor_id)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Default'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Default'));

INSERT INTO gemini.sensor_platform_sensors (sensor_platform_id, sensor_id)
VALUES
    ((SELECT id FROM gemini.sensor_platforms WHERE sensor_platform_name = 'Default'), (SELECT id FROM gemini.sensors WHERE sensor_name = 'Default'));

-- Insert Default Resources
INSERT INTO gemini.resources (resource_uri, resource_file_name, is_external, resource_experiment_id, resource_data_format_id, resource_info)
VALUES
    ('https://www.google.com', 'google.html', TRUE, (SELECT id FROM gemini.experiments WHERE experiment_name = 'Default'), (SELECT id FROM gemini.data_formats WHERE data_format_name = 'HTML'), '{"description": "Default Resource"}');

-- Insert Default Script
INSERT INTO gemini.scripts (script_name, script_url, script_extension, script_info)
VALUES
    ('Default', 'https://www.google.com', 'html', '{"description": "Default Script"}');

-- Insert 5 Script Runs for this script
INSERT INTO gemini.script_runs (script_id, script_run_info)
VALUES
    ((SELECT id FROM gemini.scripts WHERE script_name = 'Default'), '{"description": "Default Script Run 1"}'),
    ((SELECT id FROM gemini.scripts WHERE script_name = 'Default'), '{"description": "Default Script Run 2"}'),
    ((SELECT id FROM gemini.scripts WHERE script_name = 'Default'), '{"description": "Default Script Run 3"}'),
    ((SELECT id FROM gemini.scripts WHERE script_name = 'Default'), '{"description": "Default Script Run 4"}'),
    ((SELECT id FROM gemini.scripts WHERE script_name = 'Default'), '{"description": "Default Script Run 5"}');

INSERT INTO gemini.experiment_scripts (experiment_id, script_id)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Default'), (SELECT id FROM gemini.scripts WHERE script_name = 'Default'));

-- Insert Default Procedure
INSERT INTO gemini.procedures (procedure_name, procedure_info)
VALUES
    ('Default', '{"description": "Default Procedure"}');

INSERT INTO gemini.experiment_procedures (experiment_id, procedure_id)
VALUES
    ((SELECT id FROM gemini.experiments WHERE experiment_name = 'Default'), (SELECT id FROM gemini.procedures WHERE procedure_name = 'Default'));

-- Insert 5 Procedure Runs for this procedure
INSERT INTO gemini.procedure_runs (procedure_id, procedure_run_info)
VALUES
    ((SELECT id FROM gemini.procedures WHERE procedure_name = 'Default'), '{"description": "Default Procedure Run 1"}'),
    ((SELECT id FROM gemini.procedures WHERE procedure_name = 'Default'), '{"description": "Default Procedure Run 2"}'),
    ((SELECT id FROM gemini.procedures WHERE procedure_name = 'Default'), '{"description": "Default Procedure Run 3"}'),
    ((SELECT id FROM gemini.procedures WHERE procedure_name = 'Default'), '{"description": "Default Procedure Run 4"}'),
    ((SELECT id FROM gemini.procedures WHERE procedure_name = 'Default'), '{"description": "Default Procedure Run 5"}');

-- Create 3 Default Datasets
INSERT INTO gemini.datasets (dataset_name, collection_date, dataset_info, dataset_type_id)
VALUES
    ('Default Dataset 1', '2020-01-01', '{"description": "Default Dataset 1"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Other')),
    ('Default Dataset 2', '2021-01-01', '{"description": "Default Dataset 2"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Other')),
    ('Default Dataset 3', '2022-01-01', '{"description": "Default Dataset 3"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Other'));

-- Create 3 Datasets for Default Trait
INSERT INTO gemini.datasets (dataset_name, collection_date, dataset_info, dataset_type_id)
VALUES
    ('Default Trait Dataset 1', '2020-01-01', '{"description": "Default Dataset 1"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Trait')),
    ('Default Trait Dataset 2', '2021-01-01', '{"description": "Default Dataset 2"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Trait')),
    ('Default Trait Dataset 3', '2022-01-01', '{"description": "Default Dataset 3"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Trait'));

INSERT INTO gemini.trait_datasets (trait_id, dataset_id)
VALUES
    ((SELECT id FROM gemini.traits WHERE trait_name = 'Default'), (SELECT id FROM gemini.datasets WHERE dataset_name = 'Default Trait Dataset 1')),
    ((SELECT id FROM gemini.traits WHERE trait_name = 'Default'), (SELECT id FROM gemini.datasets WHERE dataset_name = 'Default Trait Dataset 2')),
    ((SELECT id FROM gemini.traits WHERE trait_name = 'Default'), (SELECT id FROM gemini.datasets WHERE dataset_name = 'Default Trait Dataset 3'));

-- Create 3 Datasets for Default Sensor
INSERT INTO gemini.datasets (dataset_name, collection_date, dataset_info, dataset_type_id)
VALUES
    ('Default Sensor Dataset 1', '2020-01-01', '{"description": "Default Dataset 1"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Sensor')),
    ('Default Sensor Dataset 2', '2021-01-01', '{"description": "Default Dataset 2"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Sensor')),
    ('Default Sensor Dataset 3', '2022-01-01', '{"description": "Default Dataset 3"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Sensor'));

INSERT INTO gemini.sensor_datasets (sensor_id, dataset_id)
VALUES
    ((SELECT id FROM gemini.sensors WHERE sensor_name = 'Default'), (SELECT id FROM gemini.datasets WHERE dataset_name = 'Default Sensor Dataset 1')),
    ((SELECT id FROM gemini.sensors WHERE sensor_name = 'Default'), (SELECT id FROM gemini.datasets WHERE dataset_name = 'Default Sensor Dataset 2')),
    ((SELECT id FROM gemini.sensors WHERE sensor_name = 'Default'), (SELECT id FROM gemini.datasets WHERE dataset_name = 'Default Sensor Dataset 3'));

-- Create 3 Datasets for Default Procedure
INSERT INTO gemini.datasets (dataset_name, collection_date, dataset_info, dataset_type_id)
VALUES
    ('Default Procedure Dataset 1', '2020-01-01', '{"description": "Default Dataset 1"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Procedure')),
    ('Default Procedure Dataset 2', '2021-01-01', '{"description": "Default Dataset 2"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Procedure')),
    ('Default Procedure Dataset 3', '2022-01-01', '{"description": "Default Dataset 3"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Procedure'));

INSERT INTO gemini.procedure_datasets (procedure_id, dataset_id)
VALUES
    ((SELECT id FROM gemini.procedures WHERE procedure_name = 'Default'), (SELECT id FROM gemini.datasets WHERE dataset_name = 'Default Procedure Dataset 1')),
    ((SELECT id FROM gemini.procedures WHERE procedure_name = 'Default'), (SELECT id FROM gemini.datasets WHERE dataset_name = 'Default Procedure Dataset 2')),
    ((SELECT id FROM gemini.procedures WHERE procedure_name = 'Default'), (SELECT id FROM gemini.datasets WHERE dataset_name = 'Default Procedure Dataset 3'));

-- Create 3 Datasets for Default Script
INSERT INTO gemini.datasets (dataset_name, collection_date, dataset_info, dataset_type_id)
VALUES
    ('Default Script Dataset 1', '2020-01-01', '{"description": "Default Dataset 1"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Script')),
    ('Default Script Dataset 2', '2021-01-01', '{"description": "Default Dataset 2"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Script')),
    ('Default Script Dataset 3', '2022-01-01', '{"description": "Default Dataset 3"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Script'));

INSERT INTO gemini.script_datasets (script_id, dataset_id)
VALUES
    ((SELECT id FROM gemini.scripts WHERE script_name = 'Default'), (SELECT id FROM gemini.datasets WHERE dataset_name = 'Default Script Dataset 1')),
    ((SELECT id FROM gemini.scripts WHERE script_name = 'Default'), (SELECT id FROM gemini.datasets WHERE dataset_name = 'Default Script Dataset 2')),
    ((SELECT id FROM gemini.scripts WHERE script_name = 'Default'), (SELECT id FROM gemini.datasets WHERE dataset_name = 'Default Script Dataset 3'));

-- Create 3 Datasets for Default Model
INSERT INTO gemini.datasets (dataset_name, collection_date, dataset_info, dataset_type_id)
VALUES
    ('Default Model Dataset 1', '2020-01-01', '{"description": "Default Dataset 1"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Model')),
    ('Default Model Dataset 2', '2021-01-01', '{"description": "Default Dataset 2"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Model')),
    ('Default Model Dataset 3', '2022-01-01', '{"description": "Default Dataset 3"}', (SELECT id FROM gemini.dataset_types WHERE dataset_type_name = 'Model'));

INSERT INTO gemini.model_datasets (model_id, dataset_id)
VALUES
    ((SELECT id FROM gemini.models WHERE model_name = 'Default'), (SELECT id FROM gemini.datasets WHERE dataset_name = 'Default Model Dataset 1')),
    ((SELECT id FROM gemini.models WHERE model_name = 'Default'), (SELECT id FROM gemini.datasets WHERE dataset_name = 'Default Model Dataset 2')),
    ((SELECT id FROM gemini.models WHERE model_name = 'Default'), (SELECT id FROM gemini.datasets WHERE dataset_name = 'Default Model Dataset 3'));

--- Assign all datasets to Experiment 'Default'
INSERT INTO gemini.experiment_datasets (experiment_id, dataset_id)
SELECT (SELECT id FROM gemini.experiments WHERE experiment_name = 'Default'), id
FROM gemini.datasets;


-- Insert Test Sensor Records
DO $$
DECLARE
    i INTEGER := 0;
BEGIN
    WHILE i < 1000 LOOP
        INSERT INTO gemini.sensor_records (
            timestamp,
            sensor_id,
            sensor_name,
            sensor_data,
            record_info
        ) VALUES (
            NOW() + (i || ' seconds')::INTERVAL,
            (SELECT id FROM gemini.sensors WHERE sensor_name = 'Default'),
            'Default',
            json_build_object('value', random()),
            '{"experiment": "Default", "site": "Default", "season": "Default"}'
        );
        i := i + 1;
    END LOOP;
END $$;

-- Insert Test Trait Records
DO $$
DECLARE
    i INTEGER := 0;
BEGIN
    WHILE i < 1000 LOOP
        INSERT INTO gemini.trait_records (
            timestamp,
            trait_name,
            trait_value,
            record_info
        ) VALUES (
            NOW() + (i || ' seconds')::INTERVAL,
            'Default',
            random(),
            '{"experiment": "Default", "site": "Default", "season": "Default"}'
        );
        i := i + 1;
    END LOOP;
END $$;

-- Insert Test Dataset Records
DO $$
DECLARE
    i INTEGER := 0;
BEGIN
    WHILE i < 1000 LOOP
        INSERT INTO gemini.dataset_records (
            timestamp,
            dataset_name,
            dataset_data,
            record_info
        ) VALUES (
            NOW() + (i || ' seconds')::INTERVAL,
            'Default',
            json_build_object('value', random()),
            '{"experiment": "Default", "site": "Default", "season": "Default"}'
        );
        i := i + 1;
    END LOOP;
END $$;

-- Insert Test Model Records
DO $$
DECLARE
    i INTEGER := 0;
BEGIN
    WHILE i < 1000 LOOP
        INSERT INTO gemini.model_records (
            timestamp,
            model_name,
            model_data,
            record_info
        ) VALUES (
            NOW() + (i || ' seconds')::INTERVAL,
            'Default',
            json_build_object('value', random()),
            '{"experiment": "Default", "site": "Default", "season": "Default"}'
        );
        i := i + 1;
    END LOOP;
END $$;

-- Insert Test Procedure Records
DO $$
DECLARE
    i INTEGER := 0;
BEGIN
    WHILE i < 1000 LOOP
        INSERT INTO gemini.procedure_records (
            timestamp,
            procedure_name,
            procedure_data,
            record_info
        ) VALUES (
            NOW() + (i || ' seconds')::INTERVAL,
            'Default',
            json_build_object('value', random()),
            '{"experiment": "Default", "site": "Default", "season": "Default"}'
        );
        i := i + 1;
    END LOOP;
END $$;

-- Insert Test Script Records
DO $$
DECLARE
    i INTEGER := 0;
BEGIN
    WHILE i < 1000 LOOP
        INSERT INTO gemini.script_records (
            timestamp,
            script_name,
            script_data,
            record_info
        ) VALUES (
            NOW() + (i || ' seconds')::INTERVAL,
            'Default',
            json_build_object('value', random()),
            '{"experiment": "Default", "site": "Default", "season": "Default"}'
        );
        i := i + 1;
    END LOOP;
END $$;




-- ------------------------------------------------------------
-- -- Insert the initial data for the database
-- ------------------------------------------------------------

-- -- Insert GEMINI Experiment
-- INSERT INTO gemini.experiments (experiment_name, experiment_info, experiment_start_date, experiment_end_date)
-- VALUES
--     ('GEMINI', '{"description": "GEMINI Experiment"}', '2020-01-01', '2025-12-31');


-- -- Insert Seasons for each year of the GEMINI Experiment
-- INSERT INTO gemini.seasons (season_name, season_start_date, season_end_date, experiment_id)
-- VALUES
--     ('2020', '2020-01-01', '2020-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
--     ('2021', '2021-01-01', '2021-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
--     ('2022', '2022-01-01', '2022-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
--     ('2023', '2023-01-01', '2023-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
--     ('2024', '2024-01-01', '2024-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI')),
--     ('2025', '2025-01-01', '2025-12-31', (SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'));

-- -- Insert GEMINI Sites
-- INSERT INTO gemini.sites (site_name, site_city, site_state, site_country, site_info)
-- VALUES
--     ('Davis', 'Davis', 'CA', 'USA', '{"description": "Davis Site"}'),
--     ('Kearney', 'Kearney', 'CA', 'USA', '{"description": "Kearney Site"}');

-- INSERT INTO gemini.experiment_sites (experiment_id, site_id)
-- VALUES
--     ((SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'), (SELECT id FROM gemini.sites WHERE site_name = 'Davis')),
--     ((SELECT id FROM gemini.experiments WHERE experiment_name = 'GEMINI'), (SELECT id FROM gemini.sites WHERE site_name = 'Kearney'));


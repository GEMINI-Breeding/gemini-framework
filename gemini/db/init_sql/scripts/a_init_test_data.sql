INSERT INTO gemini.experiments (id, experiment_name, experiment_info, experiment_start_date, experiment_end_date, created_at, updated_at)
VALUES 
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'Test Experiment 1', '{"description": "This is a test experiment"}', '2020-01-01', '2020-12-31', NOW(), NOW());


INSERT INTO gemini.seasons (id, experiment_id, season_name, season_info, season_start_date, season_end_date, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'Test Season 1', '{"description": "This is a test season"}', '2020-01-01', '2020-12-31', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'Test Season 2', '{"description": "This is a test season"}', '2020-01-01', '2020-12-31', NOW(), NOW());


INSERT INTO gemini.sites (id, site_name, site_city, site_state, site_country, site_info, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'Test Site 1', 'Test City 1', 'Test State 1', 'Test Country 1', '{"description": "This is a test site"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'Test Site 2', 'Test City 2', 'Test State 2', 'Test Country 2', '{"description": "This is a test site"}', NOW(), NOW());


INSERT INTO gemini.cultivars (id, cultivar_accession, cultivar_population, cultivar_info, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'Test Accession 1', 'Test Population 1', '{"description": "This is a test cultivar"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'Test Accession 2', 'Test Population 2', '{"description": "This is a test cultivar"}', NOW(), NOW());


INSERT INTO gemini.plots (id, experiment_id, season_id, site_id, plot_number, plot_row_number, plot_column_number, plot_geometry_info, plot_info, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 1, 1, 1, '{"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]}', '{"description": "This is a test plot"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 2, 2, 2, '{"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]}', '{"description": "This is a test plot"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b5', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 3, 3, 3, '{"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]}', '{"description": "This is a test plot"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b6', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 4, 4, 4, '{"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]}', '{"description": "This is a test plot"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b7', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 5, 5, 5, '{"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]}', '{"description": "This is a test plot"}', NOW(), NOW());



INSERT INTO gemini.plants (id, plot_id, plant_number, plant_info, cultivar_id, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 1, '{"description": "This is a test plant"}', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 2, '{"description": "This is a test plant"}', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', NOW(), NOW());



INSERT INTO gemini.traits (id, trait_name, trait_units, trait_level_id, trait_metrics, trait_info, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'Test Trait 1', 'Test Units 1', 1, '{"metric1": "value1", "metric2": "value2"}', '{"description": "This is a test trait"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'Test Trait 2', 'Test Units 2', 2, '{"metric1": "value1", "metric2": "value2"}', '{"description": "This is a test trait"}', NOW(), NOW());


INSERT INTO gemini.sensor_platforms (id, sensor_platform_name, sensor_platform_info, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'Test Sensor Platform 1', '{"description": "This is a test sensor platform"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'Test Sensor Platform 2', '{"description": "This is a test sensor platform"}', NOW(), NOW());


INSERT INTO gemini.sensors (id, sensor_name, sensor_type_id, sensor_data_type_id, sensor_data_format_id, sensor_info, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'Test Sensor 1', 1, 1, 1, '{"description": "This is a test sensor"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'Test Sensor 2', 2, 2, 2, '{"description": "This is a test sensor"}', NOW(), NOW());


INSERT INTO gemini.resources (id, resource_uri, resource_file_name, is_external, resource_experiment_id, resource_data_format_id, resource_info, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'http://example.com/resource1', 'resource1', FALSE, 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 1, '{"description": "This is a test resource"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'http://example.com/resource2', 'resource2', FALSE, 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 2, '{"description": "This is a test resource"}', NOW(), NOW());


INSERT INTO gemini.scripts (id, script_name, script_url, script_extension, script_info, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'Test Script 1', 'http://example.com/script1', '.sh', '{"description": "This is a test script"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'Test Script 2', 'http://example.com/script2', '.py', '{"description": "This is a test script"}', NOW(), NOW());


INSERT INTO gemini.script_runs (id, script_id, script_run_info, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', '{"description": "This is a test script run"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', '{"description": "This is a test script run"}', NOW(), NOW());


INSERT INTO gemini.models (id, model_name, model_url, model_info, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'Test Model 1', 'http://example.com/model1', '{"description": "This is a test model"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'Test Model 2', 'http://example.com/model2', '{"description": "This is a test model"}', NOW(), NOW());


INSERT INTO gemini.model_runs (id, model_id, model_run_info, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', '{"description": "This is a test model run"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', '{"description": "This is a test model run"}', NOW(), NOW());


INSERT INTO gemini.procedures (id, procedure_name, procedure_info, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'Test Procedure 1', '{"description": "This is a test procedure"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'Test Procedure 2', '{"description": "This is a test procedure"}', NOW(), NOW());


INSERT INTO gemini.procedure_runs (id, procedure_id, procedure_run_info, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', '{"description": "This is a test procedure run"}', NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', 'f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', '{"description": "This is a test procedure run"}', NOW(), NOW());


INSERT INTO gemini.datasets (id, collection_date, dataset_name, dataset_info, dataset_type_id, created_at, updated_at)
VALUES
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b3', '2020-01-01', 'Test Dataset 1', '{"description": "This is a test dataset"}', 1, NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b4', '2020-01-01', 'Test Dataset 2', '{"description": "This is a test dataset"}', 2, NOW(), NOW()),
('f4b3b3b3-3b3b-4b4b-b3b3-b3b3b3b3b3b5', '2020-01-01', 'Test Dataset 3', '{"description": "This is a test dataset"}', 1, NOW(), NOW());
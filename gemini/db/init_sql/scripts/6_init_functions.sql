------------------------------------------------------------------------------
-- Database Functions and Procedures
------------------------------------------------------------------------------

-- Function to create a new plot if it does not exist
CREATE OR REPLACE FUNCTION gemini.create_plot_if_not_exists(
    exp_name TEXT,
    sea_name TEXT,
    sit_name TEXT,
    plt_num INTEGER,
    plt_row_num INTEGER,
    plt_col_num INTEGER
) RETURNS UUID AS $$
DECLARE
    exp_id UUID;
    sea_id UUID;
    sit_id UUID;
    pl_id UUID;
BEGIN
    -- Check if the experiment exists
    SELECT id INTO exp_id FROM gemini.experiments WHERE experiment_name = exp_name;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Experiment % does not exist', exp_name;
    END IF;

    -- Check if the season exists for the experiment
    SELECT id INTO sea_id FROM gemini.seasons WHERE season_name = sea_name AND experiment_id = exp_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Season % does not exist for experiment %', sea_name, exp_name;
    END IF;

    -- Check if the site exists
    SELECT id INTO sit_id FROM gemini.sites WHERE site_name = sit_name;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Site % does not exist', sit_name;
    END IF;

    -- Check if the plot already exists
    SELECT id INTO pl_id FROM gemini.plots 
    WHERE experiment_id = exp_id 
      AND season_id = sea_id 
      AND site_id = sit_id 
      AND plot_number = plt_num
      AND plot_row_number = plt_row_num
      AND plot_column_number = plt_col_num;

    IF NOT FOUND THEN
        -- If not, create a new plot
        INSERT INTO gemini.plots (experiment_id, season_id, site_id, plot_number, plot_row_number, plot_column_number)
        VALUES (exp_id, sea_id, sit_id, plt_num, plt_row_num, plt_col_num)
        RETURNING id INTO pl_id;
    END IF;

    -- Return the plot ID
    RETURN pl_id;
END;
$$ LANGUAGE plpgsql;

-- Function to create a dataset for an experiment if it does not exist
CREATE OR REPLACE FUNCTION gemini.create_dataset_if_not_exists(
    dat_name TEXT,
    dat_type_id INTEGER,
    col_date DATE,
    exp_name TEXT
) RETURNS UUID AS $$
DECLARE
    dat_id UUID;
    exp_id UUID;
BEGIN
    -- Check if the experiment exists
    SELECT id INTO exp_id FROM gemini.experiments WHERE experiment_name = exp_name;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Experiment % does not exist', exp_name;
    END IF;


    -- Check if the dataset already exists
    SELECT id INTO dat_id FROM gemini.datasets WHERE dataset_name = dat_name;
    IF NOT FOUND THEN
        -- If not, create a new dataset
        INSERT INTO gemini.datasets (dataset_name, dataset_type_id, collection_date)
        VALUES (dat_name, dat_type_id, col_date)
        RETURNING id INTO dat_id;
    END IF;

    -- Check if the dataset is already associated with the experiment
    IF NOT EXISTS (
        SELECT 1
        FROM gemini.experiment_datasets
        WHERE experiment_id = exp_id AND dataset_id = dat_id
    ) THEN
        -- If not, associate the dataset with the experiment
        INSERT INTO gemini.experiment_datasets (experiment_id, dataset_id)
        VALUES (exp_id, dat_id);
    END IF;

    -- Return the dataset ID
    RETURN dat_id;
END;
$$ LANGUAGE plpgsql;

-- Function to check the validity of a dataset, experiment, season, and site combination using names

CREATE OR REPLACE FUNCTION gemini.check_dataset_validity(
    dat_name TEXT,
    exp_name TEXT,
    sea_name TEXT,
    sit_name TEXT
) RETURNS BOOLEAN AS $$
BEGIN
    -- Check if the combination is a part of gemini.valid_datasets_combinations_view
    IF EXISTS (
        SELECT 1
        FROM gemini.valid_dataset_combinations_view vdc
        WHERE vdc.dataset_name = dat_name
          AND vdc.experiment_name = exp_name
          AND vdc.season_name = sea_name
          AND vdc.site_name = sit_name
    ) THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to populate ID fields in dataset_records table based on names
CREATE OR REPLACE FUNCTION gemini.populate_dataset_record_ids()
RETURNS TRIGGER AS $$
DECLARE
    dat_id UUID;
    exp_id UUID;
    sea_id UUID;
    sit_id UUID;
BEGIN
    -- Check if the dataset, experiment, season, and site are valid
    IF NOT gemini.check_dataset_validity(NEW.dataset_name, NEW.experiment_name, NEW.season_name, NEW.site_name) THEN
        RAISE EXCEPTION 'Invalid dataset, experiment, season, or site combination';
    END IF;

    -- Get the IDs based on names
    SELECT id INTO dat_id FROM gemini.datasets WHERE dataset_name = NEW.dataset_name;
    SELECT id INTO exp_id FROM gemini.experiments WHERE experiment_name = NEW.experiment_name;
    SELECT id INTO sea_id FROM gemini.seasons WHERE season_name = NEW.season_name AND experiment_id = exp_id;
    SELECT id INTO sit_id FROM gemini.sites WHERE site_name = NEW.site_name;

    -- Update the record with the IDs
    NEW.dataset_id := dat_id;
    NEW.experiment_id := exp_id;
    NEW.season_id := sea_id;
    NEW.site_id := sit_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_populate_dataset_record_ids
BEFORE INSERT OR UPDATE ON gemini.dataset_records
FOR EACH ROW
EXECUTE FUNCTION gemini.populate_dataset_record_ids();

-- Function to check the validity of a procedure, dataset, experiment, season, and site combination using names
CREATE OR REPLACE FUNCTION gemini.check_procedure_validity(
    pro_name TEXT,
    dat_name TEXT,
    exp_name TEXT,
    sea_name TEXT,
    sit_name TEXT
) RETURNS BOOLEAN AS $$
BEGIN
    -- Check if dataset with dat_name exists, if not, create it
    IF NOT EXISTS (
        SELECT 1
        FROM gemini.datasets
        WHERE dataset_name = dat_name
    ) THEN
        PERFORM gemini.create_dataset_if_not_exists(dat_name, 3, CURRENT_DATE, exp_name);
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM gemini.procedure_datasets_view pdv
        WHERE pdv.procedure_name = pro_name
            AND pdv.dataset_name = dat_name
    )
    THEN
        INSERT INTO gemini.procedure_datasets (
            procedure_id,
            dataset_id
        )
        VALUES (
            (SELECT id FROM gemini.procedures WHERE procedure_name = pro_name),
            (SELECT id FROM gemini.datasets WHERE dataset_name = dat_name)
        );
    END IF;
    
    -- Check if the combination of valid_procedure_dataset_combinations_view exists
    IF EXISTS (
        SELECT 1
        FROM gemini.valid_procedure_dataset_combinations_view vpdc
        WHERE vpdc.procedure_name = pro_name
          AND vpdc.dataset_name = dat_name
          AND vpdc.experiment_name = exp_name
          AND vpdc.season_name = sea_name
          AND vpdc.site_name = sit_name
    ) THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

    
-- Function to populate ID fields in procedure_records table based on names
CREATE OR REPLACE FUNCTION gemini.populate_procedure_record_ids()
RETURNS TRIGGER AS $$
DECLARE
    pro_id UUID;
    dat_id UUID;
    exp_id UUID;
    sea_id UUID;
    sit_id UUID;
BEGIN
    -- Check if the procedure, dataset, experiment, season, and site are valid
    IF NOT gemini.check_procedure_validity(NEW.procedure_name, NEW.dataset_name, NEW.experiment_name, NEW.season_name, NEW.site_name) THEN
        RAISE EXCEPTION 'Invalid procedure, dataset, experiment, season, or site combination';
    END IF;

    -- Get the IDs based on names
    SELECT id INTO pro_id FROM gemini.procedures WHERE procedure_name = NEW.procedure_name;
    SELECT id INTO dat_id FROM gemini.datasets WHERE dataset_name = NEW.dataset_name;
    SELECT id INTO exp_id FROM gemini.experiments WHERE experiment_name = NEW.experiment_name;
    SELECT id INTO sea_id FROM gemini.seasons WHERE season_name = NEW.season_name AND experiment_id = exp_id;
    SELECT id INTO sit_id FROM gemini.sites WHERE site_name = NEW.site_name;

    -- Update the record with the IDs
    NEW.procedure_id := pro_id;
    NEW.dataset_id := dat_id;
    NEW.experiment_id := exp_id;
    NEW.season_id := sea_id;
    NEW.site_id := sit_id;

    RETURN NEW;
END;

$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_populate_procedure_record_ids
BEFORE INSERT OR UPDATE ON gemini.procedure_records
FOR EACH ROW
EXECUTE FUNCTION gemini.populate_procedure_record_ids();

-- Function to check the validity of a script, dataset, experiment, season, and site combination using names
CREATE OR REPLACE FUNCTION gemini.check_script_validity(
    scr_name TEXT,
    dat_name TEXT,
    exp_name TEXT,
    sea_name TEXT,
    sit_name TEXT
) RETURNS BOOLEAN AS $$
BEGIN

    -- Check if dataset with dat_name exists, if not, create it
    IF NOT EXISTS (
        SELECT 1
        FROM gemini.datasets
        WHERE dataset_name = dat_name
    ) THEN
        PERFORM gemini.create_dataset_if_not_exists(dat_name, 4, CURRENT_DATE, exp_name);
    END IF;

    -- Check if the script is already associated with the dataset
    IF NOT EXISTS (
        SELECT 1
        FROM gemini.script_datasets_view sdv
        WHERE sdv.script_name = scr_name
          AND sdv.dataset_name = dat_name
    ) THEN
        INSERT INTO gemini.script_datasets (script_id, dataset_id)
        VALUES (
            (SELECT id FROM gemini.scripts WHERE script_name = scr_name),
            (SELECT id FROM gemini.datasets WHERE dataset_name = dat_name)
        );
    END IF;

    -- Check if the combination of valid_script_dataset_combinations_view exists
    IF EXISTS (
        SELECT 1
        FROM gemini.valid_script_dataset_combinations_view vsdc
        WHERE vsdc.script_name = scr_name
          AND vsdc.dataset_name = dat_name
          AND vsdc.experiment_name = exp_name
          AND vsdc.season_name = sea_name
          AND vsdc.site_name = sit_name
    ) THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to populate ID fields in script_records table based on names
CREATE OR REPLACE FUNCTION gemini.populate_script_record_ids()
RETURNS TRIGGER AS $$
DECLARE
    scr_id UUID;
    dat_id UUID;
    exp_id UUID;
    sea_id UUID;
    sit_id UUID;
BEGIN
    -- Check if the script, dataset, experiment, season, and site are valid
    IF NOT gemini.check_script_validity(NEW.script_name, NEW.dataset_name, NEW.experiment_name, NEW.season_name, NEW.site_name) THEN
        RAISE EXCEPTION 'Invalid script, dataset, experiment, season, or site combination';
    END IF;

    -- Get the IDs based on names
    SELECT id INTO scr_id FROM gemini.scripts WHERE script_name = NEW.script_name;
    SELECT id INTO dat_id FROM gemini.datasets WHERE dataset_name = NEW.dataset_name;
    SELECT id INTO exp_id FROM gemini.experiments WHERE experiment_name = NEW.experiment_name;
    SELECT id INTO sea_id FROM gemini.seasons WHERE season_name = NEW.season_name AND experiment_id = exp_id;
    SELECT id INTO sit_id FROM gemini.sites WHERE site_name = NEW.site_name;

    -- Update the record with the IDs
    NEW.script_id := scr_id;
    NEW.dataset_id := dat_id;
    NEW.experiment_id := exp_id;
    NEW.season_id := sea_id;
    NEW.site_id := sit_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_populate_script_record_ids
BEFORE INSERT OR UPDATE ON gemini.script_records
FOR EACH ROW
EXECUTE FUNCTION gemini.populate_script_record_ids();

-- Function to check validity of a model, dataset, experiment, season, and site combination using names
CREATE OR REPLACE FUNCTION gemini.check_model_validity(
    mod_name TEXT,
    dat_name TEXT,
    exp_name TEXT,
    sea_name TEXT,
    sit_name TEXT
) RETURNS BOOLEAN AS $$
BEGIN

    -- Check if dataset with dat_name exists, if not, create it 
    IF NOT EXISTS (
        SELECT 1
        FROM gemini.datasets
        WHERE dataset_name = dat_name
    ) THEN
        PERFORM gemini.create_dataset_if_not_exists(dat_name, 5, CURRENT_DATE, exp_name);
    END IF;

    -- Check if the model is already associated with the dataset
    IF NOT EXISTS (
        SELECT 1
        FROM gemini.model_datasets_view mdv
        WHERE mdv.model_name = mod_name
          AND mdv.dataset_name = dat_name
    ) THEN
        INSERT INTO gemini.model_datasets (model_id, dataset_id)
        VALUES (
            (SELECT id FROM gemini.models WHERE model_name = mod_name),
            (SELECT id FROM gemini.datasets WHERE dataset_name = dat_name)
        );
    END IF;


    -- Check if the combination of valid_model_dataset_combinations_view exists
    IF EXISTS (
        SELECT 1
        FROM gemini.valid_model_dataset_combinations_view vmddc
        WHERE vmddc.model_name = mod_name
          AND vmddc.dataset_name = dat_name
          AND vmddc.experiment_name = exp_name
          AND vmddc.season_name = sea_name
          AND vmddc.site_name = sit_name
    ) THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to populate ID fields in model_records table based on names
CREATE OR REPLACE FUNCTION gemini.populate_model_record_ids()
RETURNS TRIGGER AS $$
DECLARE
    mod_id UUID;
    dat_id UUID;
    exp_id UUID;
    sea_id UUID;
    sit_id UUID;
BEGIN
    
    -- Check if the model, dataset, experiment, season, and site are valid
    IF NOT gemini.check_model_validity(NEW.model_name, NEW.dataset_name, NEW.experiment_name, NEW.season_name, NEW.site_name) THEN
        RAISE EXCEPTION 'Invalid model, dataset, experiment, season, or site combination';
    END IF;

    -- Get the IDs based on names
    SELECT id INTO mod_id FROM gemini.models WHERE model_name = NEW.model_name;
    SELECT id INTO dat_id FROM gemini.datasets WHERE dataset_name = NEW.dataset_name;
    SELECT id INTO exp_id FROM gemini.experiments WHERE experiment_name = NEW.experiment_name;
    SELECT id INTO sea_id FROM gemini.seasons WHERE season_name = NEW.season_name AND experiment_id = exp_id;
    SELECT id INTO sit_id FROM gemini.sites WHERE site_name = NEW.site_name;

    -- Update the record with the IDs
    NEW.model_id := mod_id;
    NEW.dataset_id := dat_id;
    NEW.experiment_id := exp_id;
    NEW.season_id := sea_id;
    NEW.site_id := sit_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_populate_model_record_ids
BEFORE INSERT OR UPDATE ON gemini.model_records
FOR EACH ROW
EXECUTE FUNCTION gemini.populate_model_record_ids();

-- Function to check the validity of plot, experiment, season and site
CREATE OR REPLACE FUNCTION gemini.check_plot_validity(
    exp_name TEXT,
    sea_name TEXT,
    sit_name TEXT,
    plt_num INTEGER,
    plt_row_num INTEGER,
    plt_col_num INTEGER
) RETURNS BOOLEAN AS $$
BEGIN
    -- Check if the combination of valid_plot_combinations_view exists
    IF EXISTS (
        SELECT 1
        FROM gemini.valid_plot_combinations_view vpc
        WHERE vpc.experiment_name = exp_name
          AND vpc.season_name = sea_name
          AND vpc.site_name = sit_name
    ) THEN
        PERFORM gemini.create_plot_if_not_exists(exp_name, sea_name, sit_name, plt_num, plt_row_num, plt_col_num);
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to check the validity of a sensor, dataset, experiment, season, and site combination using names
CREATE OR REPLACE FUNCTION gemini.check_sensor_validity(
    sen_name TEXT,
    dat_name TEXT,
    exp_name TEXT,
    sea_name TEXT,
    sit_name TEXT
) RETURNS BOOLEAN AS $$
BEGIN

    -- Check if dataset with dat_name exists, if not, create it
    IF NOT EXISTS (
        SELECT 1
        FROM gemini.datasets
        WHERE dataset_name = dat_name
    ) THEN
        PERFORM gemini.create_dataset_if_not_exists(dat_name, 1, CURRENT_DATE, exp_name);
    END IF;

    -- Check if the sensor is already associated with the dataset
    IF NOT EXISTS (
        SELECT 1
        FROM gemini.sensor_datasets_view sds
        WHERE sds.sensor_name = sen_name
          AND sds.dataset_name = dat_name
    ) THEN
        INSERT INTO gemini.sensor_datasets (sensor_id, dataset_id)
        VALUES (
            (SELECT id FROM gemini.sensors WHERE sensor_name = sen_name),
            (SELECT id FROM gemini.datasets WHERE dataset_name = dat_name)
        );
    END IF;

    -- Check if the combination of valid_sensor_dataset_combinations_view exists
    IF EXISTS (
        SELECT 1
        FROM gemini.valid_sensor_dataset_combinations_view vsdc
        WHERE vsdc.sensor_name = sen_name
          AND vsdc.dataset_name = dat_name
          AND vsdc.experiment_name = exp_name
          AND vsdc.season_name = sea_name
          AND vsdc.site_name = sit_name
    ) THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to populate ID fields in sensor_records table based on names and plot data
CREATE OR REPLACE FUNCTION gemini.populate_sensor_record_ids()
RETURNS TRIGGER AS $$
DECLARE
    sen_id UUID;
    dat_id UUID;
    exp_id UUID;
    sea_id UUID;
    sit_id UUID;
    pl_id UUID;
BEGIN
    -- Check if the sensor, dataset, experiment, season, and site are valid
    IF NOT gemini.check_sensor_validity(NEW.sensor_name, NEW.dataset_name, NEW.experiment_name, NEW.season_name, NEW.site_name) THEN
        RAISE EXCEPTION 'Invalid sensor, dataset, experiment, season, or site combination';
    END IF;

    -- Check if the combination of experiment, season, and site is valid for plots
    IF NOT gemini.check_plot_validity(NEW.experiment_name, NEW.season_name, NEW.site_name, NEW.plot_number, NEW.plot_row_number, NEW.plot_column_number) THEN
        RAISE EXCEPTION 'Invalid experiment, season, or site combination for plots';
    END IF;

    -- Get the IDs based on names
    SELECT id INTO sen_id FROM gemini.sensors WHERE sensor_name = NEW.sensor_name;
    SELECT id INTO dat_id FROM gemini.datasets WHERE dataset_name = NEW.dataset_name;
    SELECT id INTO exp_id FROM gemini.experiments WHERE experiment_name = NEW.experiment_name;
    SELECT id INTO sea_id FROM gemini.seasons WHERE season_name = NEW.season_name AND experiment_id = exp_id;
    SELECT id INTO sit_id FROM gemini.sites WHERE site_name = NEW.site_name;

    -- Get the plot ID based on the experiment, season, and site, plot_number, plot_row_number and plot_column_number
    SELECT id INTO pl_id FROM gemini.plots 
    WHERE experiment_id = exp_id 
      AND season_id = sea_id 
      AND site_id = sit_id 
      AND plot_number = NEW.plot_number
      AND plot_row_number = NEW.plot_row_number
      AND plot_column_number = NEW.plot_column_number;
    IF pl_id IS NULL THEN
        RAISE EXCEPTION 'No matching plot found for the given parameters';
    END IF;

    -- Update the record with the IDs
    NEW.sensor_id := sen_id;
    NEW.dataset_id := dat_id;
    NEW.experiment_id := exp_id;
    NEW.season_id := sea_id;
    NEW.site_id := sit_id;
    NEW.plot_id := pl_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_populate_sensor_record_ids
BEFORE INSERT OR UPDATE ON gemini.sensor_records
FOR EACH ROW
EXECUTE FUNCTION gemini.populate_sensor_record_ids();

-- Function to check the validity of a trait, dataset, experiment, season, and site combination using names
CREATE OR REPLACE FUNCTION gemini.check_trait_validity(
    trai_name TEXT,
    dat_name TEXT,
    exp_name TEXT,
    sea_name TEXT,
    sit_name TEXT
) RETURNS BOOLEAN AS $$
BEGIN

    -- Check if dataset with dat_name exists, if not, create it
    IF NOT EXISTS (
        SELECT 1
        FROM gemini.datasets
        WHERE dataset_name = dat_name
    ) THEN
        PERFORM gemini.create_dataset_if_not_exists(dat_name, 2, CURRENT_DATE, exp_name);
    END IF;

    -- Check if the trait is already associated with the dataset
    IF NOT EXISTS (
        SELECT 1
        FROM gemini.trait_datasets_view tds
        WHERE tds.trait_name = trai_name
          AND tds.dataset_name = dat_name
    ) THEN
        INSERT INTO gemini.trait_datasets (trait_id, dataset_id)
        VALUES (
            (SELECT id FROM gemini.traits WHERE trait_name = trai_name),
            (SELECT id FROM gemini.datasets WHERE dataset_name = dat_name)
        );
    END IF;

    -- Check if the combination of valid_trait_dataset_combinations_view exists
    IF EXISTS (
        SELECT 1
        FROM gemini.valid_trait_dataset_combinations_view vtdc
        WHERE vtdc.trait_name = trai_name
          AND vtdc.dataset_name = dat_name
          AND vtdc.experiment_name = exp_name
          AND vtdc.season_name = sea_name
          AND vtdc.site_name = sit_name
    ) THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to populate ID fields in trait_records table based on names
CREATE OR REPLACE FUNCTION gemini.populate_trait_record_ids()
RETURNS TRIGGER AS $$
DECLARE
    trai_id UUID;
    dat_id UUID;
    exp_id UUID;
    sea_id UUID;
    sit_id UUID;
    pl_id UUID;
BEGIN
    -- Check if the trait, dataset, experiment, season, and site are valid
    IF NOT gemini.check_trait_validity(NEW.trait_name, NEW.dataset_name, NEW.experiment_name, NEW.season_name, NEW.site_name) THEN
        RAISE EXCEPTION 'Invalid trait, dataset, experiment, season, or site combination';
    END IF;

    -- Check if the combination of experiment, season, and site is valid for plots
    IF NOT gemini.check_plot_validity(NEW.experiment_name, NEW.season_name, NEW.site_name, NEW.plot_number, NEW.plot_row_number, NEW.plot_column_number) THEN
        RAISE EXCEPTION 'Invalid experiment, season, or site combination for plots';
    END IF;

    -- Get the IDs based on names
    SELECT id INTO trai_id FROM gemini.traits WHERE trait_name = NEW.trait_name;
    SELECT id INTO dat_id FROM gemini.datasets WHERE dataset_name = NEW.dataset_name;
    SELECT id INTO exp_id FROM gemini.experiments WHERE experiment_name = NEW.experiment_name;
    SELECT id INTO sea_id FROM gemini.seasons WHERE season_name = NEW.season_name AND experiment_id = exp_id;
    SELECT id INTO sit_id FROM gemini.sites WHERE site_name = NEW.site_name;

    -- Get the plot ID based on the experiment, season, and site
    SELECT id INTO pl_id FROM gemini.plots 
    WHERE experiment_id = exp_id 
      AND season_id = sea_id 
      AND site_id = sit_id 
      AND plot_number = NEW.plot_number
      AND plot_row_number = NEW.plot_row_number
      AND plot_column_number = NEW.plot_column_number;
    IF pl_id IS NULL THEN
        RAISE EXCEPTION 'No matching plot found for the given parameters';
    END IF;

    -- Update the record with the IDs
    NEW.trait_id := trai_id;
    NEW.dataset_id := dat_id;
    NEW.experiment_id := exp_id;
    NEW.season_id := sea_id;
    NEW.site_id := sit_id;
    NEW.plot_id := pl_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_populate_trait_record_ids
BEFORE INSERT OR UPDATE ON gemini.trait_records
FOR EACH ROW
EXECUTE FUNCTION gemini.populate_trait_record_ids();
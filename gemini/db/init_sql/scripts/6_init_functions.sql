------------------------------------------------------------------------------
-- Database Functions and Procedures
------------------------------------------------------------------------------

-- Function to check the validity of a dataset, experiment, season, and site combination using names

CREATE OR REPLACE FUNCTION gemini.check_dataset_validity(
    dat_name TEXT,
    exp_name TEXT,
    sea_name TEXT,
    sit_name TEXT
) RETURNS BOOLEAN AS $$
BEGIN
    -- Check if the dataset exists
    IF NOT EXISTS (SELECT 1 FROM gemini.datasets WHERE gemini.datasets.dataset_name = dat_name) THEN
        RETURN FALSE;
    END IF;

    -- Check if the experiment exists
    IF NOT EXISTS (SELECT 1 FROM gemini.experiments WHERE gemini.experiments.experiment_name = exp_name) THEN
        RETURN FALSE;
    END IF;

    -- Check if the season exists and belongs to the experiment
    IF NOT EXISTS (
        SELECT 1
        FROM gemini.seasons s
        JOIN gemini.experiments e ON s.experiment_id = e.id
        WHERE s.season_name = sea_name AND e.experiment_name = exp_name
    ) THEN
        RETURN FALSE;
    END IF;

    -- Check if the site is associated with the experiment based on experiment_sites
    IF NOT EXISTS (
        SELECT 1 FROM gemini.experiment_sites es
        WHERE es.experiment_id = (SELECT id FROM gemini.experiments WHERE experiment_name = exp_name)
        AND es.site_id = (SELECT id FROM gemini.sites WHERE site_name = sit_name)
    )
    THEN
        RETURN FALSE;
    END IF;

    -- If all checks pass, the combination is valid
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;


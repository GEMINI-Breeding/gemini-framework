------------------------------------------------------------------------------
-- Database Functions and Procedures
------------------------------------------------------------------------------

------------------------------------------------------------------------------
-- Function: get_plots
--
-- Description:
-- Returns a list of plots for a given experiment, season and site

CREATE OR REPLACE FUNCTION gemini.get_plots(
    experiment_name TEXT,
    season_name TEXT,
    site_name TEXT
) RETURNS SETOF gemini.plot_view AS
$$
BEGIN
    RETURN QUERY
    SELECT * FROM gemini.plot_view
    WHERE
        experiment_name = experiment_name AND
        season_name = season_name AND
        site_name = site_name;
END;
$$ LANGUAGE plpgsql;


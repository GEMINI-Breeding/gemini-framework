from gemini.db.models.sites import SiteModel

# Get Default Site
default_site = SiteModel.get_by_parameters(site_name='Default')

# Print Site Plots
print("Plots:")
plots = default_site.plots
for plot in plots:
    print(plot.plot_number)

# Print Site Experiments
print("Experiments:")
experiments = default_site.experiments
for experiment in experiments:
    print(experiment.experiment_name)
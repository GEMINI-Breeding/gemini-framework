from gemini.api.site import Site

# Create a new Site for Experiment A
new_site = Site.create(
    site_name="Site Test 1",
    site_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Site: {new_site}")

# Get associated experiments
associated_experiments = new_site.get_associated_experiments()
for experiment in associated_experiments:
    print(f"Associated Experiment: {experiment}")

# Associate the new site with Experiment B
new_site.associate_experiment(experiment_name="Experiment B")
print(f"Associated Site with Experiment B")

# Check if the new site is associated with Experiment B
is_associated = new_site.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Site associated with Experiment B? {is_associated}")

# Unassociate the new site from Experiment B
new_site.unassociate_experiment(experiment_name="Experiment B")
print(f"Unassociated Site from Experiment B")

# Verify the unassociation
is_associated_after_unassociation = new_site.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Site still associated with Experiment B? {is_associated_after_unassociation}")
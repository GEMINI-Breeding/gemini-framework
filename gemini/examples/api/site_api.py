from gemini.api.site import Site

# Create a new site with experiment Experiment A
new_site = Site.create(
    site_name="Site Test 1",
    site_city="City A",
    site_state="State A",
    site_country="Country A",
    site_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created Site: {new_site}")

# Assign the site to Experiment B
new_site.assign_experiment("Experiment B")
print(f"Assigned Site to Experiment B: {new_site}")

# Get all Experiments for the site
experiments = new_site.get_experiments()
print(f"All Experiments:")
for experiment in experiments:
    print(experiment)

# Check if the site belongs to Experiment B
belongs = new_site.belongs_to_experiment("Experiment B")
print(f"Site belongs to Experiment B: {belongs}")

# Remove the site from Experiment B
new_site.unassign_experiment("Experiment B")
print(f"Removed Site from Experiment B: {new_site}")

# Check if it belongs to Experiment B
belongs = new_site.belongs_to_experiment("Experiment B")
print(f"Site belongs to Experiment B: {belongs}")

# Get Site with site_name and experiment_name that do exist
site = Site.get("Site Test 1", "Experiment A")
print(f"Got Site: {site}")

# Get Site by ID
site = Site.get_by_id(new_site.id)
print(f"Got Site by ID: {site}")

# Get all sites
all_sites = Site.get_all()
print(f"All Sites:")
for site in all_sites:
    print(site)

# Search for sites
searched_sites = Site.search(experiment_name="Experiment A")
length_searched_sites = len(searched_sites)
print(f"Found {length_searched_sites} sites in Experiment A")

# Refresh the site
site.refresh()
print(f"Refreshed Site: {site}")

# Update the site
site.update(
    site_info={"test": "test_updated"},
    site_city="City B",
    site_state="State B",
    site_country="Country B",
)
print(f"Updated Site: {site}")

# Set Site Info
site.set_info(
    site_info={"test": "test_set"},
)
print(f"Set Site Info: {site}")

# Get Site Info
site_info = site.get_info()
print(f"Site Info: {site_info}")

# Delete the site
is_deleted = new_site.delete()
print(f"Deleted Site: {is_deleted}")




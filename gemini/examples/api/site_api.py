from gemini.api.site import Site

# Create a new site
new_site = Site.create(
    site_name="Site Test X",
    site_city="City A",
    site_state="State A",
    site_country="Country A",
    site_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created Site: {new_site}")

# Get Site with site_name that does exist
site = Site.get("Site Test X")
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
site = site.refresh()
print(f"Refreshed Site: {site}")

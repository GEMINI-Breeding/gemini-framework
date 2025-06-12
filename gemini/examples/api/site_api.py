from gemini.api.site import Site

# Create a new Site for Experiment A
new_site = Site.create(
    site_name="Site X",
    site_city="City X",
    site_state="State X",
    site_country="Country X",
    site_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Site: {new_site}")

# Get Site by ID
site_by_id = Site.get_by_id(new_site.id)
print(f"Site by ID: {site_by_id}")

# Get Site by Name
site_by_name = Site.get(site_name="Site X")
print(f"Site by Name: {site_by_name}")

# Get all sites
all_sites = Site.get_all()
for site in all_sites:
    print(f"Site: {site}")

# Search for sites by name
search_results = Site.search(site_name="Site X")
for result in search_results:
    print(f"Search Result: {result}")

# Update Site
site_by_name.update(
    site_city="Updated City",
    site_state="Updated State",
    site_country="Updated Country",
    site_info={"updated": "info"}
)
print(f"Updated Site: {site_by_name}")

# Refresh Site
site_by_name.refresh()
print(f"Refreshed Site: {site_by_name}")

# Set Site Info
site_by_name.set_info(
    site_info={"new": "info"}
)
print(f"Set Site Info: {site_by_name.get_info()}")

# Check if Site Exists before deletion
exists = Site.exists(site_name="Site X")
print(f"Site exists: {exists}")

# Delete Site
is_deleted = site_by_name.delete()
print(f"Deleted Site: {is_deleted}")

# Check if Site Exists after deletion
exists_after_deletion = Site.exists(site_name="Site X")
print(f"Site exists after deletion: {exists_after_deletion}")
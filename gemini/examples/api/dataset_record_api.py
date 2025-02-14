from gemini.api.dataset_record import DatasetRecord

# Create a new dataset record
new_dataset_record = DatasetRecord.create(
    experiment_name="Experiment A",
    site_name="Site A",
    season_name="Season A",
    dataset_name="Dataset A"
)
print(f"Created Dataset Record: {new_dataset_record}")

from gemini.db.models.datasets import DatasetModel

# Get Datasets
datasets = DatasetModel.all()

# Print Datasets
print("Datasets:")
for dataset in datasets:
    print(f"{dataset.id}: {dataset.dataset_name} {dataset.dataset_type.dataset_type_name}")
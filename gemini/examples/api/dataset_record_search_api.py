from gemini.api.dataset import Dataset

# Get Dataset A
dataset = Dataset.get("Dataset A")
print(f"Got Dataset: {dataset}")

# Get all dataset A records
dataset_records = dataset.get_records()
for record in dataset_records:
    print(f"Dataset Record: {record}")
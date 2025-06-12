from gemini.api.sensor import Sensor

# Create a new Sensor for Experiment A
new_sensor = Sensor.create(
    sensor_name="Sensor X",
    sensor_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Sensor: {new_sensor}")

# Get Associated Experiments
associated_experiments = new_sensor.get_associated_experiments()
for experiment in associated_experiments:
    print(f"Associated Experiment: {experiment}")

# Associate the new sensor with Experiment B
new_sensor.associate_experiment(experiment_name="Experiment B")
print(f"Associated Sensor with Experiment B")

# Check if the new sensor is associated with Experiment B
is_associated = new_sensor.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Sensor associated with Experiment B? {is_associated}")

# Unassociate the new sensor from Experiment B
new_sensor.unassociate_experiment(experiment_name="Experiment B")
print(f"Unassociated Sensor from Experiment B")

# Verify the unassociation
is_associated_after_unassociation = new_sensor.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Sensor still associated with Experiment B? {is_associated_after_unassociation}")
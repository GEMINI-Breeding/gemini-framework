from gemini.api.sensor_platform import SensorPlatform

# Create a new Sensor Platform for Experiment A
new_sensor_platform = SensorPlatform.create(
    sensor_platform_name="Platform Test 1",
    sensor_platform_info={"test": "test"},
    experiment_name="Experiment A"
)
print(f"Created New Sensor Platform: {new_sensor_platform}")

# Get Associated Experiments
associated_experiments = new_sensor_platform.get_associated_experiments()
for experiment in associated_experiments:
    print(f"Associated Experiment: {experiment}")

# Associate the new sensor platform with Experiment B
new_sensor_platform.associate_experiment(experiment_name="Experiment B")
print(f"Associated Sensor Platform with Experiment B")

# Check if the new sensor platform is associated with Experiment B
is_associated = new_sensor_platform.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Sensor Platform associated with Experiment B? {is_associated}")

# Unassociate the new sensor platform from Experiment B
new_sensor_platform.unassociate_experiment(experiment_name="Experiment B")
print(f"Unassociated Sensor Platform from Experiment B")

# Verify the unassociation
is_associated_after_unassociation = new_sensor_platform.belongs_to_experiment(experiment_name="Experiment B")
print(f"Is Sensor Platform still associated with Experiment B? {is_associated_after_unassociation}")
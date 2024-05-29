from gemini.api import Experiment

test_experiment = Experiment.create(experiment_name="Test Experiment")

test_experiment.add_info(
    {
        "location": "Kathmandu, Nepal",
        "latitude": 27.7172,
        "longitude": 85.324,
        "altitude": 1400
    }
)

print(test_experiment)
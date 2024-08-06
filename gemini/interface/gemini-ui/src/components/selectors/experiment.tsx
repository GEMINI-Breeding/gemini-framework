import { useGEMINIStore } from "@/store";
import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";
import { Select } from "@mantine/core";
import Experiments from "@/api/experiments";

export default function ExperimentSelector() {
  // Get State and actions from the global store
  const setExperiments = useGEMINIStore((state) => state.setExperiments);
  const currentExperiment = useGEMINIStore((state) => state.currentExperiment);
  const setCurrentExperiment = useGEMINIStore(
    (state) => state.setCurrentExperiment
  );

  // Fetch Experiments
  const { data, isError, isLoading, isSuccess } = useQuery({
    queryKey: ["experiments"],
    queryFn: async () => {
      return await Experiments.getExperiments();
    },
    retry: true,
    retryDelay: 100,
  });

  // Set the data in the global store using the action
  useEffect(() => {
    if (isSuccess) {
      setExperiments(data.map((experiment) => experiment.id));
      setCurrentExperiment(data[0]);
    }
  }, [data, isSuccess, setExperiments, setCurrentExperiment]);

  // Experiment Selection Handler
  function onExperimentSelect(experiment_name: string | null) {
    // Get Experiment from API data
    const selected_experiment = data?.find(
      (experiment) => experiment.experiment_name === experiment_name
    );
    // Set the experiment in the global store
    setCurrentExperiment(selected_experiment!);
  }

  // Placeholder Text
  let placeholder = "Select Experiment";
  if (isLoading) {
    placeholder = "Loading...";
  } else if (isError) {
    placeholder = "Error Fetching Experiments";
  } else if (data?.length === 0) {
    placeholder = "No Experiments Found";
  }

  return (
    <div>
      <Select
        placeholder={placeholder}
        label="Select Experiment"
        data={data?.map((experiment) => experiment.experiment_name)}
        value={currentExperiment?.experiment_name}
        onChange={onExperimentSelect}
      ></Select>
    </div>
  );
}

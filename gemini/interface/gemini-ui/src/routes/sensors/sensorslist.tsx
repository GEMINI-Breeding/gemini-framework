import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { Title, Divider, Space, Stack } from "@mantine/core";

import { useGEMINIStore } from "@/store";
import Experiments from "@/api/experiments";
import SensorCard from "@/components/datacards/sensorcard";
import CenterMessage from "@/components/centermessage/centermessage";
import ExperimentSelector from "@/components/selectors/experiment";

export default function SensorsList() {
  // Get the current experiment from the global store
  const experiment = useGEMINIStore((state) => state.currentExperiment);

  // Fetch the sensors for the current experiment
  const { data, isLoading, refetch } = useQuery({
    queryKey: ["sensors", experiment],
    queryFn: async () => {
      return await Experiments.getExperimentSensors(experiment.experiment_name);
    },
    enabled: !!experiment, // This ensures the query only runs when `experiment` is truthy
  });

  // Refetch the sensors when the experiment changes
  useEffect(() => {
    if (experiment) {
      refetch();
    }
  }, [experiment, refetch]);

  // Show a loading message while fetching the sensors
  if (isLoading) {
    return <CenterMessage message="Loading Sensors..." />;
  }

  // If no experiment is selected, show a message
  if (!experiment || !experiment.experiment_name) {
    return <CenterMessage message="Please Select an Experiment" />;
  }

  // Otherwise, show the sensors
  return (
    <div>
      <ul>
        <Title order={1}>Sensors</Title>
        <Divider />
        <Space h="md" />
        <Stack gap="md">
          {data?.length ?? 0 > 0 ? (
            data?.map((sensor) => (
              <SensorCard key={sensor.id} sensor={sensor} />
            ))
          ) : (
            <CenterMessage
              message={
                "No Sensors Found for experiment " + experiment.experiment_name
              }
            />
          )}
        </Stack>
      </ul>
    </div>
  );
}

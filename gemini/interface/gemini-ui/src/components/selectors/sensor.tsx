import { useGEMINIStore } from "@/store";
import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";
import { Select } from "@mantine/core";
import Experiment from "@/api/experiments";

export default function SensorSelector() {
  // Get State and actions from the global store
  const setSensors = useGEMINIStore((state) => state.setSensors);
  const currentSensor = useGEMINIStore((state) => state.currentSensor);
  const setCurrentSensor = useGEMINIStore((state) => state.setCurrentSensor);
  const currentExperiment = useGEMINIStore((state) => state.currentExperiment);

  // Fetch Sensors for the current experiment
  const { data, isError, isLoading, isSuccess } = useQuery({
    queryKey: ["sensors", currentExperiment],
    queryFn: async () => {
      return await Experiment.getExperimentSensors(
        currentExperiment.experiment_name
      );
    },
    enabled: !!currentExperiment,
  });

  // Set the data in the global store using the action
  useEffect(() => {
    if (isSuccess) {
      setSensors(data.map((sensor) => sensor.id));
      setCurrentSensor(data[0]);
    }
  }, [data, isSuccess, setSensors, setCurrentSensor]);

  // Sensor Selection Handler
  function onSensorSelect(sensor_name: string | null) {
    // Get Sensor from API data
    const selected_sensor = data?.find(
      (sensor) => sensor.sensor_name === sensor_name
    );
    // Set the sensor in the global store
    setCurrentSensor(selected_sensor!);
  }

  // Placeholder Text
  let placeholder = "Select Sensor";
  if (isLoading) {
    placeholder = "Loading...";
  } else if (isError) {
    placeholder = "Error Fetching Sensors";
  } else if (data?.length === 0) {
    placeholder = "No Sensors Found";
  }

  return (
    <div>
      <Select
        placeholder={placeholder}
        label="Select Sensor"
        data={data?.map((sensor) => sensor.sensor_name)}
        value={currentSensor?.sensor_name}
        onChange={onSensorSelect}
      ></Select>
    </div>
  );
}

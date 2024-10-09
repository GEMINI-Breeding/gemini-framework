import { TextInput, Stack, Group, Button, Select } from "@mantine/core";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import Experiments from "@/api/experiments";
import Sensors from "@/api/sensors";
import {
  GEMINISensorTypes,
  GEMINIDataFormats,
  GEMINIDataTypes,
} from "@/api/enums";

// Create string options for Sensor Type
const sensorTypeOptions = Object.keys(GEMINISensorTypes).filter((key) =>
  isNaN(Number(key))
);

// Create string options for Data Format
const dataFormatOptions = Object.keys(GEMINIDataFormats).filter((key) =>
  isNaN(Number(key))
);

// Create string options for Data Type
const dataTypeOptions = Object.keys(GEMINIDataTypes).filter((key) =>
  isNaN(Number(key))
);

export default function SensorCreateForm() {
  // Local state storing sensor to be created
  const [experimentName, setExperimentName] = useState<string>("");
  const [sensorName, setSensorName] = useState<string>("");
  const [sensorType, setSensorType] = useState<number>(0);
  const [dataFormat, setDataFormat] = useState<number>(0);
  const [dataType, setDataType] = useState<number>(0);

  // Get Experiments to choose from, from the API
  const { data: experiments } = useQuery({
    queryKey: ["experiments"],
    queryFn: Experiments.getExperiments,
  });

  // Create a mutation to create a new sensor
  const createSensor = useMutation({
    mutationKey: ["create_sensor", experimentName],
    mutationFn: async (newSensor: object) => {
      return await Sensors.createSensor(newSensor);
    },
  });

  // Handle form submission
  function onCreateButtonClick() {
    createSensor.mutate({
      experiment_name: experimentName,
      sensor_name: sensorName,
      sensor_type_id: sensorType,
      sensor_data_format_id: dataFormat,
      sensor_data_type_id: dataType,
    });
  }

  return (
    <div>
      <Stack>
        <Select
          label="Experiment"
          placeholder="Select Experiment"
          data={experiments?.map((experiment) => experiment.experiment_name)}
          onChange={(value) => setExperimentName(value as string)}
        />
        <TextInput
          label="Sensor Name"
          placeholder="Enter Sensor Name"
          value={sensorName}
          onChange={(event) => setSensorName(event.target.value)}
        />
        <Select
          label="Sensor Type"
          placeholder="Select Sensor Type"
          data={sensorTypeOptions}
          value={GEMINISensorTypes[sensorType]}
          onChange={(value) => {
            const numericValue =
              GEMINISensorTypes[value as keyof typeof GEMINISensorTypes];
            setSensorType(numericValue);
          }}
        />
        <Select
          label="Data Type"
          placeholder="Select Data Type"
          data={dataTypeOptions}
          value={GEMINIDataTypes[dataType]}
          onChange={(value) => {
            const numericValue =
              GEMINIDataTypes[value as keyof typeof GEMINIDataTypes];
            setDataType(numericValue);
          }}
        />
        <Select
          label="Data Format"
          placeholder="Select Data Format"
          data={dataFormatOptions}
          value={GEMINIDataFormats[dataFormat]}
          onChange={(value) => {
            const numericValue =
              GEMINIDataFormats[value as keyof typeof GEMINIDataFormats];
            setDataFormat(numericValue);
          }}
        />
      </Stack>
      <Group justify="flex-end">
        <Button onClick={onCreateButtonClick}>Create Sensor</Button>
      </Group>
    </div>
  );
}

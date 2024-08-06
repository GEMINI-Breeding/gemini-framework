import { TextInput, Stack, Group, Button } from "@mantine/core";
import { DatePickerInput, DateValue } from "@mantine/dates";
import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import Experiments from "@/api/experiments";

export default function ExperimentCreateForm() {
  // Local state storing experiment to be created
  const [experimentName, setExperimentName] = useState<string>("");
  const [experimentStartDate, setExperimentStartDate] = useState<Date | null>(
    null
  );
  const [experimentEndDate, setExperimentEndDate] = useState<Date | null>(null);

  // Mutation to Create a new Experiment
  const createExperiment = useMutation({
    mutationKey: ["create_experiment"],
    mutationFn: async (newExperiment: object) => {
      return await Experiments.createExperiment(newExperiment);
    },
  });

  // Input Handlers
  function handleExperimentNameChange(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    setExperimentName(event.target.value);
  }

  function handleExperimentStartDateChange(date: DateValue) {
    setExperimentStartDate(date);
  }

  function handleExperimentEndDateChange(date: DateValue) {
    setExperimentEndDate(date);
  }

  function onCreateButtonClick() {
    createExperiment.mutate({
      experiment_name: experimentName,
      experiment_start_date: experimentStartDate?.toISOString(),
      experiment_end_date: experimentEndDate?.toISOString(),
    });
  }

  return (
    <div>
      <Stack>
        <TextInput
          label="Experiment Name"
          placeholder="Enter Experiment Name"
          value={experimentName}
          onChange={handleExperimentNameChange}
        />
        <DatePickerInput
          label="Start Date"
          placeholder="Select Start Date"
          value={experimentStartDate}
          onChange={handleExperimentStartDateChange}
        />
        <DatePickerInput
          label="End Date"
          placeholder="Select End Date"
          value={experimentEndDate}
          onChange={handleExperimentEndDateChange}
        />
        <Group justify="flex-end">
          <Button onClick={onCreateButtonClick}>Create Experiment</Button>
        </Group>
      </Stack>
    </div>
  );
}

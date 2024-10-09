import { TextInput, Stack, Group, Button, Select } from "@mantine/core";
import { DatePickerInput, DateValue } from "@mantine/dates";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import Experiments from "@/api/experiments";
import Seasons from "@/api/seasons";

export default function SeasonCreateForm() {
  // Local State for storing season to be created
  const [experimentName, setExperimentName] = useState<string>("");
  const [seasonName, setSeasonName] = useState<string>("");
  const [seasonStartDate, setSeasonStartDate] = useState<Date | null>(null);
  const [seasonEndDate, setSeasonEndDate] = useState<Date | null>(null);

  // Get Experiments to choose from, from the API
  const { data: experiments } = useQuery({
    queryKey: ["experiments"],
    queryFn: Experiments.getExperiments,
  });

  // Create a mutation to create a new season
  const createSeason = useMutation({
    mutationKey: ["create_season", experimentName],
    mutationFn: async (newSeason: object) => {
      return await Seasons.createSeason(newSeason);
    },
  });

  // Handle form submission
  function onCreateButtonClick() {
    createSeason.mutate({
      experiment_name: experimentName,
      season_name: seasonName,
      season_start_date: seasonStartDate?.toISOString(),
      season_end_date: seasonEndDate?.toISOString(),
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
          label="Season Name"
          placeholder="Enter Season Name"
          value={seasonName}
          onChange={(event) => setSeasonName(event.target.value)}
        />
        <DatePickerInput
          label="Start Date"
          placeholder="Select Start Date"
          value={seasonStartDate}
          onChange={(date: DateValue) => setSeasonStartDate(date)}
        />
        <DatePickerInput
          label="End Date"
          placeholder="Select End Date"
          value={seasonEndDate}
          onChange={(date: DateValue) => setSeasonEndDate(date)}
        />
        <Group>
          <Button onClick={onCreateButtonClick}>Create Season</Button>
        </Group>
      </Stack>
    </div>
  );
}

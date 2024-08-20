import { TextInput, Stack, Group, Button, Select } from "@mantine/core";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import Experiments from "@/api/experiments";
import Sites from "@/api/sites";

export default function SiteCreateForm() {
  // Local state storing site to be created
  const [experimentName, setExperimentName] = useState<string>("");
  const [siteName, setSiteName] = useState<string>("");
  const [siteCity, setSiteCity] = useState<string>("");
  const [siteState, setSiteState] = useState<string>("");
  const [siteCountry, setSiteCountry] = useState<string>("");

  // Get Experiments to choose from, from the API
  const { data: experiments } = useQuery({
    queryKey: ["experiments"],
    queryFn: Experiments.getExperiments,
  });

  // Create a mutation to create a new site
  const createSite = useMutation({
    mutationKey: ["create_site", experimentName],
    mutationFn: async (newSite: object) => {
      return await Sites.createSite(newSite);
    },
  });

  // Handle form submission
  function onCreateButtonClick() {
    createSite.mutate({
      experiment_name: experimentName,
      site_name: siteName,
      site_city: siteCity,
      site_state: siteState,
      site_country: siteCountry,
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
          label="Site Name"
          placeholder="Enter Site Name"
          value={siteName}
          onChange={(event) => setSiteName(event.target.value)}
        />
        <TextInput
          label="Site City"
          placeholder="Enter Site City"
          value={siteCity}
          onChange={(event) => setSiteCity(event.target.value)}
        />
        <TextInput
          label="Site State"
          placeholder="Enter Site State"
          value={siteState}
          onChange={(event) => setSiteState(event.target.value)}
        />
        <TextInput
          label="Site Country"
          placeholder="Enter Site Country"
          value={siteCountry}
          onChange={(event) => setSiteCountry(event.target.value)}
        />
        <Group justify="flex-end">
          <Button onClick={onCreateButtonClick}>Create Site</Button>
        </Group>
      </Stack>
    </div>
  );
}

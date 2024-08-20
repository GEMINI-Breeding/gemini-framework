import { TextInput, Stack, Group, Button, Select } from "@mantine/core";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import Experiments from "@/api/experiments";
import Traits from "@/api/traits";
import { GEMINITraitLevels } from "@/api/enums";

// Create string options for Trait Level
const traitLevelOptions = Object.keys(GEMINITraitLevels);

export default function TraitCreateForm() {
  // Local state storing trait to be created
  const [experimentName, setExperimentName] = useState<string>("");
  const [traitName, setTraitName] = useState<string>("");
  const [traitLevel, setTraitLevel] = useState<number>(0);
  const [traitUnits, setTraitUnits] = useState<string>("");

  // Get Experiments to choose from, from the API
  const { data: experiments } = useQuery({
    queryKey: ["experiments"],
    queryFn: Experiments.getExperiments,
  });

  // Create a mutation to create a new trait
  const createTrait = useMutation({
    mutationKey: ["create_trait", experimentName],
    mutationFn: async (newTrait: object) => {
      return await Traits.createTrait(newTrait);
    },
  });

  // Handle form submission
  function onCreateButtonClick() {
    createTrait.mutate({
      experiment_name: experimentName,
      trait_name: traitName,
      trait_level: traitLevel,
      trait_units: traitUnits,
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
          label="Trait Name"
          placeholder="Enter Trait Name"
          value={traitName}
          onChange={(event) => setTraitName(event.target.value)}
        />
        <Select
          label="Trait Level"
          placeholder="Select Trait Level"
          data={traitLevelOptions}
          onChange={(value) => {
            const numericValue =
              GEMINITraitLevels[value as keyof typeof GEMINITraitLevels];
            setTraitLevel(numericValue);
          }}
        />
        <TextInput
          label="Trait Units"
          placeholder="Enter Trait Units"
          value={traitUnits}
          onChange={(event) => setTraitUnits(event.target.value)}
        />
        <Group justify="flex-end">
          <Button onClick={onCreateButtonClick}>Create Trait</Button>
        </Group>
      </Stack>
    </div>
  );
}

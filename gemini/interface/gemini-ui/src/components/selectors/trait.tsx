import { useGEMINIStore } from "@/store";
import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { Select } from "@mantine/core";
import Experiments from "@/api/experiments";

export default function TraitSelector() {
  // Get State and actions from the global store
  const setTraits = useGEMINIStore((state) => state.setTraits);
  const currentTrait = useGEMINIStore((state) => state.currentTrait);
  const setCurrentTrait = useGEMINIStore((state) => state.setCurrentTrait);
  const currentExperiment = useGEMINIStore((state) => state.currentExperiment);

  // Fetch Traits for the current experiment
  const { data, isError, isLoading, isSuccess } = useQuery({
    queryKey: ["traits", currentExperiment],
    queryFn: async () => {
      return await Experiments.getExperimentTraits(
        currentExperiment.experiment_name
      );
    },
    enabled: !!currentExperiment,
  });

  // Set the data in the global store using the action
  useEffect(() => {
    if (isSuccess) {
      setTraits(data.map((trait) => trait.id));
      setCurrentTrait(data[0]);
    }
  }, [data, isSuccess, setTraits, setCurrentTrait]);

  // Trait Selection Handler
  function onTraitSelect(trait_name: string | null) {
    // Get Trait from API data
    const selected_trait = data?.find(
      (trait) => trait.trait_name === trait_name
    );
    // Set the trait in the global store
    setCurrentTrait(selected_trait!);
  }

  // Placeholder Text
  let placeholder = "Select Trait";

  if (isLoading) {
    placeholder = "Loading...";
  } else if (isError) {
    placeholder = "Error Fetching Traits";
  } else if (data?.length === 0) {
    placeholder = "No Traits Found";
  }

  return (
    <div>
      <Select
        placeholder={placeholder}
        label="Select Trait"
        data={data?.map((trait) => trait.trait_name)}
        value={currentTrait?.trait_name}
        onChange={onTraitSelect}
      ></Select>
    </div>
  );
}

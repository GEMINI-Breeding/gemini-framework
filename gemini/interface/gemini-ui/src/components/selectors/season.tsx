import { useGEMINIStore } from "@/store";
import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";
import { Select } from "@mantine/core";
import Experiments from "@/api/experiments";

export default function SeasonSelector() {
  // Get State and actions from the global store
  const currentExperiment = useGEMINIStore((state) => state.currentExperiment);
  const setSeasons = useGEMINIStore((state) => state.setSeasons);
  const currentSeason = useGEMINIStore((state) => state.currentSeason);
  const setCurrentSeason = useGEMINIStore((state) => state.setCurrentSeason);

  // Fetch Seasons for the current experiment
  const { data, isError, isLoading, isSuccess } = useQuery({
    queryKey: ["seasons", currentExperiment],
    queryFn: async () => {
      return await Experiments.getExperimentSeasons(
        currentExperiment.experiment_name
      );
    },
    enabled: !!currentExperiment,
  });

  // Set the data in the global store using the action
  useEffect(() => {
    if (isSuccess) {
      setSeasons(data.map((season) => season.id));
      setCurrentSeason(data[0]);
    }
  }, [data, isSuccess, setSeasons, setCurrentSeason]);

  // Season Selection Handler
  function onSeasonSelect(season_name: string | null) {
    // Get Season from API data
    const selected_season = data?.find(
      (season) => season.season_name === season_name
    );
    // Set the season in the global store
    setCurrentSeason(selected_season!);
  }

  // Placeholder Text
  let placeholder = "Select Season";
  if (isLoading) {
    placeholder = "Loading...";
  } else if (isError) {
    placeholder = "Error Fetching Seasons";
  } else if (data?.length === 0) {
    placeholder = "No Seasons Found";
  }

  return (
    <div>
      <Select
        placeholder={placeholder}
        label="Select Season"
        data={data?.map((season) => season.season_name)}
        value={currentSeason?.season_name}
        onChange={onSeasonSelect}
      ></Select>
    </div>
  );
}

import { useGEMINIStore } from "@/store";
import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { Select } from "@mantine/core";
import Experiments from "@/api/experiments";

export default function SiteSelector() {
  // Get State and actions from the global store
  const setSites = useGEMINIStore((state) => state.setSites);
  const currentSite = useGEMINIStore((state) => state.currentSite);
  const setCurrentSite = useGEMINIStore((state) => state.setCurrentSite);
  const currentExperiment = useGEMINIStore((state) => state.currentExperiment);

  // Fetch Sites for the current experiment
  const { data, isError, isLoading, isSuccess } = useQuery({
    queryKey: ["sites", currentExperiment],
    queryFn: async () => {
      return await Experiments.getExperimentSites(
        currentExperiment.experiment_name
      );
    },
    enabled: !!currentExperiment,
  });

  // Set the data in the global store using the action
  useEffect(() => {
    if (isSuccess) {
      setSites(data.map((site) => site.id));
      setCurrentSite(data[0]);
    }
  }, [data, isSuccess, setSites, setCurrentSite]);

  // Site Selection Handler
  function onSiteSelect(site_name: string | null) {
    // Get Site from API data
    const selected_site = data?.find((site) => site.site_name === site_name);
    // Set the site in the global store
    setCurrentSite(selected_site!);
  }

  // Placeholder Text
  let placeholder = "Select Site";
  if (isLoading) {
    placeholder = "Loading...";
  } else if (isError) {
    placeholder = "Error Fetching Sites";
  } else if (data?.length === 0) {
    placeholder = "No Sites Found";
  }

  return (
    <div>
      <Select
        placeholder={placeholder}
        label="Select Site"
        data={data?.map((site) => site.site_name)}
        value={currentSite?.site_name}
        onChange={onSiteSelect}
      ></Select>
    </div>
  );
}

import { useGEMINIStore } from "@/store";
import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";
import { Select } from "@mantine/core";
import Platforms from "@/api/platforms";

export default function PlatformSelector() {
  // Get State and actions from the global store
  const setPlatforms = useGEMINIStore((state) => state.setPlatforms);
  const currentPlatform = useGEMINIStore((state) => state.currentPlatform);
  const setCurrentPlatform = useGEMINIStore(
    (state) => state.setCurrentPlatform
  );

  // Fetch Platforms
  const { data, isError, isLoading, isSuccess } = useQuery({
    queryKey: ["platforms"],
    queryFn: async () => {
      return await Platforms.getPlatforms();
    },
  });

  // Set the data in the global store using the action
  useEffect(() => {
    if (isSuccess) {
      setPlatforms(data.map((platform) => platform.id));
      setCurrentPlatform(data[0]);
    }
  }, [data, isSuccess, setPlatforms, setCurrentPlatform]);

  // Platform Selection Handler
  function onPlatformSelect(platform_name: string | null) {
    // Get Platform from API data
    const selected_platform = data?.find(
      (platform) => platform.sensor_platform_name === platform_name
    );
    // Set the platform in the global store
    setCurrentPlatform(selected_platform!);
  }

  // Placeholder Text
  let placeholder = "Select Platform";
  if (isLoading) {
    placeholder = "Loading...";
  } else if (isError) {
    placeholder = "Error Fetching Platforms";
  } else if (data?.length === 0) {
    placeholder = "No Platforms Found";
  }

  return (
    <div>
      <Select
        placeholder={placeholder}
        label="Select Platform"
        data={data?.map((platform) => platform.sensor_platform_name)}
        value={currentPlatform?.sensor_platform_name}
        onChange={onPlatformSelect}
      ></Select>
    </div>
  );
}

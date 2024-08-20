import {
  Group,
  Button,
  Box,
  Stack,
  ActionIcon,
  Select,
  Divider,
} from "@mantine/core";

import { useGEMINIUploadStore } from "@/store";
import ExperimentSelector from "@/components/selectors/experiment";
import SeasonSelector from "@/components/selectors/season";
import SensorSelector from "@/components/selectors/sensor";
import TraitSelector from "@/components/selectors/trait";
import SiteSelector from "@/components/selectors/site";
import { IconPlus } from "@tabler/icons-react";

// Modals
import {
  openFileSelectorModal,
  openExperimentCreateModal,
  openSeasonCreateModal,
} from "@/components/modals/modalhandler";

const UPLOAD_TYPES = ["Sensor", "Trait", "Plot", "Other"];

export default function UploadForm() {
  // Get the upload store state and actions
  const uploadType = useGEMINIUploadStore((state) => state.uploadType);
  const setUploadType = useGEMINIUploadStore((state) => state.setUploadType);

  return (
    <div>
      <Stack gap="md">
        <Group grow>
          <Box>
            <Select
              data={UPLOAD_TYPES}
              label="Select Upload Type"
              placeholder="Select Upload Type"
              value={uploadType}
              onChange={(value) => setUploadType(value as string)}
            ></Select>
          </Box>
        </Group>
        <Divider />
        {/* This is the experiment selector */}
        <Group preventGrowOverflow={false} justify="space-between" gap="sm">
          <Box w="90%">
            <ExperimentSelector />
          </Box>
          <Box pt={27.5}>
            <ActionIcon
              variant="filled"
              color="blue"
              onClick={() => {
                openExperimentCreateModal();
              }}
            >
              <IconPlus />
            </ActionIcon>
          </Box>
        </Group>
        {/* This is the season selector */}
        <Group preventGrowOverflow={false} justify="space-between" gap="sm">
          <Box w="90%">
            <SeasonSelector />
          </Box>
          <Box pt={27.5}>
            <ActionIcon
              variant="filled"
              color="blue"
              onClick={() => {
                openSeasonCreateModal();
              }}
            >
              <IconPlus />
            </ActionIcon>
          </Box>
        </Group>
        {/* This is the site selector */}
        <Group preventGrowOverflow={false} justify="space-between" gap="sm">
          <Box w="90%">
            <SiteSelector />
          </Box>
          <Box pt={27.5}>
            <ActionIcon
              variant="filled"
              color="blue"
              onClick={() => {
                console.log("Add Site");
              }}
            >
              <IconPlus />
            </ActionIcon>
          </Box>
        </Group>
        {/* This is the sensor selector */}
        <Group preventGrowOverflow={false} justify="space-between" gap="sm">
          <Box w="90%">
            <SensorSelector />
          </Box>
          <Box pt={27.5}>
            <ActionIcon
              variant="filled"
              color="blue"
              onClick={() => {
                console.log("Add Sensor");
              }}
            >
              <IconPlus />
            </ActionIcon>
          </Box>
        </Group>
        {/* This is the trait selector */}
        <Group
          preventGrowOverflow={false}
          justify="space-between"
          gap="sm"
          display={uploadType === "Trait" ? "flex" : "none"}
        >
          <Box w="90%">
            <TraitSelector />
          </Box>
          <Box pt={27.5}>
            <ActionIcon
              variant="filled"
              color="blue"
              onClick={() => {
                console.log("Add Trait");
              }}
            >
              <IconPlus />
            </ActionIcon>
          </Box>
        </Group>
        <Group justify="space-between">
          <Button
            color="blue"
            onClick={() => {
              openFileSelectorModal();
            }}
          >
            Select Files
          </Button>
          <Button color="blue">Upload Data</Button>
        </Group>
      </Stack>
    </div>
  );
}

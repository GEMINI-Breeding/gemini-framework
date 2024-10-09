import { Drawer, Title, Stack } from "@mantine/core";
import UploadTasksView from "./uploadtasksview";

interface TaskProgressDrawerProps {
  opened: boolean;
  onClose: () => void;
}

export default function TaskProgressDrawer({
  opened,
  onClose,
}: TaskProgressDrawerProps) {
  return (
    <div>
      <Drawer.Root
        opened={opened}
        onClose={onClose}
        position="right"
        offset={8}
        radius="sm"
        size="md"
        padding="md"
      >
        <Drawer.Overlay />
        <Drawer.Content>
          <Drawer.Header>
            <Drawer.Title>
              <Title order={4}>Task Progress</Title>
            </Drawer.Title>
            <Drawer.CloseButton />
          </Drawer.Header>
          <Drawer.Body>
            <Stack gap="md">
              <UploadTasksView />
            </Stack>
          </Drawer.Body>
        </Drawer.Content>
      </Drawer.Root>
    </div>
  );
}

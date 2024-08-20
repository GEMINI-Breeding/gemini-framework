import { useDisclosure } from "@mantine/hooks";
import { Drawer } from "@mantine/core";

interface TaskProgressDrawerProps {
  opened: boolean;
  onClose: () => void;
}

export default function TaskProgressDrawer({
  opened,
  onClose,
}: TaskProgressDrawerProps) {
  return (
    <Drawer
      opened={opened}
      onClose={onClose}
      position="right"
      offset={8}
      radius="sm"
      //   withCloseButton={false}
      size="md"
      padding="md"
      title="Task Progress"
    ></Drawer>
  );
}

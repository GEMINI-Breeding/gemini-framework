import { Badge, Paper, Group, Text } from "@mantine/core";
import { ActionIcon } from "@mantine/core";
import { IconX } from "@tabler/icons-react";

interface FileCardProps {
  file: File;
  onRemove: (file: File) => void;
}

export default function FileCard({ file, onRemove }: FileCardProps) {
  return (
    <Paper shadow="md" radius="md" p="md" withBorder>
      <Group justify="space-between">
        <Group>
          <Text size="xl" fw={700}>
            {file.name}
          </Text>
          <Badge color="blue" variant="filled">
            {file.type}
          </Badge>
        </Group>
        <Group>
          <ActionIcon
            variant="filled"
            color="red"
            onClick={() => onRemove(file)}
          >
            <IconX />
          </ActionIcon>
        </Group>
      </Group>
    </Paper>
  );
}

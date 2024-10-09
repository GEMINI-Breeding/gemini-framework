import { Progress, Paper, Stack, Text, Group, Badge } from "@mantine/core";
import { useState, useEffect } from "react";

interface UploadProgressProps {
  file: File;
  progress: number;
}

enum UploadStatus {
  Uploading = "Uploading",
  Complete = "Complete",
  Error = "Error",
}

export default function UploadProgress({
  file,
  progress,
}: UploadProgressProps) {
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>(
    UploadStatus.Uploading
  );

  useEffect(() => {
    if (progress === 100) {
      setUploadStatus(UploadStatus.Complete);
    }
  }, [progress]);

  return (
    <Paper shadow="xs" radius="md" p="sm" withBorder>
      <Stack gap="xs">
        <Group>
          <Text size="md" fw={500} span w="30%">
            File Upload
          </Text>
          <Text size="sm" c="dimmed" truncate="end" w="30%">
            {file.name}
          </Text>
        </Group>
        <Group justify="space-between">
          <Progress value={progress} color="blue" w="85%" />
          <Text size="sm">{progress}%</Text>
        </Group>
        <Group>
          <Badge color="blue" variant="filled">
            {uploadStatus}
          </Badge>
        </Group>
      </Stack>
    </Paper>
  );
}

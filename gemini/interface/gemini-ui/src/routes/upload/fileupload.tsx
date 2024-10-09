import { Title, Stack, Box } from "@mantine/core";
import { FileDropzone } from "@/components/dropzone/dropzone";

export default function FileUpload() {
  return (
    <div>
      <Stack gap="md">
        <Title order={1}>Upload Data</Title>
        <Box>
          <FileDropzone></FileDropzone>
        </Box>
      </Stack>
    </div>
  );
}

import { Stack, Box } from "@mantine/core";
import UploadProgress from "@/components/datacards/uploadprogress";
import useFileUpload from "@/hooks/useFileUpload";

export default function UploadTasksView() {
  const { uploads } = useFileUpload({
    uploadPrefix: "web-uploaded-files",
  });

  return (
    <Box>
      <Stack gap="md">
        {uploads.map((upload) => (
          <UploadProgress
            key={upload.file.name}
            file={upload.file}
            progress={upload.progress}
          />
        ))}
      </Stack>
    </Box>
  );
}

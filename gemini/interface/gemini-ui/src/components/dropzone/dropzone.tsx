import { Group, Text, rem } from "@mantine/core";
import { IconUpload, IconFile } from "@tabler/icons-react";
import { Dropzone, DropzoneProps } from "@mantine/dropzone";
import { openDataUploadModal } from "@/components/modals/modalhandler";
import useFileUpload from "@/hooks/useFileUpload";
import { useState } from "react";

export function FileDropzone(props: Partial<DropzoneProps>) {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

  const { uploadFiles, uploads } = useFileUpload({
    uploadPrefix: "web-uploaded-files",
  });

  function onDrop(files: File[]) {
    setSelectedFiles(files);
    uploadFiles(files);
  }

  return (
    <div>
      <Dropzone
        onDrop={onDrop}
        style={{
          border: "2px dashed var(--mantine-color-dimmed)",
          borderRadius: rem(10),
        }}
        {...props}
      >
        <Group
          justify="center"
          gap="xl"
          mih={220}
          style={{ pointerEvents: "none" }}
        >
          <Dropzone.Accept>
            <IconUpload
              style={{
                width: rem(52),
                height: rem(52),
                color: "var(--mantine-color-blue-6)",
              }}
              stroke={1.5}
            />
          </Dropzone.Accept>
          <Dropzone.Idle>
            <IconFile
              style={{
                width: rem(60),
                height: rem(60),
                color: "var(--mantine-color-dimmed)",
              }}
              stroke={1.5}
            />
          </Dropzone.Idle>
          <div>
            <Text size="xl" fw={600} inline>
              Drag files here or click to browse files.
            </Text>
            <Text size="md" c="dimmed" inline mt={7}>
              You can attach as many files as you like.
            </Text>
            <Text size="md" c="dimmed" inline mt={7}>
              After upload, you will be asked information about the data.
            </Text>
          </div>
        </Group>
      </Dropzone>
    </div>
  );
}

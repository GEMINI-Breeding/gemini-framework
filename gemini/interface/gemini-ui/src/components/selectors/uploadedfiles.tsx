// import { useListState } from "@mantine/hooks";
import { useGEMINIUploadStore } from "@/store";
import { ScrollArea } from "@mantine/core";
import FileCard from "@/components/datacards/filecard";

export default function UploadedFilesSelector() {
  // Get global store state and actions
  const files = useGEMINIUploadStore((state) => state.files);
  const setFiles = useGEMINIUploadStore((state) => state.setFiles);

  // Create Items from the files
  const items = files.map((file) => {
    return (
      <FileCard
        key={file.name}
        file={file}
        onRemove={() => {
          setFiles(files.filter((f) => f !== file));
        }}
      />
    );
  });

  return (
    <div>
      <ScrollArea>{items}</ScrollArea>
    </div>
  );
}

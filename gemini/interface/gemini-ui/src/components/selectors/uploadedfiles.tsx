import { Table, ActionIcon } from "@mantine/core";
import { useGEMINIUploadStore } from "@/store";
import { IconX } from "@tabler/icons-react";

export default function UploadedFileSelector() {
  // Get global store state and actions
  const files = useGEMINIUploadStore((state) => state.files);
  const setFiles = useGEMINIUploadStore((state) => state.setFiles);

  // Delete Handler
  function deleteFile(file: File) {
    setFiles(files.filter((f) => f !== file));
  }

  // Create Items from the files
  const rows = files.map((file) => (
    <Table.Tr key={file.name}>
      <Table.Td>{file.name}</Table.Td>
      <Table.Td>{file.size}</Table.Td>
      <Table.Td>
        <ActionIcon
          color="red"
          onClick={() => {
            deleteFile(file);
          }}
        >
          <IconX />
        </ActionIcon>
      </Table.Td>
    </Table.Tr>
  ));

  return (
    <div>
      <Table stickyHeader stickyHeaderOffset={60}>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>File Name</Table.Th>
            <Table.Th>Size</Table.Th>
            <Table.Th>Remove</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>{rows}</Table.Tbody>
      </Table>
    </div>
  );
}

import { Drawer, Title } from "@mantine/core";
import useFileUpload from "@/hooks/useFileUpload";

interface TaskProgressDrawerProps {
  opened: boolean;
  onClose: () => void;
}

export default function TaskProgressDrawer({
  opened,
  onClose,
}: TaskProgressDrawerProps) {

  const { uploads } = useFileUpload({});


  return (
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
          <div>
            {uploads.map((upload) => {
              return (
                <div key={upload.id}>
                  <p>{upload.file.name}</p>
                  <progress value={upload.progress} max={100} />
                </div>
              );
            })}
          </div>
        </Drawer.Body>
      </Drawer.Content>
    </Drawer.Root>
  );
}

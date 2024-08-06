import { Modal } from "@mantine/core";

interface ModalComponentProps {
  opened: boolean;
  withCloseButton: boolean;
  modalTitle: string;
  onClose: () => void;
  children?: React.ReactNode;
}

export default function ModalComponent({
  opened,
  withCloseButton,
  modalTitle,
  onClose,
  children,
}: ModalComponentProps) {
  return (
    <Modal
      opened={opened}
      onClose={onClose}
      withCloseButton={withCloseButton}
      title={modalTitle}
    >
      {children}
    </Modal>
  );
}

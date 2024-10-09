import { Container, Text, Stack, Center } from "@mantine/core";

interface CenterMessageProps {
  message: string;
}

export default function CenterMessage({ message }: CenterMessageProps) {
  return (
    <Container fluid>
      <Stack justify="center" align="center">
        <Text ta="center" fw={600} size="xl" style={{ fontSize: 30 }}>
          <Center>{message}</Center>
        </Text>
      </Stack>
    </Container>
  );
}

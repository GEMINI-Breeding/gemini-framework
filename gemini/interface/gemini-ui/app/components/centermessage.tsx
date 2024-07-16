import {Container, Text} from "@mantine/core";

interface CenterMessageProps {
    message: string;
};

export default function CenterMessage({message}: CenterMessageProps) {
    return (
        <Container>
            <Text ta="center" size="xl">
                {message}
            </Text>
        </Container>
    );
}

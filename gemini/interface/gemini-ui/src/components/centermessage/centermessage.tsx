import {Container, Text, Stack} from "@mantine/core";

interface CenterMessageProps {
    message: string;
};

export default function CenterMessage({message}: CenterMessageProps) {
    return (
        <Container fluid>
            <Stack justify="center" align="center" style={{height: "100vh"}}>
                <Text ta="center" fw={600} size="xl" style={{fontSize:30}}>
                    {message}
                </Text>
            </Stack>
        </Container>
    );
}
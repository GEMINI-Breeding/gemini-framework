import React from "react";
import { Container, Text } from "@mantine/core";

export default function CenterMessage({ message }: { message: string }) {
    return (
        <Container>
            <Text ta="center" size="xl"> 
                {message}
            </Text>
        </Container>
    );
}
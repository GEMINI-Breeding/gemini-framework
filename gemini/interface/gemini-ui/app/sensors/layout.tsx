import type { Metadata } from "next";
import { Space, Stack } from "@mantine/core";
import { Divider, Title } from "@mantine/core";

export const metadata: Metadata = {
  title: "GEMINI Sensors",
  description: "User Interface to browse and work with GEMINI Sensors"
};

export default function SensorLayout({ children} : Readonly<{children: React.ReactNode;}>) {
    return (
        <div>
            <Title order={1}>Sensors</Title>
            <Divider />
            <Space h="md" />
            <Stack gap="md">
                {children}
            </Stack>
        </div>
    );
}


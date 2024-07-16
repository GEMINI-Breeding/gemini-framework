import { Divider, Space, Title, Stack } from "@mantine/core";
import { Outlet } from "@remix-run/react";

export default function SensorLayout() {
    return (
        <div>
            <Title order={1}>Sensors</Title>
            <Divider />
            <Space h="md" />
            <Stack gap="md">
                <Outlet />
            </Stack>
        </div>
    );
}

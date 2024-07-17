import {Space, Stack} from "@mantine/core";
import {Divider, Title} from "@mantine/core";

export default function SensorLayout({children}: Readonly<{children: React.ReactNode;}>) {
    return (
        <div>
            <Title order={1}>Sensors</Title>
            <Divider />
            <Space h="md" />
            <div>
                {children}
            </div>
        </div>
    );
}
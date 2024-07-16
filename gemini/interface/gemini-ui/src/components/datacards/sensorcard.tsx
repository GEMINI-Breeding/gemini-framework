import { Sensor } from "@/api/types";
import { Button, Badge, Paper, Group, Text, Box} from "@mantine/core";
import { GEMINIDataFormats, GEMINIDataTypes, GEMINISensorTypes } from "@/api/enums";
import Link from "next/link";

interface SensorCardProps {
    sensor: Sensor;
}

export default function SensorCard({ sensor }: SensorCardProps) {
    return (
        <Paper p="lg" shadow="xs" style={{ marginBottom: 10 }}>
            <Group justify="space-between">
                <Group>
                    <Text size="xl" fw={700}>
                        {sensor.sensor_name}
                    </Text>
                    <Badge color="blue" variant="filled">
                        {GEMINISensorTypes[sensor.sensor_type_id]}
                    </Badge>
                    <Badge color="green" variant="filled">
                        {GEMINIDataTypes[sensor.sensor_data_type_id]}
                    </Badge>
                    <Badge color="red" variant="filled">
                        {GEMINIDataFormats[sensor.sensor_data_format_id]}
                    </Badge>
                </Group>
                <Group>
                    <Button>View Info</Button>
                    <Button>
                        <Link href={`/sensors/${sensor.id}`}>View Data</Link>
                    </Button>
                </Group>
            </Group>
        </Paper>
    );
}
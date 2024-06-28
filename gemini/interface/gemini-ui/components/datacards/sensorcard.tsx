import { Sensor } from "@/api/types";
import { Badge, Card, CardSection, Group, Text, Box} from "@mantine/core";
import { Button, Grid, GridCol } from "@mantine/core";
import classes from './cards.module.css';
import Link from "next/link";

interface SensorCardProps {
    sensor_id: string;
    sensor: Sensor;
}

export default function SensorCard({ sensor_id, sensor }: SensorCardProps) {
    return (
        <div>
            <Box className={classes.sensorcard}>
                <Group justify="space-between">
                    <Group>
                        <Text size="xl" fw={700}>
                            {sensor.sensor_name}
                        </Text>
                        <Badge color="blue" variant="filled">
                            {sensor.sensor_type_id}
                        </Badge>
                    </Group>
                    <Group>
                        <Button>
                            View Info
                        </Button>
                        <Button>
                            <Link href={`/sensors/${sensor_id}`} passHref>
                                View Data
                            </Link>
                        </Button>
                    </Group>             
                </Group>
            </Box>
        </div>
    );
}
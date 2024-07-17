import Sensors from "@/api/sensors";
import { Sensor } from "@/api/types";
import SensorCard from "@/components/datacards/sensorcard";
import CenterMessage from "@/components/centermessage/centermessage";
import { Stack } from "@mantine/core";

export default async function SensorsView() {
    const sensors = await Sensors.getSensors();
    return (
        <div>
            <Stack gap="md">
                {sensors.length > 0 ? (
                    sensors.map((sensor: Sensor) => (
                        <SensorCard key={sensor.id} sensor={sensor} />
                    ))
                ) : (
                    <CenterMessage message="No sensors found."/>
                )}
            </Stack>
        </div>
    );
}
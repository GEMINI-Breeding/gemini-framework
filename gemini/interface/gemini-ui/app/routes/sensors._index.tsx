import { Divider, Space, Stack } from "@mantine/core";
import Sensors from "api/sensors";
import { Sensor } from "api/types";
import { useLoaderData } from "@remix-run/react";

import SensorCard from "app/components/datacards/sensorcard";
import CenterMessage from "app/components/centermessage/centermessage";

export async function loader() {
    const sensors = await Sensors.getSensors();
    return sensors;
};

export default function SensorsView() {
    
    const sensors = useLoaderData<Sensor[]>();
    
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
    )
};
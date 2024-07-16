import { LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import Sensors from "api/sensors";
import { Sensor } from "api/types";
import SensorRecords from "api/sensor_records";
import { Divider, Space, Title } from "@mantine/core";
import DataViewer from "app/components/dataviewer/dataviewer";

export async function loader({params, } : LoaderFunctionArgs) {

    // Get the Sensor based on Sensor ID
    const sensor = await Sensors.getSensorById(params.sensor_id!);
    // Get the Sensor Records Generator based on Sensor ID
    const sensorData = await SensorRecords.getSensorRecords({sensor_id: params.sensor_id!});

    return {
        sensor: sensor,
        sensorData: sensorData
    };
}

export default function SensorDataView() {

    const sensor = useLoaderData<{sensor: Sensor}>().sensor;
    const sensorDataGenerator = useLoaderData<{sensorData: AsyncGenerator}>().sensorData as AsyncGenerator;

    return (
        <div>
            <Title order={3}>Showing Data for Sensor: {sensor.sensor_name}</Title>
            <Space h="md" />
            <DataViewer columns={[]} recordsGenerator={sensorDataGenerator} />
        </div>
    )
};



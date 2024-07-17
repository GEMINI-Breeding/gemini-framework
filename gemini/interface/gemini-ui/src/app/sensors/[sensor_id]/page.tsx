import {Divider, Space, Title} from "@mantine/core";
import Sensors from "@/api/sensors";
import SensorRecords from "@/api/sensor_records";

export default async function SensorDataView({params} : {params: {sensor_id: string}}) {
    const sensor = await Sensors.getSensorById(params.sensor_id);
    const sensorData = await SensorRecords.getSensorRecords({sensor_id: params.sensor_id});

    return (
        <div>
            <Title order={3}>{sensor.sensor_name}</Title>
            <Divider />
            <Space h="md" />
        </div>
    );
}
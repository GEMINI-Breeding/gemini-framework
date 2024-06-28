import { Divider, Space, Title } from "@mantine/core";
import Sensors from "@/api/sensors";
import { Sensor } from "@/api/types";
import SensorCard from "@/components/datacards/sensorcard";


export default async function SensorsView() {

    const sensors = await Sensors.getSensors();
    console.log(sensors);

    return (
        <div>
            <div>
                {sensors.map((sensor: Sensor) => (
                    <div key={sensor.id}>
                        <SensorCard sensor={sensor} sensor_id={sensor.id} key={sensor.id} />
                        <Space h="md" />
                        <Divider />
                    </div>
                ))}
            </div>
        </div>
    );
}
import { Divider, Space, Title } from "@mantine/core";
import Sensors from "@/api/sensors";
import { Sensor } from "@/api/types";
import SensorCard from "@/components/datacards/sensorcard";
import CenterMessage from "@/components/centermessage";


export default async function SensorsView() {

    const sensors = await Sensors.getSensors();   

    return (
        <div>
            <div>
            {sensors.length > 0 ? (
                sensors.map((sensor: Sensor) => (
                    <div key={sensor.id}>
                        <SensorCard sensor={sensor} />
                        <Space h="md" />
                        <Divider />
                    </div>
                ))
            ) : (
                <CenterMessage message="No sensors found."/>
            )}
            </div>
        </div>
    );
}

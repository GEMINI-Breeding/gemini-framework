import { Divider, Space, Title } from "@mantine/core";
import Sensors from "@/app/api/sensors";
import SensorRecords from "@/app/api/sensor_records";
import DataViewer from "@/components/dataviewer/dataviewer";

export default async function SensorDataView({params} : {params: {sensor_id: string}}) {
    
    const sensor = await Sensors.getSensorById(params.sensor_id);
    const sensorData = await SensorRecords.getSensorRecords({sensor_id: params.sensor_id});

    return (
        <div>
            <Title order={3}>{sensor.sensor_name}</Title>
            <Divider />
            <Space h="md" />
            <div>
                {/* {sensorData.length > 0 ? (
                    <DataViewer 
                        records={sensorData.map(SensorRecords.flattenSensorRecord)} 
                        columns={Object.keys(SensorRecords.flattenSensorRecord(sensorData[0]))} 
                    />
                ) : (
                    <div>No data found for sensor {sensor.sensor_name}</div>
                )} */}
            </div>
        </div>

    );
}

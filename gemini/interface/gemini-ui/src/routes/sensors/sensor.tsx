import { useState } from "react";
import { useParams } from "react-router";
import { useQuery } from "@tanstack/react-query";
import { Space, Title, Text } from "@mantine/core";

import { GEMINIDataTypes} from "@/api/enums";
import Sensor from "@/api/sensors";
import SensorRecords from "@/api/sensor_records";
import useProgressiveReadableStream from "@/hooks/useProgressiveReadableStream";
import SensorDataViewer from "@/components/dataviewer/sensordataviewer";
import SensorImageViewer from "@/components/dataviewer/sensorimageviewer";

export default function SensorView() {

    // Get the sensor name from the URL
    const {sensor_name} = useParams();

    // If no sensor name is provided, show a message
    if (!sensor_name) {
        return (
            <div>
                <Title order={3}>No Sensor Name Provided</Title>
                <Space h="md" />
                <Text>Please provide a sensor name in the URL</Text>
            </div>
        );
    }

    // Get Information about the sensor from API
    const { data: sensorData } = useQuery({
        queryKey: ["sensor", sensor_name],
        queryFn: async () => {
            return await Sensor.getSensor(sensor_name);
        }
    });

    // Set the query parameters
    const [params] = useState({sensor_name: sensor_name});

    // Fetch the sensor data using the useProgressiveReadableStream hook
    const {data : streamData, loading, error} = useProgressiveReadableStream(
        SensorRecords.getSensorRecords,
        params
    );

    const Header = (
        <div>
            <Title order={3}>{sensor_name}</Title>
            <Space h="md" />
        </div>
    );

    if (loading) {
        return (
            <div>
                {Header}
                <Text>Loading data...</Text>
            </div>
        );
    }

    if (error) {
        return (
            <div>
                {Header}
                <Text>Error Loading Data: {error.message}</Text>
            </div>
        );
    }

    // Flatten the data
    let flattened_data = streamData.map((record) => {
        return SensorRecords.flattenSensorRecord(record);
    });

    // Get the Sensor Type
    const sensorDataType = sensorData?.sensor_data_type_id;


    return (
        <div>
            {Header}
            {sensorDataType === GEMINIDataTypes.Image ? (
                <SensorImageViewer data={flattened_data} />
            ) : (
                <SensorDataViewer data={flattened_data} />
            )}
        </div>
    );

}


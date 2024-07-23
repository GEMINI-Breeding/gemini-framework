import Experiments from "@/api/experiments";
import SensorCard from "@/components/datacards/sensorcard";
import { useQuery } from "@tanstack/react-query";
// import { useEffect } from "react";
import useStore from "@/store";
import { Title, Divider, Space, Stack } from "@mantine/core";
import CenterMessage from "@/components/centermessage/centermessage";
import { useEffect } from "react";


export default function SensorsView() {
    const experiment = useStore((state) => state.experiment);

    const { data, refetch } = useQuery({
        queryKey: ["sensors"],
        queryFn: async () => {
            return await Experiments.getExperimentSensors(experiment);
        },
        enabled: !!experiment, // This ensures the query only runs when `experiment` is truthy
    });

    useEffect(() => {
        if (experiment) {
            refetch();
        }
    }, [experiment, refetch]);

    if (!experiment) {
        return <CenterMessage message="Please Select an Experiment" />;
    }

    return (
        <div>
            <ul>
                <Title order={1}>Sensors</Title>
                <Divider />
                <Space h="md" />
                <Stack gap="md">
                    {(data?.length ?? 0) > 0 ? (
                        data?.map((sensor) => (
                            <SensorCard key={sensor.id} sensor={sensor} />
                        ))
                    ) : (
                        <CenterMessage message={"No Sensors Found for experiment " + experiment} />
                    )}
                </Stack>    
            </ul>
        </div>
    );
}
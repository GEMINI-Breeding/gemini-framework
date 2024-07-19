// // import Sensors from "@/api/sensors";
// import Experiments from "@/api/experiments";
// import SensorCard from "@/components/datacards/sensorcard";
// import { useQuery } from "@tanstack/react-query";
// import useStore from "@/store";
// import { Title, Divider, Space, Stack } from "@mantine/core";
// import CenterMessage from "@/components/centermessage/centermessage";

// export default function SensorsView() {
    
//     const currentExperiment = useStore((state) => state.currentExperiment)

//     const { data } = useQuery({
//         queryKey: ["sensors"],
//         queryFn: async () => {
//             return await Experiments.getExperimentSensors(currentExperiment.experiment_name)
//         }
//     })

//     return (
//         <div>
//             <ul>
//                 <Title order={1}>Sensors</Title>
//                 <Divider />
//                 <Space h="md" />
//                 <Stack gap="md">
//                     {(data?.length ?? 0) > 0 ? (
//                         data?.map((sensor) => (
//                             <SensorCard key={sensor.id} sensor={sensor} />
//                         ))
//                     ) : (
//                         <CenterMessage message="No sensors found." />
//                     )}
//                 </Stack>
//             </ul>
//         </div>
//     )

// }
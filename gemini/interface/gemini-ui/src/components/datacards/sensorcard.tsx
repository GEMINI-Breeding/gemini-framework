import { Button, Badge, Paper, Group, Text} from "@mantine/core";
import { GEMINIDataFormats, GEMINIDataTypes, GEMINISensorTypes } from "@/api/enums";
import { Link } from "react-router-dom";

interface SensorCardProps {
    sensor: any;
}

export default function SensorCard({ sensor }: SensorCardProps) {
    return (
        <Paper shadow="md" radius="md" p="md" withBorder>
            <Group justify="space-between">
                <Group>
                    <Text size="xl" fw={700}>
                        {sensor.sensor_name}
                    </Text>
                    <Badge color="blue" variant="filled">
                        {GEMINISensorTypes[sensor.sensor_type_id]}
                    </Badge>
                    <Badge color="green" variant="filled">
                        {GEMINIDataTypes[sensor.sensor_data_type_id]}
                    </Badge>
                    <Badge color="red" variant="filled">
                        {GEMINIDataFormats[sensor.sensor_data_format_id]}
                    </Badge>
                </Group>
                <Group>
                    <Button>View Info</Button>
                    <Link to={`/sensors/${sensor.id}`}>
                        <Button>View Data</Button>
                    </Link>
                </Group>
            </Group>
        </Paper>
    );
}






// import { Sensor } from "@/api/types";
// import { Button, Badge, Paper, Group, Text} from "@mantine/core";
// import { GEMINIDataFormats, GEMINIDataTypes, GEMINISensorTypes } from "@/api/enums";
// // import Link from "next/link";

// interface SensorCardProps {
//     sensor: Sensor;
// }

// export default function SensorCard({ sensor }: SensorCardProps) {
//     return (
//         <Paper shadow="md" radius="md" p="md" withBorder>
//             <Group justify="space-between">
//                 <Group>
//                     <Text size="xl" fw={700}>
//                         {sensor.sensor_name}
//                     </Text>
//                     <Badge color="blue" variant="filled">
//                         {GEMINISensorTypes[sensor.sensor_type_id]}
//                     </Badge>
//                     <Badge color="green" variant="filled">
//                         {GEMINIDataTypes[sensor.sensor_data_type_id]}
//                     </Badge>
//                     <Badge color="red" variant="filled">
//                         {GEMINIDataFormats[sensor.sensor_data_format_id]}
//                     </Badge>
//                 </Group>
//                 <Group>
//                     <Button>View Info</Button>
//                     <Button>View Data</Button>
//                 </Group>
//             </Group>
//         </Paper>
//     );
// }
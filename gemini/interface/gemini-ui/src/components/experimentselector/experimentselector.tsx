import useStore from "@/store";
import { useQuery } from "@tanstack/react-query";
import { Input, InputBase, Combobox, useCombobox } from '@mantine/core';
import { Group, Text } from '@mantine/core';
import classes from './experimentselector.module.css';
import Experiments from "@/api/experiments";

export default function ExperimentSelector() {

    // Fetch Experiments
    const { data, isError, isLoading } = useQuery({
        queryKey: ["experiments"],
        queryFn: async () => {
            return await Experiments.getExperiments();
        },
        retry: true,
        retryDelay: 100,
    });

    // Get the current experiment from the global store and experiment setter
    const experiment = useStore((state) => state.experiment);
    const setExperiment = useStore((state) => state.setExperiment);

    // Function to set the experiment
    function onExperimentSelect(experiment_name: string) {
        setExperiment(experiment_name);
        combobox.closeDropdown();
    }

    // Combobox Store
    const combobox = useCombobox({});

    
    if (isLoading) {
        return <Text>Loading...</Text>;
    }

    if (isError) {
        return <Text>Error Fetching Experiments</Text>;
    }

    if (data?.length === 0) {
        return <Text>No Experiments Found</Text>;
    }

    return (
        <Group gap={10}>
            <Text size="xl" fw={500}>Choose Experiment: </Text>
            <Combobox
                store={combobox}
                onOptionSubmit={onExperimentSelect}
            >
                <Combobox.Target>
                    <InputBase
                        className={classes.selector}
                        component="button"
                        type="button"
                        pointer
                        rightSection={<Combobox.Chevron />}
                        onClick={() => combobox.toggleDropdown()}
                        rightSectionPointerEvents="none"
                    >
                        {experiment ?? <Input.Placeholder>Select Experiment</Input.Placeholder>}
                    </InputBase>
                </Combobox.Target>
                <Combobox.Dropdown>
                    <Combobox.Options>
                        {data?.map((experiment) => (
                            <Combobox.Option key={experiment.experiment_name} value={experiment.experiment_name}>
                                {experiment.experiment_name}
                            </Combobox.Option>
                        ))}
                    </Combobox.Options>
                </Combobox.Dropdown>
            </Combobox>
        </Group>
    );
}



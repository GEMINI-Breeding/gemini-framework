import { useQuery } from "@tanstack/react-query";
import useStore from "@/store";
import Experiments from "@/api/experiments"
import { Input, InputBase, Combobox, useCombobox } from '@mantine/core';
import {Group, Text} from '@mantine/core';
import classes from './experimentselector.module.css';

export default function ExperimentSelector() {

    const { data } = useQuery({
        queryKey: ["experiments"],
        queryFn: Experiments.getExperiments,
    });

    const currentExperiment = useStore((state) => state.currentExperiment);
    const setCurrentExperiment = useStore((state) => state.setCurrentExperiment);

    // Combobox Store
    const combobox = useCombobox({
        onDropdownClose: () => combobox.resetSelectedOption(),
    });

    function submitAction(experiment_name: any) {

        const experiment = data?.find((experiment) => experiment.experiment_name === experiment_name);
        setCurrentExperiment(experiment);

        // Close the dropdown
        combobox.closeDropdown();
    }


    const options = data?.map((experiment) => {
        return (
            <Combobox.Option value={experiment.experiment_name} key={experiment.id}>
                {experiment.experiment_name}
            </Combobox.Option>
        );
    });

    return (
        <Group gap={10}>
        <Text size="xl" fw={500}>Choose Experiment: </Text>
        <Combobox
            store = {combobox}
            onOptionSubmit={submitAction}
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
                    {currentExperiment.experiment_name ?? <Input.Placeholder>Select Experiment</Input.Placeholder>}
                </InputBase>
            </Combobox.Target>
            <Combobox.Dropdown>
                <Combobox.Options>
                    {options}
                </Combobox.Options>
            </Combobox.Dropdown>
        </Combobox>
        </Group>
    )
}

"use client";

import { Group, Select, Text } from '@mantine/core';
import { useState } from 'react';
import experimentsAPI from "@/app/api/experiments";

interface ExperimentSelectorProps {
    experimentNames: string[];
}

export default async function ExperimentSelector({ experimentNames }: ExperimentSelectorProps) {

    const [selectedExperiment, setSelectedExperiment] = useState<string|null>(null);

    return (
        <div>
        <Group>
            <Text size="xl" fw={600}>Choose Experiment</Text>
            <Select value={selectedExperiment} onChange={setSelectedExperiment} data={experimentNames}>
            </Select>
        </Group>
        </div>
    )
}
import { TextInput, Stack, Group, Button, Select} from "@mantine/core";
import { DatePickerInput, DateValue } from "@mantine/dates";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import Experiments from "@/api/experiments";
import Seasons from "@/api/seasons";

export default function SeasonCreateForm() {


    // Local State for storing season to be created
    const [experimentName, setExperimentName] = useState<string>("");
    const [seasonName, setSeasonName] = useState<string>("");
    const [seasonStartDate, setSeasonStartDate] = useState<Date | null>(null);
    const [seasonEndDate, setSeasonEndDate] = useState<Date | null>(null);

    // Get Experiments to choose from, from the API
    const { data: experiments } = useQuery({
        queryKey: ["experiments"],
        queryFn: Experiments.getExperiments,
    });
    
    // Create a mutation to create a new season
    const createSeason = useMutation({
        mutationKey: ["create_season", experimentName],
        mutationFn: async (newSeason: object) => {
            return await Seasons
        },
    });

    // Input Handlers

    // Handle form submission

    return (
        <div>
            <Stack>
                <Select
                    data
            </Stack>
        </div>
    )



}
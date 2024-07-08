"use client";

import experiments from "@/api/experiments";
import { MantineProvider } from "@mantine/core";
import { createContext } from "react";
import { Experiment, Season, Sensor, Site, Trait } from "@/api/types";


interface GEMINIContextProps {
    experiments: Experiment[];
    currentExperiment: Experiment;
    seasons: Season[];
    sites: Site[];
    sensors: Sensor[];
    traits: Trait[];
}

const GEMINIContext = createContext<GEMINIContextProps>({} as GEMINIContextProps);

// GEMINI Provider
export default function GEMINIProvider({ ...props }: GEMINIContextProps) {

    return (
        <GEMINIContext.Provider value={{...props}}>
        </GEMINIContext.Provider>
    )
}

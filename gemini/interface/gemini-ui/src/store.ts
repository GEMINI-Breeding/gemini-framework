import { create } from 'zustand';
import { Experiment, Sensor, Trait } from "@/api/types";

type GEMINIStore = {
    experiment: Experiment,
    sensor: Sensor,
    trait: Trait,
    sensor_filter_params: object,
    trait_filter_params: object,
    setSensorFilterParams: (params: object) => void,
    setTraitFilterParams: (params: object) => void,
    setExperiment: (experiment: Experiment) => void,
    setSensor: (sensor: Sensor) => void,
    setTrait: (trait: Trait) => void,
}

const useStore = create<GEMINIStore>((set) => ({
    experiment: {} as Experiment,
    sensor: {} as Sensor,
    trait: {} as Trait,
    sensor_filter_params: {},
    trait_filter_params: {},
    setSensorFilterParams: (params) =>
        set((state) => ({
            ...state,
            sensor_filter_params: params
        })),
    setTraitFilterParams: (params) =>
            set((state) => ({
                ...state,
                trait_filter_params: params
            })),
    setExperiment: (experiment) =>
            set((state) => ({
                ...state,
                experiment
            })),
    setSensor: (sensor) =>
            set((state) => ({
                ...state,
                sensor
            })),
    setTrait: (trait) =>
            set((state) => ({
                ...state,
                trait
            })),
}));


export default useStore;
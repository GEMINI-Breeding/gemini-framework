import { create } from 'zustand';

type GEMINIStore = {
    experiment: any,
    sensor: any,
    trait: any,
    setExperiment: (experiment: any) => void,
    setSensor: (sensor: any) => void,
    setTrait: (trait: any) => void,
}


const useStore = create<GEMINIStore>((set) => ({
    experiment: null,
    sensor: null,
    trait: null,
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
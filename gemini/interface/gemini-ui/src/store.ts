import {configureStore} from '@reduxjs/toolkit';


// import {create} from 'zustand';
// import zustymiddleware from 'zustymiddleware';

// type GEMINIStore = {
//     currentExperiment: any;
//     currentSensor: any;
//     currentTrait: any;
//     currentPlot: any;
//     setCurrentExperiment: (experiment: any) => void;
//     setCurrentSensor: (sensor: any) => void;
//     setCurrentTrait: (trait: any) => void;
//     setCurrentPlot: (plot: any) => void;
// }

// const useStore = create<GEMINIStore>(zustymiddleware((set: any) => ({
//     currentExperiment: {},
//     currentSensor: {},
//     currentTrait: {},
//     currentPlot: {},
//     setCurrentExperiment: (experiment: Object) => set({currentExperiment: experiment}),
//     setCurrentSensor: (sensor: Object) => set({currentSensor: sensor}),
//     setCurrentTrait: (trait: Object) => set({currentTrait: trait}),
//     setCurrentPlot: (plot: Object) => set({currentPlot: plot}),
// })));

// (window as any).store = useStore;
// export default useStore;


import { create } from "zustand";
import {
  Experiment,
  Season,
  Sensor,
  Trait,
  SensorPlatform,
  Site,
} from "@/api/types";

type GEMINIState = {
  experiments: string[];
  seasons: string[];
  platforms: string[];
  sensors: string[];
  traits: string[];
  sites: string[];
  currentExperiment: Experiment;
  currentSeason: Season;
  currentPlatform: SensorPlatform;
  currentSensor: Sensor;
  currentTrait: Trait;
  currentSite: Site;
};

type GEMINIUploadState = {
  uploadType: string;
  experiment: string;
  sensor: string;
  trait: string;
  site: string;
  platform: string;
  files: File[];
};

type GEMINIUploadAction = {
  setUploadType: (uploadType: string) => void;
  setExperiment: (experiment: string) => void;
  setSensor: (sensor: string) => void;
  setTrait: (trait: string) => void;
  setSite: (site: string) => void;
  setPlatform: (platform: string) => void;
  setFiles: (files: File[]) => void;
};

type GEMINIAction = {
  setExperiments: (experiments: string[]) => void;
  setSeasons: (seasons: string[]) => void;
  setPlatforms: (platforms: string[]) => void;
  setSensors: (sensors: string[]) => void;
  setTraits: (traits: string[]) => void;
  setSites: (sites: string[]) => void;
  setCurrentExperiment: (experiment: Experiment) => void;
  setCurrentSeason: (season: Season) => void;
  setCurrentPlatform: (platform: SensorPlatform) => void;
  setCurrentSensor: (sensor: Sensor) => void;
  setCurrentTrait: (trait: Trait) => void;
  setCurrentSite: (site: Site) => void;
};

type GEMINIStore = GEMINIState & GEMINIAction;
type GEMINIUploadStore = GEMINIUploadState & GEMINIUploadAction;

export const useGEMINIStore = create<GEMINIStore>((set) => ({
  experiments: [],
  seasons: [],
  platforms: [],
  sensors: [],
  traits: [],
  sites: [],
  currentExperiment: {} as Experiment,
  currentSeason: {} as Season,
  currentPlatform: {} as SensorPlatform,
  currentSensor: {} as Sensor,
  currentTrait: {} as Trait,
  currentSite: {} as Site,
  setExperiments: (experiments: string[]) =>
    set(() => ({ experiments: experiments })),
  setSeasons: (seasons: string[]) => set(() => ({ seasons: seasons })),
  setPlatforms: (platforms: string[]) => set(() => ({ platforms: platforms })),
  setSensors: (sensors: string[]) => set(() => ({ sensors: sensors })),
  setTraits: (traits: string[]) => set(() => ({ traits: traits })),
  setSites: (sites: string[]) => set(() => ({ sites: sites })),
  setCurrentExperiment: (experiment: Experiment) =>
    set(() => ({ currentExperiment: experiment })),
  setCurrentSeason: (season: Season) => set(() => ({ currentSeason: season })),
  setCurrentPlatform: (platform: SensorPlatform) =>
    set(() => ({ currentPlatform: platform })),
  setCurrentSensor: (sensor: Sensor) => set(() => ({ currentSensor: sensor })),
  setCurrentTrait: (trait: Trait) => set(() => ({ currentTrait: trait })),
  setCurrentSite: (site: Site) => set(() => ({ currentSite: site })),
}));

export const useGEMINIUploadStore = create<GEMINIUploadStore>((set) => ({
  uploadType: "",
  experiment: "",
  sensor: "",
  trait: "",
  site: "",
  platform: "",
  files: [],
  setUploadType: (uploadType: string) =>
    set(() => ({ uploadType: uploadType })),
  setExperiment: (experiment: string) =>
    set(() => ({ experiment: experiment })),
  setSensor: (sensor: string) => set(() => ({ sensor: sensor })),
  setTrait: (trait: string) => set(() => ({ trait: trait })),
  setSite: (site: string) => set(() => ({ site: site })),
  setPlatform: (platform: string) => set(() => ({ platform: platform })),
  setFiles: (files: File[]) => set(() => ({ files: files })),
}));

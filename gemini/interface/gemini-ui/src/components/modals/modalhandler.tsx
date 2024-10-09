import { modals } from "@mantine/modals";

// Modals' Content
import DataUploadForm from "@/components/forms/dataupload";
import ExperimentCreateForm from "@/components/forms/experimentcreate";
import SeasonCreateForm from "@/components/forms/seasoncreate";
import SensorCreateForm from "@/components/forms/sensorcreate";
import SiteCreateForm from "@/components/forms/sitecreate";
import TraitCreateForm from "@/components/forms/traitcreate";

export function openDataUploadModal() {
  modals.open({
    title: "Upload Data",
    children: <DataUploadForm />,
  });
}

export function openExperimentCreateModal() {
  modals.open({
    title: "Create Experiment",
    children: <ExperimentCreateForm />,
  });
}

export function openSeasonCreateModal() {
  modals.open({
    title: "Create Season",
    children: <SeasonCreateForm />,
  });
}

export function openSensorCreateModal() {
  modals.open({
    title: "Create Sensor",
    children: <SensorCreateForm />,
  });
}

export function openSiteCreateModal() {
  modals.open({
    title: "Create Site",
    children: <SiteCreateForm />,
  });
}

export function openTraitCreateModal() {
  modals.open({
    title: "Create Trait",
    children: <TraitCreateForm />,
  });
}

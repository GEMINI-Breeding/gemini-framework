import { modals } from "@mantine/modals";

// Modals' Content
import DataUploadForm from "@/components/forms/dataupload";
import ExperimentCreateForm from "@/components/forms/experimentcreate";
import UploadedFilesSelector from "@/components/selectors/uploadedfiles";

export function openDataUploadModal() {
  modals.open({
    title: "Upload Data",
    children: <DataUploadForm />,
  });
}

export function openFileSelectorModal() {
  modals.open({
    title: "Select Files",
    children: <UploadedFilesSelector />,
  });
}

export function openExperimentCreateModal() {
  modals.open({
    title: "Create Experiment",
    children: <ExperimentCreateForm />,
  });
}

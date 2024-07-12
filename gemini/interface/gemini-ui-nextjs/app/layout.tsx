import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

// Mantine
import "@mantine/core/styles.css"
import GEMINIProvider from "./providers";
import { MantineProvider } from "@mantine/core";
import Shell from "@/components/shell/shell";

import experimentsAPI from "@/app/api/experiments";
import { Experiment } from "@/app/api/types";

export const metadata: Metadata = {
  title: "GEMINI",
  description: "User Interface to browse and work with GEMINI Data"
};


export async function getGEMINIProps() {
  debugger;
  const experiments = await experimentsAPI.getExperiments();

  if (experiments.length === 0) {
    return {
      experiments: [],
      currentExperiment: null,
      seasons: [],
      sites: [],
      sensors: [],
      traits: []
    };
  }

  const currentExperiment = experiments[0];
  const seasons = await experimentsAPI.getExperimentSeasons(currentExperiment.experiment_name);
  const sites = await experimentsAPI.getExperimentSites(currentExperiment.experiment_name);
  const sensors = await experimentsAPI.getExperimentSensors(currentExperiment.experiment_name);
  const traits = await experimentsAPI.getExperimentTraits(currentExperiment.experiment_name);

  return {
    experiments,
    currentExperiment,
    seasons,
    sites,
    sensors,
    traits
  };
}


export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  const serverProps = await getGEMINIProps();

  return (
    <html lang="en">
      <head>
      </head>
      <body className={inter.className}>
        <GEMINIProvider {...serverProps}>
          <MantineProvider>
            <Shell>{children}</Shell>
          </MantineProvider>
        </GEMINIProvider>
      </body>
    </html>
  );
}

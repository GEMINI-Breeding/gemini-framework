"use client";

import { NextUIProvider } from "@nextui-org/system";
import { createContext } from "react";

// Create a Custom Context Provider for GEMINI Project
const GEMINIContext = createContext({});
const GEMINIContextProvider = GEMINIContext.Provider;

export function Providers({ children } : { children: React.ReactNode }) {
  return (
    <GEMINIContextProvider value={{}}>
      <NextUIProvider>
        {children}
      </NextUIProvider>
    </GEMINIContextProvider>
  );
}


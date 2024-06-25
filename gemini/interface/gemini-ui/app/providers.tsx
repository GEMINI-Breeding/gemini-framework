"use client";

import { NextUIProvider } from "@nextui-org/system";
import { createContext } from "react";
import { ThemeProvider as NextThemeProvider } from "next-themes";
import { ThemeProviderProps } from "next-themes/dist/types";

// Create a Custom Context Provider for GEMINI Project
const GEMINIContext = createContext({});
const GEMINIContextProvider = GEMINIContext.Provider;

export interface ProvidersProps {
  children: React.ReactNode;
  themeProps?: ThemeProviderProps;
}

export function Providers({ children, themeProps } : ProvidersProps) {
  return (
      <NextUIProvider>
        <NextThemeProvider {...themeProps}>
          {children}
        </NextThemeProvider>
      </NextUIProvider>
  );
}


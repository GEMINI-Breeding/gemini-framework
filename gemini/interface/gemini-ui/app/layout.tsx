import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

// Mantine
import "@mantine/core/styles.css"
import {ColorSchemeScript, DEFAULT_THEME, MantineProvider} from "@mantine/core";
import { createTheme, MantineGradient } from "@mantine/core";

export const metadata: Metadata = {
  title: "GEMINI",
  description: "User Interface to browse and work with GEMINI Data"
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
      </head>
      <body className={inter.className}>
        <MantineProvider defaultColorScheme="light">{children}</MantineProvider>
      </body>
    </html>
  );
}

import type { Metadata } from "next";
import { Inter } from "next/font/google";

// Mantine
import "@mantine/core/styles.css"
import { MantineProvider, ColorSchemeScript } from "@mantine/core";
import Shell from "@/components/shell/shell";

export default async function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
    return (
        <html lang="en">
            <head>
                <ColorSchemeScript />
            </head>
            <body>
                <MantineProvider>
                    <Shell>
                        {children}
                    </Shell>
                </MantineProvider>
            </body>
        </html>
    );
}
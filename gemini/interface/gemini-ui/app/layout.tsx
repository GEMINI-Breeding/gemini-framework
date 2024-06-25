import "@/styles/globals.css";
import type { Metadata } from "next";
import { Providers } from "./providers";
import React from "react";

import LayoutNavbar from "@/components/layout/navbar";
import { fontSans } from "@/config/fonts";
import clsx from "clsx";

type RootLayoutProps = {
  children: React.ReactNode;
};

export const metadata: Metadata = {
  title: "GEMINI",
  description: "User Interface to browse and upload GEMINI Data"
};

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html suppressHydrationWarning lang="en">
      <body className={clsx(
          "min-h-screen bg-background font-sans antialiased",
          fontSans.variable,
        )}>
        <Providers themeProps={{ attribute: "class", defaultTheme: "light" }}>
          <LayoutNavbar />
          {children}
        </Providers>
      </body>
    </html>
  );
}

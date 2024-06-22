import type { Metadata } from "next";
import { Providers } from "./providers";
import React from "react";

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
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

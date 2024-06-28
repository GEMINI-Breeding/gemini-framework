import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

// Mantine
import "@mantine/core/styles.css"
import { MantineProvider} from "@mantine/core";
import Shell from "@/components/shell/shell";

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
        <MantineProvider defaultColorScheme="light">
          <Shell>{children}</Shell>
        </MantineProvider>
      </body>
    </html>
  );
}

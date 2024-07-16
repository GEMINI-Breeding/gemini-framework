// Layout.tsx
import '@mantine/core/styles.css';

import { Links, Meta, Scripts } from "@remix-run/react";
import { ReactNode } from "react";
import { MantineProvider, ColorSchemeScript } from "@mantine/core";
import Shell from "./components/shell/shell";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <html>
      <head>
        <link rel="icon" href="data:image/x-icon;base64,AA" />
        <Meta />
        <Links />
        <ColorSchemeScript />
      </head>
      <body>
        <Scripts />
        <MantineProvider>
            <Shell>{children}</Shell>
        </MantineProvider>
      </body>
    </html>
  );
}
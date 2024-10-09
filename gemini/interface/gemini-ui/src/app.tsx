import "@mantine/core/styles.css";
import "@mantine/dropzone/styles.css";
import "@mantine/dates/styles.css";
import { MantineProvider } from "@mantine/core";
import { ModalsProvider } from "@mantine/modals";
import AppRoutes from "@/routes";
import Shell from "./components/shell/shell";



export default function App() {
  return (
    <div>
      <MantineProvider>
        <ModalsProvider>
          <Shell>
            <AppRoutes />
          </Shell>
        </ModalsProvider>
      </MantineProvider>
    </div>
  );
}

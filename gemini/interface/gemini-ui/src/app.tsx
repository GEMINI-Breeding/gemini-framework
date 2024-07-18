import '@mantine/core/styles.css';
import {MantineProvider} from '@mantine/core';
import AppRoutes from '@/routes';
import Shell from './components/shell/shell';


export default function App() {
    return (
        <div>
            <MantineProvider>
                <Shell>
                    <AppRoutes />
                </Shell>
            </MantineProvider>
        </div>
    );
}


import {Routes, Route, Outlet} from 'react-router-dom';
// import Shell from '@/components/shell/shell';
// import SensorsView from '@/routes/sensors/sensors';
// import SensorView from './routes/sensors/sensor';
import SensorsList from './routes/sensors/sensorslist';
import Home from '@/routes/home';

export default function AppRoutes() {
    return (
        <Routes>
            <Route path="/" element={<Outlet />}>
                <Route index element={<Home />} />
                <Route path="sensors" element={<SensorsList />} />
                {/* <Route path="sensors" element={<SensorsView />}>
                    <Route path=":sensor_name" element={<SensorView />} />
                </Route> */}
            </Route>
        </Routes>
    );
}
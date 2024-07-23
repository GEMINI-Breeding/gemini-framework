import {Routes, Route, Outlet} from 'react-router-dom';
// import Shell from '@/components/shell/shell';
import SensorsView from '@/routes/sensors/sensors';
import Home from '@/routes/home';

export default function AppRoutes() {
    return (
        <Routes>
            <Route path="/" element={<Outlet />}>
                <Route index element={<Home />} />
                <Route path="sensors" element={<SensorsView />} /> 
            </Route>
        </Routes>
    );
}
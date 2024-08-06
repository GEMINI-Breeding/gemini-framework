import { Routes, Route, Outlet } from "react-router-dom";
// import SensorsList from './routes/sensors/sensorslist';
import FileUpload from "@/routes/upload/fileupload";
import Home from "@/routes/home";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Outlet />}>
        <Route index element={<Home />} />
        {/* <Route path="sensors" element={<SensorsList />} /> */}
        <Route path="upload" element={<FileUpload />} />
        {/* <Route path="sensors" element={<SensorsView />}>
                    <Route path=":sensor_name" element={<SensorView />} />
                </Route> */}
      </Route>
    </Routes>
  );
}

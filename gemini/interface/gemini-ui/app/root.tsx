import Layout from "./layout";
import { Outlet, LiveReload, ScrollRestoration } from "@remix-run/react";

export default function App() {
    return (
        <Layout>
            <ScrollRestoration />
            <Outlet />
        </Layout>
    )
}
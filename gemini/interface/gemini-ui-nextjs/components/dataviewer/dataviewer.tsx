import { DataTable, DataTableColumn } from "mantine-datatable";
import SensorRecords from "@/app/api/sensor_records";
import { Suspense } from "react";
import { LoadingOverlay } from "@mantine/core";
import { ReadableStream } from "node:stream/web";

interface DataViewerProps {
    columns: string[];
    records?: any[];
    stream?: ReadableStream;
}

export default function DataViewer({ columns, records }: DataViewerProps) {
    
    // Function to convert string list of columns to DataTableColumn list
    function getColumns(columns: string[]): DataTableColumn[] {
        return columns.map((column) => {
            // Convert underscore case to proper casing with capitalization
            const title = column.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ');
            return {
                accessor: column,
                title: title
            };
        });
    }
    
    return (
        <div>
            <DataTable
                columns={getColumns(columns)}
                records={records}
            />
        </div>
    );
}
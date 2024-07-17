"use client";

import {DataTable, DataTableColumn} from "mantine-datatable";
import useReadableStream from "@/hooks/useReadableStream";

interface DataViewerProps {
    columns: string[];
    records?: any[];
    stream?: ReadableStream<Object>;
}

function toDataTableColumns(columns: string[]): DataTableColumn[] {
    return columns.map((column) => {
        const title = column.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ');
        return {
            accessor: column,
            title: title
        };
    });
}

export default function DataViewer({columns, records, stream}: DataViewerProps) {
    
    const {data, error, loading} = useReadableStream(async () => stream!, [stream]);
    
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <div>
            {data.map((record, index) => (
                <div key={index}>{JSON.stringify(record)}</div>
            ))}
        </div>
    );
}
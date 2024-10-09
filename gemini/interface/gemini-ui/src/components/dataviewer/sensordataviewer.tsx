import { DataTable, DataTableColumn } from "mantine-datatable";
import { useEffect, useState } from "react";
import { Sensor, SensorRecord } from "@/api/types";

const PAGE_SIZE = 10;

interface SensorDataViewerProps {
    sensor: Sensor;
    data: SensorRecord[];
}

/**
 * Retrieves the columns from the given data.
 * 
 * @param data - The data from which to retrieve the columns.
 * @returns An array of strings representing the columns.
 */
function getColumnsFromData(data: any): string[] {
    if (data.length === 0) {
        return [];
    }
    let columns = Object.keys(data[0]);
    // Remove Columns with id in the name
    columns = columns.filter(column => !column.includes('id'));
    return columns;
}

/**
 * Converts an array of column names into an array of DataTableColumn objects.
 * @param columns - The array of column names.
 * @returns An array of DataTableColumn objects.
 */
function toDataTableColumns(columns: string[]): DataTableColumn[] {
    return columns.map((column) => {
        const title = column.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ');
        return {
            accessor: column,
            title: title
        };
    });
}


export default function SensorDataViewer({data}: SensorDataViewerProps) {
    
    const columns = getColumnsFromData(data);
    const [page, setPage] = useState(1);
    const [records, setRecords] = useState(data.slice(0, PAGE_SIZE));

    useEffect(() => {
        const from = (page - 1) * PAGE_SIZE;
        const to = page * PAGE_SIZE;
        setRecords(data.slice(from, to));
    }, [page]);

    return (
        <DataTable
            withTableBorder
            borderRadius="sm"
            withColumnBorders
            striped
            highlightOnHover
            columns={toDataTableColumns(columns)}
            records={records}
            totalRecords={data.length}
            recordsPerPage={PAGE_SIZE}
            page={page}
            onPageChange={(newPage) => setPage(newPage)}
        />
    );
}

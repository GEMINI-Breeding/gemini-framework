import {DataTable, DataTableColumn} from "mantine-datatable";
import { useAsyncGenerator } from "hooks";

interface DataViewerProps {
    columns: string[];
    records?: any[];
    recordsGenerator?: AsyncGenerator;
}

// Function to convert string list of columns to DataTableColumn list
function toDataTableColumns(columns: string[]): DataTableColumn[] {
    return columns.map((column) => {
        const title = column.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ');
        return {
            accessor: column,
            title: title
        };
    });
}

export default function DataViewer({ columns, records, recordsGenerator }: DataViewerProps) {
    
    console.log(columns);
    
    return (
        <div>
            <h1>Datatable</h1>
        </div>
    );
}
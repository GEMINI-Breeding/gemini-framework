"use client";

import { useState } from "react";
import { DataTable, DataTableColumn } from "mantine-datatable";

import {
    Table,
    UnstyledButton,
    Group,
    Text,
    Center,
    TextInput,
    rem,
    keys,
} from "@mantine/core";
import { IconSelector, IconChevronDown, IconChevronUp, IconSearch } from '@tabler/icons-react';

interface DataViewerProps {
    reversed?: boolean;
    sorted?: boolean;
    records?: any[];
    columns: DataTableColumn[];
    sourceUrl?: string;
}

export default function DataViewer({ reversed, sorted, records, columns, sourceUrl }: DataViewerProps) {
    return (
        <div>
             <DataTable
                columns={columns}
                records={records}
            />
        </div>
    )
}
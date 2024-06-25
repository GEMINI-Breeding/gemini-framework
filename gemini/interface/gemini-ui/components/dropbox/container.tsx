"use client"

import React, { useCallback, useState } from "react";
import { TargetBox } from "./target-box";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";


export default function Container() {
    const [droppedFiles, setDroppedFiles] = useState<File[]>([])
    
    const handleFileDrop = useCallback(
        (item: {files: any[]}) => {
            if (item) {
                const files = item.files.map((file: any) => file)
                setDroppedFiles(files)
            }
        }
    , [setDroppedFiles]
    )

    return (
        <div>
            <DndProvider backend={HTML5Backend}>
                <TargetBox onDrop={handleFileDrop} />
            </DndProvider>
            <div>
                Dropped Files:
                {droppedFiles.map((file, index) => (
                    <div key={index}>
                        {file.name}
                    </div>
                ))}
            </div>
        </div>
    )


}
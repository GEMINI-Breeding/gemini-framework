import React, { useCallback, useState } from "react";
import { TargetBox } from "./target-box";


export default function Container() {
    const [droppedFiles, setDropedFiles] = useState<File[]>([])
    
    const handleFileDrop = useCallback
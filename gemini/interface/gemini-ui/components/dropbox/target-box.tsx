import { DropTargetMonitor } from 'react-dnd';
import { useDrop } from 'react-dnd';
import { NativeTypes } from 'react-dnd-html5-backend';

type TargetBoxProps = {
    onDrop: (item: { files: any[] }) => void;
};


export function TargetBox ({ onDrop }: TargetBoxProps) {

    const [{ canDrop, isOver }, drop] = useDrop(() => ({
        accept: [NativeTypes.FILE],
        drop(item, monitor) {
            if (onDrop) {
                onDrop(item as { files: any[] });
            }
        },
        collect: (monitor: DropTargetMonitor) => ({
            isOver: monitor.isOver(),
            canDrop: monitor.canDrop(),
        }),
    }));

    const isActive = canDrop && isOver;

    return (
        <div style={{ width: '100%', height: '100%', position: 'relative' }}>
            {isActive ? 'Release to drop' : 'Drag file here'}
        </div>
    );
}



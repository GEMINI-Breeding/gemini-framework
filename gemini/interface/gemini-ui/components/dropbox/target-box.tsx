import { useRef } from 'react';
import { DropTargetMonitor } from 'react-dnd';
import { useDrop } from 'react-dnd';
import { NativeTypes } from 'react-dnd-html5-backend';

type TargetBoxProps = {
    onDrop: (item: { files: any[] }) => void;
};


export function TargetBox ({ onDrop }: TargetBoxProps) {

    const dropRef = useRef<HTMLDivElement>(null);
    const [{ canDrop, isOver }, drop] = useDrop(
        () => ({
          accept: [NativeTypes.FILE],
          drop(item: { files: any[] }) {
            console.log('drop', item.files)
            if (onDrop) {
              onDrop(item)
            }
          },
          canDrop(item: any) {
            console.log('canDrop', item.files, item.items)
            return true
          },
          hover(item: any) {
            console.log('hover', item.files, item.items)
          },
          collect: (monitor: DropTargetMonitor) => {
            const item = monitor.getItem() as any
            if (item) {
              console.log('collect', item.files, item.items)
            }
    
            return {
              isOver: monitor.isOver(),
              canDrop: monitor.canDrop(),
            }
          },
        })
    )

    drop(dropRef);
    const isActive = canDrop && isOver;

    return (
            <div ref={dropRef} style={{ border: '1px solid gray',
                height: '15rem',
                width: '15rem',
                padding: '2rem',
                textAlign: 'center' }}>
                {isActive ? 'Release to drop' : 'Drag file here'}
            </div>
        );
}



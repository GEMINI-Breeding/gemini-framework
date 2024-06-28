"use client";

import { Text, Group, Button, rem} from '@mantine/core';
import { Dropzone, DropzoneProps, FileWithPath, MIME_TYPES } from '@mantine/dropzone';
import { DropzoneAccept, DropzoneReject, DropzoneIdle } from '@mantine/dropzone';
import { IconCloudUpload, IconX, IconDownload, IconUpload, IconFile } from '@tabler/icons-react';
import '@mantine/dropzone/styles.css';
import classes from './dragdrop.module.css';

export default function DragDrop(props: Partial<DropzoneProps>) {

    function onDrop(files: FileWithPath[]) {
        console.log(files);
    }

    return (
        <div>
            <Dropzone onDrop={onDrop} {...props} className={classes.root}>
            <Group justify="center" gap="lg" mih={220} style={{ pointerEvents: 'none' }}>
                <DropzoneAccept>
                    <IconUpload
                        style={{ width: rem(52), height: rem(52)}}
                        stroke={1.5}
                    />
                </DropzoneAccept>
                <DropzoneReject>
                    <IconX
                        style={{ width: rem(52), height: rem(52)}}
                        stroke={1.5}
                    />
                </DropzoneReject>
                <DropzoneIdle>
                    <IconFile
                        style={{ width: rem(52), height: rem(52)}}
                        stroke={1.5}
                    />
                </DropzoneIdle>

                <div>
                    <Text size="xl" fw={600}  inline>
                        Drag your data here or select files
                    </Text>
                    <Text size="sm" c="dimmed" inline mt={7}>
                        You can attach as many files as you want
                    </Text>
                </div>
            </Group>
            </Dropzone>
        </div>
    )
}
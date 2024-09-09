import { useCallback, useState } from "react";
import { getObjectUploadURL } from "@/api/files";

interface Upload {
  file: File;
  progress: number;
  status: "PENDING" | "UPLOADING" | "COMPLETE" | "ERROR";
  error?: string;
}

interface useFileUploadProps {
  uploadBucket?: string;
  uploadPrefix?: string;
  onUploadComplete?: (file: File, status: Upload) => void;
  onUploadsComplete?: (statuses: Upload[]) => void;
}

const useFileUpload = ({
  uploadBucket,
  uploadPrefix,
  onUploadComplete,
  onUploadsComplete,
}: useFileUploadProps) => {
  const [uploads, setUploads] = useState<Upload[]>([]);

  const uploadFiles = useCallback(
    async (files: File[]) => {
      const newStatuses = files.map((file) => ({
        file,
        progress: 0,
        status: "PENDING" as const,
      }));

      setUploads(newStatuses);

      await Promise.all(
        files.map(async (file, index) => {
          try {
            // Complete Object Name from file name and prefix
            const objectName = `${uploadPrefix}/${file.name}`;

            // Get Presigned URL
            const presignedURLResponse = await getObjectUploadURL(
              objectName,
              uploadBucket
            );
            if (Object.keys(presignedURLResponse).length === 0) {
              throw new Error("Error getting presigned URL");
            }
            const presignedURL = presignedURLResponse.url;

            // Upload the file
            const uploadRequest = new XMLHttpRequest();

            uploadRequest.upload.onprogress = (event) => {
              let progress = (event.loaded / event.total) * 100;
              progress = Math.round(progress);
              setUploads((prevUploads) =>
                prevUploads.map((upload, i) =>
                  i === index
                    ? { ...upload, progress, status: "UPLOADING" }
                    : upload
                )
              );
            };

            uploadRequest.onload = () => {
              setUploads((prevUploads) =>
                prevUploads.map((upload, i) =>
                  i === index
                    ? { ...upload, progress: 100, status: "COMPLETE" }
                    : upload
                )
              );
              onUploadComplete?.(file, {
                file,
                progress: 100,
                status: "COMPLETE",
              });
            };

            uploadRequest.open("PUT", presignedURL);
            uploadRequest.send(file);
          } catch (error) {
            console.error("Error uploading file: ", error);
            setUploads((prevUploads) =>
              prevUploads.map((upload, i) =>
                i === index
                  ? {
                      ...upload,
                      status: "ERROR",
                      error: (error as Error).message,
                    }
                  : upload
              )
            );
            onUploadComplete?.(file, {
              file,
              progress: 0,
              status: "ERROR",
              error: (error as Error).message,
            });
          }
        })
      );

      onUploadsComplete?.(uploads);
    },
    [onUploadComplete, onUploadsComplete]
  );

  return { uploadFiles, uploads };
};

export default useFileUpload;

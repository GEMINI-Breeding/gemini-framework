import { create } from "zustand";
import { useCallback } from "react";
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

interface UploadState {
  uploads: Upload[];
  addUpload: (upload: Upload) => void;
  updateUpload: (index: number, updatedUpload: Partial<Upload>) => void;
  removeUpload: (index: number) => void;
}

const useUploadStore = create<UploadState>((set) => ({
  uploads: [],
  addUpload: (upload) =>
    set((state) => ({ uploads: [...state.uploads, upload] })),
  updateUpload: (index, updatedUpload) =>
    set((state) => ({
      uploads: state.uploads.map((upload, i) =>
        i === index ? { ...upload, ...updatedUpload } : upload
      ),
    })),
  removeUpload: (index) =>
    set((state) => ({ uploads: state.uploads.filter((_, i) => i !== index) })),
}));

const useFileUpload = ({
  uploadBucket,
  uploadPrefix,
  onUploadComplete,
  onUploadsComplete,
}: useFileUploadProps) => {
  const { uploads, addUpload, updateUpload } = useUploadStore();

  const handleFileUpload = useCallback(
    async (file: File, index: number) => {
      try {
        const objectName = `${uploadPrefix}/${file.name}`;
        const presignedURLResponse = await getObjectUploadURL(
          objectName,
          uploadBucket
        );

        if (Object.keys(presignedURLResponse).length === 0) {
          throw new Error("Error getting presigned URL");
        }

        const presignedURL = presignedURLResponse.url;
        const uploadRequest = new XMLHttpRequest();

        uploadRequest.upload.onprogress = (event) => {
          const progress = Math.round((event.loaded / event.total) * 100);
          updateUpload(index, { progress, status: "UPLOADING" });
        };

        uploadRequest.onload = () => {
          updateUpload(index, { progress: 100, status: "COMPLETE" });
          onUploadComplete?.(file, {
            file,
            progress: 100,
            status: "COMPLETE",
          });
        };

        uploadRequest.onerror = () => {
          const errorMessage = `Failed to upload ${file.name}. Please try again.`;
          updateUpload(index, { status: "ERROR", error: errorMessage });
          onUploadComplete?.(file, {
            file,
            progress: 0,
            status: "ERROR",
            error: errorMessage,
          });
        };

        uploadRequest.open("PUT", presignedURL);
        uploadRequest.send(file);
      } catch (error) {
        console.error(`Error uploading file ${file.name}: `, error);
        const errorMessage = `Failed to upload ${file.name}. Please try again.`;
        updateUpload(index, { status: "ERROR", error: errorMessage });
        onUploadComplete?.(file, {
          file,
          progress: 0,
          status: "ERROR",
          error: errorMessage,
        });
      }
    },
    [onUploadComplete, uploadBucket, uploadPrefix, updateUpload]
  );

  const uploadFiles = useCallback(
    async (files: File[]) => {
      const initialUploadStatuses = files.map(
        (file): Upload => ({
          file,
          progress: 0,
          status: "PENDING",
        })
      );
      initialUploadStatuses.forEach(addUpload);

      try {
        await Promise.all(files.map(handleFileUpload));
        onUploadsComplete?.(uploads);
      } catch (error) {
        console.error("An error occurred during the upload process:", error);
        // Handle generic upload error
      }
    },
    [addUpload, handleFileUpload, onUploadsComplete, uploads]
  );

  return { uploadFiles, uploads };
};

export default useFileUpload;

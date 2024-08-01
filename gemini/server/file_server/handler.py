import hashlib, os
import mimetypes
from minio import Minio
from minio.error import S3Error
from typing import Generator, BinaryIO


class MinioFileHandler:
    def __init__(self):
        
        is_local = os.getenv("GEMINI_LOCAL") == "true"
        minio_hostname = os.getenv("MINIO_HOSTNAME") if not is_local else "localhost"
        minio_port = os.getenv("MINIO_PORT", 9000)
        minio_access_key = os.getenv("MINIO_ACCESS_KEY")
        minio_secret_key = os.getenv("MINIO_SECRET_KEY") 
        minio_secure = False

        self.minio_client = Minio(
            f"{minio_hostname}:{minio_port}",
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=minio_secure
        )

        self.bucket_name = os.getenv("MINIO_BUCKET", "gemini")

        # Create the bucket if it doesn't exist
        if not self.minio_client.bucket_exists(self.bucket_name):
            self.minio_client.make_bucket(self.bucket_name)


    def file_exists(self, object_name: str, file_hash: str = None) -> bool:
        """
        Checks if a file exists with the given name and optionally with the specified hash.

        Args:
            object_name (str): Name of the object in the bucket.
            file_hash (str, optional): MD5 hash of the file. If provided, also verifies the hash.

        Returns:
            bool: True if the file exists (and hash matches if provided), False otherwise.
        """
        try:
            obj = self.minio_client.stat_object(self.bucket_name, object_name)
            if file_hash:
                return obj.etag == file_hash
            return True
        except S3Error as e:
            if e.code == "NoSuchKey":
                return False
            raise  # Re-raise other exceptions

    def upload_file(self, object_name: str, data_stream: BinaryIO, metadata: dict = None) -> str:
        """
        Uploads a file from a stream and returns the object URL.

        Args:
            object_name (str): Name of the object in the bucket.
            data_stream (BytesIO): BytesIO stream containing the file data.
            metadata (dict, optional): Additional metadata to store with the object.

        Returns:
            str: The presigned URL of the uploaded object.
        """



        file_hash = self.calculate_hash(data_stream)

        if self.file_exists(object_name, file_hash):
            return self.minio_client.presigned_get_object(self.bucket_name, object_name)

        # Get the length of the stream
        data_stream.seek(0, os.SEEK_END)
        file_length = data_stream.tell()
        data_stream.seek(0)

        # Define the part size for multipart uploads
        part_size = 5 * 1024 * 1024


        self.minio_client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            data=data_stream,
            length=file_length,
            part_size=part_size,
            content_type=self.get_mimetype(object_name)
        )

        return self.minio_client.presigned_get_object(self.bucket_name, object_name)

    def download_file(self, object_name: str, destination_file_path: str) -> str:
        """
        Downloads a file to a stream and returns the stream object.

        Args:
            object_name (str): Name of the object in the bucket.

        Returns:
            BytesIO: The BytesIO stream containing the downloaded file data.
        """
        response = self.minio_client.get_object(self.bucket_name, object_name)
        with open(destination_file_path, "wb") as file:
            for chunk in response.stream(32 * 1024):
                file.write(chunk)
        response.close()
        response.release_conn()
        return file_path
    
    def get_download_url(self, object_name: str) -> str:
        """
        Generates a presigned URL to download a file.

        Args:
            object_name (str): Name of the object in the bucket.

        Returns:
            str: The presigned URL to download the object.
        """
        return self.minio_client.presigned_get_object(self.bucket_name, object_name)
    
    def stream_file(self, object_name: str, chunk_size: int = 1024 * 1024) -> Generator[bytes, None, None]:
        """
        Streams a file from MinIO in chunks, yielding bytes.

        Args:
            object_name (str): The name of the object in the bucket.
            chunk_size (int): The size of each chunk to yield (in bytes).

        Yields:
            bytes: A chunk of the file data.
        """
        response = self.minio_client.get_object(self.bucket_name, object_name)
        for chunk in response.stream(chunk_size):
            yield chunk
        response.close()
        response.release_conn()

    def stream_lines(self, object_name: str, chunk_size: int = 1024 * 1024) -> Generator[str, None, None]:
        """
        Streams a file from MinIO line by line, yielding strings.

        Args:
            object_name (str): The name of the object in the bucket.
            chunk_size (int): The size of each chunk to read (in bytes).

        Yields:
            str: A line of the file data.
        """
        response = self.minio_client.get_object(self.bucket_name, object_name)
        buffer = ""
        for chunk in response.stream(chunk_size):
            buffer += chunk.decode("utf-8")
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                yield line
        if buffer:
            yield buffer
        response.close()
        response.release_conn()

    def delete_file(self, object_name: str) -> None:
        """
        Deletes a file from the bucket.

        Args:
            object_name (str): Name of the object to delete.
        """
        self.minio_client.remove_object(self.bucket_name, object_name)

    def list_files(self, prefix: str = None) -> list[str]:
        """
        Lists files in the bucket, optionally filtered by a prefix.

        Args:
            prefix (str, optional): If provided, only files with this prefix are returned.

        Returns:
            list[str]: A list of object names.
        """
        objects = self.minio_client.list_objects(self.bucket_name, prefix=prefix, recursive=True)
        return [obj.object_name for obj in objects]
    
    def create_bucket(self, bucket_name: str, region: str = None) -> None:
        """
        Creates a new bucket in MinIO.

        Args:
            bucket_name (str): The name of the bucket to create.
            region (str, optional): The region to create the bucket in (defaults to None for MinIO).

        Raises:
            BucketAlreadyOwnedByYou: If you already own a bucket with the same name.
            BucketAlreadyExists: If a bucket with the same name exists and is owned by someone else.
            S3Error: For other MinIO-related errors.
        """
        try:
            # Check if the bucket already exists
            if self.minio_client.bucket_exists(bucket_name):
                raise S3Error("BucketAlreadyOwnedByYou", f"Bucket '{bucket_name}' already exists")

            # Create the bucket
            self.minio_client.make_bucket(bucket_name, location=region)

        except S3Error as e:
            print(f"Error creating bucket '{bucket_name}': {e}")
            raise  # Re-raise the exception for further handling if needed

    
    def calculate_hash(self, data_stream: BinaryIO) -> str:
        """
        Calculates the MD5 hash of a data stream.

        Args:
            data_stream (BinaryIO): BytesIO stream containing the data.

        Returns:
            str: The MD5 hash of the data.
        """
        md5_hash = hashlib.md5()
        data_stream.seek(0)
        for chunk in iter(lambda: data_stream.read(4096), b""):
            md5_hash.update(chunk)
        return md5_hash.hexdigest()
    

    def get_mimetype(self, file_path: str) -> str:
        """
        Retrieves the MIME type of a file.

        Args:
            file_path (str): The path of the file.

        Returns:
            str: The MIME type of the file.
        """
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type



if __name__ == "__main__":
    file_handler = MinioFileHandler()
    
    file_to_upload = "sample.txt"
    file_path = os.path.join(os.path.dirname(__file__), file_to_upload)
    object_name = "sample.txt"

    with open(file_path, "rb") as file:
        file_handler.upload_file(object_name, file)

    # Stream Lines
    for line in file_handler.stream_lines(object_name):
        print(line)



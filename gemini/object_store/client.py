import minio
from minio.commonconfig import Tags, CopySource
import mimetypes, os, tempfile

from gemini.utilities import hashing
from gemini.logger import logger_service
from datetime import timedelta


class StorageClient:

    data_folder = f"{tempfile.gettempdir()}/gemini/data"

    def __init__(self, host, port, access_key, secret_key, secure=False):
        self.client = minio.Minio(
            endpoint=f"{host}:{port}",
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self.default_bucket = "gemini"
        if not self.client.bucket_exists(self.default_bucket):
            self.client.make_bucket(self.default_bucket)

    def tags_match(self, key, bucket, tags: dict) -> bool:
        remote_tags = self.client.get_object_tags(bucket, key)
        if remote_tags == tags:
            return True
        return False

    def digests_match(self, local_file_path, key, bucket) -> bool:
        local_file_digest = hashing.get_file_digest(local_file_path)
        remote_file_stat = self.stat_file(key, bucket)
        if remote_file_stat:
            remote_file_digest = remote_file_stat["file_etag"]
            return local_file_digest == remote_file_digest
        return False

    def make_bucket(self, bucket) -> None:
        """
        Create a new bucket
        """
        try:
            self.client.make_bucket(bucket)
        except Exception as e:
            pass

    def object_exists(self, key, bucket=None) -> bool:
        """
        Check if an object exists in the bucket
        """
        try:
            if not bucket:
                bucket = self.default_bucket
            self.client.stat_object(bucket, key)
            return True
        except:
            return False

    def update_object_tags(self, key, bucket, tags: dict) -> None:
        """
        Update tags for an object
        """
        try:
            if not tags:
                return
            remote_tags = self.client.get_object_tags(bucket, key)
            # Combine the tags, if similar keys then update, if new then add
            for key, value in tags.items():
                remote_tags[key] = value
            self.client.set_object_tags(bucket, key, remote_tags)
        except Exception as e:
            pass

    def set_object_tags(self, key, bucket, tags: dict) -> None:
        """
        Set tags for an object
        """
        try:
            if not tags:
                return
            tags = Tags(tags)
            self.client.set_object_tags(bucket, key, tags)
        except Exception as e:
            pass

    def get_object_tags(self, key, bucket) -> dict:
        """
        Get tags for an object
        """
        try:
            tags = self.client.get_object_tags(bucket, key)
            return tags
        except Exception as e:
            return None

    def put_file(
        self,
        source_file_path: str,
        destination_key: str,
        bucket=None,
        tags: dict = None,
    ) -> dict:
        """
        Put a file to the bucket
        """
        try:
            if not bucket:
                bucket = self.default_bucket
            if tags:
                tags = Tags(tags)
                return self.client.put_object(
                    bucket, destination_key, source_file_path, tags=tags
                )
            return self.client.put_object(bucket, destination_key, source_file_path)
        except Exception as e:
            return None

    def objects_match(self, key, bucket, file_path, tags: dict = None) -> bool:
        """
        Check if the file can be replaced
        """
        if not self.object_exists(key, bucket):
            return False

        digest_match = self.digests_match(file_path, key, bucket)
        tags_match = self.tags_match(key, bucket, tags)

        return digest_match and tags_match

    def upload_file(self, key, file_path = None, file_io = None, bucket=None, tags: dict = None):
        """
        Upload a file to the bucket
        """
        try:
            if file_path and file_io:
                raise ValueError("Both file path and file io cannot be provided")

            if file_path and os.path.exists(file_path):
                file_io = open(file_path, "rb")

            if not bucket:
                bucket = self.default_bucket

            if self.objects_match(key, bucket, file_path, tags):
                return None

            mimetype = mimetypes.guess_type(file_path)[0]
            remote_tags = self.get_object_tags(key, bucket)

            tags_to_insert = Tags()
            if remote_tags:
                tags_to_insert.update(remote_tags)
            tags_to_insert.update(tags) if tags else None

            # Convert all tags to string
            string_tags = {key: str(value) for key, value in tags_to_insert.items()}
            # Remove None values
            string_tags = {key: value for key, value in string_tags.items() if value}

            tags_to_insert.update(string_tags)

            write_result = self.client.put_object(
                bucket_name=bucket,
                object_name=key,
                data=file_io,
                length=os.path.getsize(file_path),
                content_type=mimetype,
                tags=tags_to_insert,
            )
            return write_result
        except Exception as e:
            return None
        

    def download_file(self, key, file_path=None, bucket=None) -> str:
        """
        Download a file from the bucket
        """
        try:
            if not bucket:
                bucket = self.default_bucket
            if not file_path:
                file_path = os.path.join(self.data_folder, key)
                file_path = os.path.normpath(file_path)
            self.client.fget_object(bucket, key, file_path)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File {file_path} not found")
            return file_path
        except Exception as e:
            return None

    def delete_file(self, key, bucket=None) -> bool:
        """
        Delete a file from the bucket
        """
        try:
            if not bucket:
                bucket = self.default_bucket
            self.client.remove_object(bucket, key)
            return True
        except Exception as e:
            return False

    def stat_file(self, key, bucket=None) -> dict:
        """
        Get file stat
        """
        try:
            if not bucket:
                bucket = self.default_bucket

            file_information = self.client.stat_object(bucket, key)
            file_information = {
                "original_file_name": key,
                "key": key,
                "bucket": bucket,
                "file_extension": os.path.splitext(key)[1],
                "file_mime_type": file_information.content_type,
                "file_size": file_information.size,
                "file_etag": file_information.etag,
                "file_metadata": file_information.metadata,
                "file_tags": (
                    dict(file_information.tags) if file_information.tags else {}
                ),
            }

            return file_information
        except Exception as e:
            return None

    def get_presigned_download_url(self, key, bucket=None, expires=3600) -> str:
        """
        Get a presigned download URL
        """
        try:
            if not bucket:
                bucket = self.default_bucket
            return self.client.presigned_get_object(
                bucket, key, expires=timedelta(seconds=expires)
            )
        except Exception as e:
            return None

    def get_presigned_upload_url(self, key, bucket=None, expires=3600) -> str:
        """
        Get a presigned upload URL
        """
        try:
            if not bucket:
                bucket = self.default_bucket
            return self.client.presigned_put_object(
                bucket, key, expires=timedelta(seconds=expires)
            )
        except Exception as e:
            return None

    def copy_object(
        self,
        source_key: str,
        destination_key: str,
        source_bucket: str = None,
        destination_bucket: str = None,
    ) -> dict:
        """
        Copy an object from one bucket to another
        """
        try:
            if not source_bucket:
                source_bucket = self.default_bucket
            if not destination_bucket:
                destination_bucket = self.default_bucket
            copy_source = CopySource(bucket_name=source_bucket, object_name=source_key)
            return self.client.copy_object(
                bucket_name=destination_bucket,
                object_name=destination_key,
                source=copy_source,
            )
        except Exception as e:
            return None

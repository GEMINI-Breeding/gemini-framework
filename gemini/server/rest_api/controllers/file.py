from litestar.controller import Controller
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.response import Response

from typing import List, Annotated, Optional

from gemini.server.rest_api.src.dependencies import file_handler
from gemini.server.rest_api.src.models import URLResponse

class FileController(Controller):

    @get('/download/url')
    async def get_object_download_url(
            self,
            object_name: str,
            bucket_name: str = 'gemini'
    ) -> URLResponse:
        """
        Get the download URL for a file in the bucket.

        Args:
            object_name (str): The name of the object in the bucket.
            bucket_name (str): The name of the bucket. Defaults to 'gemini'.

        Returns:
            URLResponse: The download URL for the object.
        """
        download_url = file_handler.get_download_url(object_name, bucket_name)
        return URLResponse(url=download_url)
    
    @get('/upload/url')
    async def get_object_upload_url(
            self,
            object_name: str,
            bucket_name: str = 'gemini'
    ) -> URLResponse:
        """
        Get the upload URL for a file in the bucket.

        Args:
            object_name (str): The name of the object in the bucket.
            bucket_name (str): The name of the bucket. Defaults to 'gemini'.

        Returns:
            URLResponse: The upload URL for the object.
        """
        upload_url = file_handler.get_upload_url(object_name, bucket_name)
        return URLResponse(url=upload_url)

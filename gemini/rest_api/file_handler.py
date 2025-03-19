import os
from litestar.datastructures import UploadFile

class RESTAPIFileHandler:

    def __init__(self, root_folder: str):
        self.root_folder = root_folder
        self.uploads_folder = os.path.join(self.root_folder, "uploads")
        self.downloads_folder = os.path.join(self.root_folder, "downloads")

        if not os.path.exists(self.uploads_folder):
            os.makedirs(self.uploads_folder)

        if not os.path.exists(self.downloads_folder):
            os.makedirs(self.downloads_folder)

    async def create_file(self, uploaded_file: UploadFile) -> str:
        original_file_name = uploaded_file.filename
        file_content = await uploaded_file.read()
        local_file_path = os.path.join(self.uploads_folder, original_file_name)
        with open(local_file_path, "wb") as f:
            f.write(file_content)
        local_file_path = os.path.abspath(local_file_path)
        return local_file_path

# Create a File Handler for uploads and downloads
home_dir = os.path.expanduser("~")
gemini_data_dir = os.path.join(home_dir, "gemini_data")
if not os.path.exists(gemini_data_dir):
    os.makedirs(gemini_data_dir)
api_file_handler = RESTAPIFileHandler(root_folder=gemini_data_dir)


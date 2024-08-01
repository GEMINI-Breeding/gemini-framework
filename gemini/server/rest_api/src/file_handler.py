import os
from litestar.datastructures import UploadFile

class FileHandler:
    
    def __init__(
        self,
        root_folder: str,
        upload_folder: str = None,
        download_folder: str = None
    ):
        
        # Create Root Folder
        if not os.path.exists(root_folder):
            os.makedirs(root_folder)
            
        # If upload folder is provided, create it
        if upload_folder:
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
        else:
            upload_folder = os.path.join(root_folder, "uploads")
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
                
        # If download folder is provided, create it
        if download_folder:
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)
        else:
            download_folder = os.path.join(root_folder, "downloads")
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)
                
        self.root_folder = root_folder
        self.upload_folder = upload_folder
        self.download_folder = download_folder
                
    async def create_file(self, uploaded_file: UploadFile) -> str:
        original_file_name = uploaded_file.filename
        file_content = await uploaded_file.read()
        local_file_path = os.path.join(self.upload_folder, original_file_name)
        with open(local_file_path, "wb") as file:
            file.write(file_content)
        local_file_path = os.path.abspath(local_file_path)
        return local_file_path
        

file_handler = FileHandler(root_folder="./gemini-data", upload_folder="./gemini-data/uploads", download_folder="./gemini-data/downloads")

from gemini.object_store.client import StorageClient
import os

islocal = os.getenv('GEMINI_IS_LOCAL')
islocal = True if islocal.lower() == 'true' else False
host = os.getenv('FILE_SERVER_HOSTNAME') if not islocal else 'localhost'
port = os.getenv('FILE_SERVER_PORT')
access_key = os.getenv('FILE_SERVER_S3_ACCESS_KEY')
secret_key = os.getenv('FILE_SERVER_S3_SECRET_KEY')

storage_service = StorageClient(
    host=host,
    port=port,
    access_key=access_key,
    secret_key=secret_key
)


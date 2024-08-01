from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os

islocal = os.getenv('GEMINI_LOCAL')
islocal = True if islocal.lower() == 'true' else False

db_username = os.getenv('DATABASE_USER')
db_password = os.getenv('DATABASE_PASSWORD')
db_host = os.getenv('DATABASE_HOSTNAME') if not islocal else 'localhost'
db_port = os.getenv('DATABASE_PORT')
db_name = os.getenv('DATABASE_NAME')

db_url = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

engine = create_engine(db_url)
session = Session(engine, autocommit=False, autoflush=True)
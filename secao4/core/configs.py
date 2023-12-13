from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    """
        Configurações gerais da API
    """
    API_V1_STR: str = "/api/v1"
    DB_URL: str = f"mysql+aiomysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DB')}"
    DBBaseModel = declarative_base()
    
    class Config:
        case_sensitive = True

settings = Settings()

from pydantic_settings import BaseSettings

from typing import Any

from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = f"mysql+aiomysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DB')}"
    DBBaseModel: Any = declarative_base()
    
    """
        import secrets
        token: str = secrets.token_urlsafe(32)
        token
    """
    JWT_SECRET: str = {os.getenv('JWT_SECRET')}
    ALGORITHM: str = 'HS256'
    ACESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 1 semana
    
    class Config:
        case_sensitive = True

settings: Settings = Settings()


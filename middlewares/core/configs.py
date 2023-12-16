from pydantic import BaseSettings

from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    API_V1_URL: str                  = "/api/v1",
    DB_URL: str                      = f"mysql+aiomysql://{os.getenv('DB_USER')}:{os.getenv('DB_PWD')}@{os.getenv('DB_HOST')}:3360/{os.getenv('DB_NAME')}",
    DBBaseModel                      = declarative_base()
    
    JWT_TYPE: str                    = "Bearer"
    JWT_SECRET: str                  = {os.getenv('JWT_SECRET')}
    ALGORITHM: str                   = 'HS256'
    # 120 MINUTOS = 2 HORAS
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    
    class Config:
        case_sensitive = True
        
settings: Settings = Settings()

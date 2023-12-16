from typing import Optional
from datetime import datetime, timezone

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from core.configs import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl = f"{settings.API_V1_URL}/users/login")

def authenticate():
    pass

def generate_jwt(subject: str, user_timezone: Optional[str] = "America/Sao_Paulo") -> str:
    payload = {
        "type": settings.JWT_TYPE,
        "exp": datetime.now(timezone(user_timezone) + settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.now(timezone(user_timezone)),
        "sub": subject
    }
    
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    

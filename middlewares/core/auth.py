from typing import Optional
from datetime import datetime, timezone

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from jose import jwt

from core.configs import settings
from core.database import Session
from core.deps import get_session
from core.security import verify_password
from models.__all__models import UserModel

oauth2_schema = OAuth2PasswordBearer(tokenUrl = f"{settings.API_V1_URL}/users/login")

def authenticate(
        cpf: str, password: str,
        session: Session = Depends(get_session)
    ) -> Optional[str]:
    try:
        query = select(UserModel).filter(UserModel.cpf == cpf)
        result = session.execute(query)
        user = result.scalars().one_or_none()
        
        if not user:
            return None
        
        if not verify_password(password, user.password):
            return None
        
        return user
    finally:
        session.close()

def generate_jwt(
        subject: str, user_timezone: Optional[str] = "America/Sao_Paulo"
    ) -> str:
    payload = {
        "type": settings.JWT_TYPE,
        "exp": datetime.now(timezone(user_timezone) + settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.now(timezone(user_timezone)),
        "sub": subject
    }
    
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    

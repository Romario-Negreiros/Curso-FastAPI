from fastapi.security import OAuth2PasswordBearer

from core.configs import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl = f"{settings.API_V1_URL}/login")



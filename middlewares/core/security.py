from passlib.context import CryptContext

CRYPT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password: str, password_hash: str) -> bool:
    return CRYPT.verify(password, password_hash)

def generate_password_hash(password: str) -> str:
    return CRYPT.hash(password)

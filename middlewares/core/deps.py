from typing import Generator, Optional

from pydantic import BaseModel

from core.database import Session

class TokenData(BaseModel):
    username: Optional[str] = None

def get_session() -> Generator:
    session: Session = Session()
    
    try:
        yield session
    finally:
        session.close()
    
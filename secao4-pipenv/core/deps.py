from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Session

async def get_session() -> Generator:
    session: AsyncSession = Session()
    
    try:
        yield session # devolve para uso
    finally:
        await session.close() # fecha a conexão com o banco

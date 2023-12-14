from core.configs import settings
from core.database import engine

async def create_table() -> None:
    import models.__all__models
    
    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)

if __name__ == "__main__":
    import asyncio
    
    asyncio.run(create_table())

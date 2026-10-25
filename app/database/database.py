from sqlalchemy import event
from collections.abc import AsyncGenerator
from ..server.configure import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

# Motor de la base de datos 

engine = create_async_engine(
    settings.database_url,
    echo = settings.enviroment == 'development'
)

# Session Maker

async_session = async_sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit=False
)

# Funcion para obtener session para la base de datos.

async def get_db() -> AsyncGenerator[
    AsyncSession,
    None
]:
    async with async_session() as session:
        yield session
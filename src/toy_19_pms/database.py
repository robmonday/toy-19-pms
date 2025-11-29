from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Database config
DATABASE_URL = "sqlite+aiosqlite:///toy_19_pms.db"  # aiosqlite for async SQLite

# Create async engine
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_session():
    """Async dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

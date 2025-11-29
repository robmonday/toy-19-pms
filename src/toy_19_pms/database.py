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

# Track if database has been initialized
_db_initialized = False


async def _ensure_db_initialized():
    """Initialize database tables if not already done."""
    global _db_initialized
    if not _db_initialized:
        from toy_19_pms.database_models import Base

        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        _db_initialized = True


@asynccontextmanager
async def get_session():
    """Async dependency to get database session. Auto-initializes DB on first use."""
    await _ensure_db_initialized()

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

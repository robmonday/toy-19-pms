from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

# Database config
DATABASE_URL: str = "sqlite+aiosqlite:///toy_19_pms.db"  # aiosqlite for async SQLite

# Create async engine - following SQLModel pattern
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


async def create_db_and_tables() -> None:
    """Create database tables. Call this once at app startup.

    Follows SQLModel best practice pattern from documentation.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session.

    Type-safe async context manager for database sessions.
    Automatically handles session lifecycle.
    """
    async with AsyncSession(engine) as session:
        yield session

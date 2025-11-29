from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = "sqlite:///toy_19_pms.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
)
SessionLocal = sessionmaker(bind=engine)


@contextmanager
def get_session():
    """Dependency to get database session"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

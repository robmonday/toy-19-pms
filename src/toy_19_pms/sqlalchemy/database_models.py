from typing import List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, declarative_base, relationship

from toy_19_pms.sqlalchemy.database import get_session as get_db_session  # noqa: F401 # for more efficient import

# Create Base first, before defining models
Base: DeclarativeBase = declarative_base()


# Define models
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(50), nullable=False)
    email: Mapped[Optional[str]] = Column(String(100), unique=True)

    # Type annotation for relationship
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, email={self.email})"


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String(200), nullable=False)
    content: Mapped[Optional[str]] = Column(String)
    user_id: Mapped[Optional[int]] = Column(Integer, ForeignKey("users.id"))

    # Type annotation for relationship
    author: Mapped[Optional["User"]] = relationship("User", back_populates="posts")

    def __repr__(self) -> str:
        return f"Post(id={self.id}, title={self.title!r}, user_id={self.user_id})"

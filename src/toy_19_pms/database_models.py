from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

# https://www.youtube.com/watch?v=GONyd0CUrP


# Define models using SQLModel (combines Pydantic + SQLAlchemy)
class User(SQLModel, table=True):
    """User model with type-safe fields."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    email: Optional[str] = Field(default=None, max_length=100, unique=True)

    # Relationship with type safety
    posts: list["Post"] = Relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, email={self.email})"


class Post(SQLModel, table=True):
    """Post model with type-safe fields."""

    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    content: Optional[str] = Field(default=None)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")

    # Relationship with type safety
    author: Optional["User"] = Relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"Post(id={self.id}, title={self.title!r}, user_id={self.user_id})"

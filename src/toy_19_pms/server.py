from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from toy_19_pms.database import create_db_and_tables, get_session
from toy_19_pms.database_models import Post


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown."""
    # Startup: Create database tables
    await create_db_and_tables()
    yield
    # Shutdown: cleanup if needed


# Initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)


# Type alias for cleaner annotations
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.get("/hello")
async def hello(session: SessionDep) -> str:
    return "Hello, World!"


@app.post("/posts/", response_model=Post)
async def create_post(post: Post, session: SessionDep) -> Post:
    await session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@app.get("/posts/", response_model=list[Post])
async def read_posts(session: SessionDep) -> list[Post]:
    stmt = select(Post).options(selectinload(Post.author))
    result = await session.exec(stmt)
    posts = result.all()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found")
    return posts


@app.get("/posts/{post_id}", response_model=Post)
async def read_post(post_id: int, session: SessionDep) -> Post:
    post = await session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def dev():
    """Run the development server with auto-reload."""

    print("Running development server...")

    uvicorn.run("toy_19_pms.server:app", host="0.0.0.0", port=8000, reload=True)

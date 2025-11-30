import asyncio

from sqlalchemy.orm import selectinload
from sqlmodel import select

from toy_19_pms.database import create_db_and_tables
from toy_19_pms.database_models import Post, get_db_session


async def main():
    await create_db_and_tables()  # run at app startup

    # Get database session for query
    async with get_db_session() as session:
        # Query posts with eager loading of author relationship
        # selectinload prevents N+1 queries in async context
        stmt = select(Post).where(Post.title == "My First Post").options(selectinload(Post.author))

        result = await session.exec(stmt)
        posts = result.all()

        # Print all posts with their authors
        print(f"Found {len(posts)} post(s):")
        for post in posts:
            author_name = post.author.name if post.author else "No author"
            print(f"  - {post.title} by {author_name}")


if __name__ == "__main__":
    asyncio.run(main())

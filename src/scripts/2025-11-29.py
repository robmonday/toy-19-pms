import asyncio

from sqlalchemy import select

from toy_19_pms.sqlalchemy.database_models import Post, get_db_session


async def main():
    async with get_db_session() as session:
        # Query all posts
        result = await session.execute(select(Post))
        posts = result.scalars().all()

        # Print all posts
        print(f"Found {len(posts)} post(s):")
        for post in posts:
            print(f"  - {post}")


if __name__ == "__main__":
    asyncio.run(main())

from toy_19_pms.database import get_session
from toy_19_pms.database_models import Post, User


def main():
    with get_session() as session:
        user = User(name="John Doe", email="john.doe@example.com")
        session.add(user)
        session.commit()  # Commit to get the user.id

        post = Post(title="My First Post", content="This is my first post", user_id=user.id)
        session.add(post)
        session.commit()
        print(user)
        print(post)


if __name__ == "__main__":
    main()

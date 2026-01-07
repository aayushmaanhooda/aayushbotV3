from .auth import get_password_hash
from .db import create_db_and_tables, engine
from .models import User
from sqlmodel import Session, select
from dotenv import load_dotenv

import os

load_dotenv()

username = os.getenv("LOGIN_USER_NAME")
password = os.getenv("PASSWORD")


def create_user(username: str, password: str):
    hashed_password = get_password_hash(password)

    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == username)).first()
        if existing:
            print("User already exists:", username)
            return existing

        user = User(username=username, hash_password=hashed_password)
        session.add(user)
        session.commit()
        session.refresh(user)

    print("✅ User created successfully!")
    print("ID:", user.id)
    print("Username:", user.username)
    return user


if __name__ == "__main__":
    # Create a test user
    create_user(username=username, password=password)

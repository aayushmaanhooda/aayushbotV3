from sqlmodel import Field, SQLModel, create_engine, Session
from dotenv import load_dotenv
from .models import User
import os

# Whenever you create a class that inherits from SQLModel
# and is configured with table = True, it is registered in this metadata attribute.

load_dotenv()

file_name = os.getenv("DB_FILE_NAME")
sqlite_url = f"sqlite:///{file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

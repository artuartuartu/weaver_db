import os

from sqlmodel import SQLModel, Session, create_engine

from database.models import User, Project  # noqa: F401

DB_FILE = os.getenv("DB_FILE", "weaver.db")
engine = create_engine(f"sqlite:///{DB_FILE}", echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

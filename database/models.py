from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    name: str | None = None
    provider: str = Field(nullable=False)
    provider_id: str = Field(unique=True, nullable=False)
    is_vip: bool = Field(default=False, nullable=False)


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: str = Field(primary_key=True)
    name: str = Field(nullable=False)
    file_path: str = Field(nullable=False)
    updated_at: str = Field(nullable=False)
    user_email: str = Field(foreign_key="users.email", nullable=False)

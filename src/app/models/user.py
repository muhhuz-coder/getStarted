from sqlmodel import SQLModel, Field


class Users(SQLModel, table=True):
    __tablename__ = "users"  
    id: int = Field(default=None, primary_key=True, index=True)
    username: str = Field(sa_column_kwargs={"unique": True}, index=True)
    email: str = Field(sa_column_kwargs={"unique": True}, index=True)
    full_name: str = Field(default=None, nullable=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
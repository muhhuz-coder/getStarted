from typing import Optional
from sqlmodel import SQLModel, Field

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int

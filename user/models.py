import os
import pathlib
from enum import Enum as PyEnum

from sqlmodel import SQLModel, create_engine, Session, Field, Relationship, Enum
from typing import List


# Define the Enum for Status
class Status(PyEnum):
    FOLLOWING = 1
    BLOCKED = 0


class FollowRelationship(SQLModel, table=True):
    class Config:
        orm_mode = True

    by_id: int = Field(foreign_key='user.id', primary_key=True, description='Relationship from')
    to_id: int = Field(foreign_key='user.id', primary_key=True, description='Relationship to')
    status: Status | None = None

    # Define the Many-to-Many relationship
    by: "User" = Relationship(back_populates="relationship_by")
    to: "User" = Relationship(back_populates="relationship_to")

    @property
    def name(self) -> str:
        return 'Relationship from %s to %s' % (self.by.username, self.to.username)


class User(SQLModel, table=True):
    class Config:
        orm_mode = True

    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str
    full_name: str | None = None
    email: str | None = None
    gender: str | None = None
    picture: bytes | None = None
    cover: bytes | None = None
    bio: str | None = None
    phone: int | None = None
    address: str | None = None
    email_verified: bool | None = None

    following: List[Relationship] = Relationship(
        back_populates="by",
        sa_relationship=Field(default=None)
    )


sql_db_path = os.path.join(pathlib.Path(__file__).parent.parent, "database.db")
sql_db_link = f"sqlite:///{sql_db_path}"
engine = create_engine(sql_db_link, echo=True)


def get_db_session():
    create_db_table()
    session = Session(engine)
    return session


def create_db_table():
    SQLModel.metadata.create_all(bind=engine)

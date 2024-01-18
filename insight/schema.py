from datetime import datetime

from sqlmodel import SQLModel


class InsightCompose(SQLModel):
    note: str
    likes: int | None = None
    date: str = None
    user: int

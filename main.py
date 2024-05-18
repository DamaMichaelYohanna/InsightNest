import os
import pathlib

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session

from insight.routing import insight
from user.views import user


app = FastAPI()
app.mount('/user', user)
app.mount('/insight', insight)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

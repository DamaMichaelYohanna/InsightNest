from fastapi import FastAPI, Body, Depends, status
from sqlmodel import Session

from user.models import get_db_session
from user.models import User
from user.schemas import RegisterInSchema, RegisterOutSchema, LoginSchema, LoginReturnSchema
from user.utility import get_password_hash, authenticate

user = FastAPI()


@user.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterOutSchema)
async def register(user_object: RegisterInSchema, db_session: Session = Depends(get_db_session)):
    user_object.password = get_password_hash(user_object.password)
    new_user = User(**user_object.dict())
    db_session.add(new_user)
    db_session.commit()
    return  new_user


@user.post("/login", response_model=LoginReturnSchema)
async def login(credentials:LoginSchema):
    username = credentials.username
    password = credentials.password
    auth_user = authenticate(username, password)
    return auth_user


@user.get("/logout")
async def logout():
    pass


@user.get("/profile/{user_id}")
async def profile(user_id: int):
    pass

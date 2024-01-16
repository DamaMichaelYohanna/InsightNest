from typing import Annotated

from fastapi import FastAPI, Body, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select

from user.models import get_session
from user.models import User
from user.schemas import RegisterInSchema, RegisterOutSchema, LoginSchema, LoginReturnSchema
from user.utility import get_password_hash, authenticate, verify_password, create_access_token, create_refresh_token

user = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@user.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterOutSchema)
async def register(user_object: RegisterInSchema, db_session: Session = Depends(get_session)):
    user_object.password = get_password_hash(user_object.password)
    new_user = User(**user_object.dict())
    db_session.add(new_user)
    db_session.commit()
    return new_user


@user.post('/login',
           summary="Create access and refresh tokens for user",
           )
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session=Depends(get_session)
):
    user_obj = session.get(select(User).where(User.username==form_data.username))
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    hashed_pass = user_obj['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    return {
        "access_token": create_access_token(user_obj['username']),
        "refresh_token": create_refresh_token(user_obj['email']),
    }


@user.get("/logout")
async def logout():
    pass


@user.get("/profile/{user_id}")
async def profile(user_id: int):
    pass


@user.post("/{user_id}/follow")
async def follow(user_id: int,
                 token: Annotated[str, Depends(oauth2_scheme)],
                 session=Depends(get_session),
                 ):
    user_2_follow = session.get(User, user_id)
    return token

@user.post("/{user_id}/unfollow")
async def unfollow(user_id: int):
    pass

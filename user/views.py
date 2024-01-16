from typing import Annotated

from fastapi import FastAPI, Body, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select

from user.deps import get_current_user
from user.models import get_session, User
from user.schemas import RegisterInSchema, RegisterOutSchema, Profile, Associate
from user.utility import get_password_hash, verify_password, create_access_token, create_refresh_token

user = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


@user.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterOutSchema)
async def register(user_object: RegisterInSchema, db_session: Session = Depends(get_session)):
    user_object.password = get_password_hash(user_object.password)
    new_user = User(**user_object.dict())
    db_session.add(new_user)
    db_session.commit()
    return new_user


@user.post('/login', summary="Create access and refresh tokens for user", )
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session=Depends(get_session)
):
    user_obj = session.exec(select(User).where(User.username == form_data.username)).one()
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    hashed_pass = user_obj.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    return {
        "access_token": create_access_token(user_obj.username),
        "refresh_token": create_refresh_token(user_obj.username),
    }


# @user.get("/profile/{user_id}")
# async def profile(user_id: int,
#                   current_user: User = Depends(get_current_user),
#                   session: Session = Depends(get_session),):
#     follower = current_user.get_followers(session=session)
#     following = current_user.get_following(session=session)
#     associate = Associate(following=len(following), follower=len(follower))
#     Profile.user = current_user
#     Profile.associate = associate
#     # if user_from_id == current_user:
#     #     Profile.owner = True
#
#     return Profile


@user.get("/profile/{user_id}", response_model=Profile)
async def my_profile(user_id:int, current_user: User = Depends(get_current_user),
                     session: Session = Depends(get_session),):
    user_from_id = session.get(User, user_id)
    follower = user_from_id.get_followers(session=session)
    following = user_from_id.get_following(session=session)
    associate = Associate(following=len(following), followers=len(follower))
    print(associate, follower, following)
    Profile.user = user_from_id
    Profile.associate = associate
    if user_from_id.id == current_user.id:
        Profile.owner = True
    else:
        Profile.owner = False

    return Profile


@user.post("/{user_id}/follow")
async def follow(
        user_id: int,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)):
    """function for user to follow another user """
    user_2_follow = session.get(User, user_id)
    current_user.follow_user(session, user_2_follow)
    return {"message": f"You are currently follow {user_2_follow.username}"}


@user.delete("/{user_id}/unfollow")
async def unfollow(user_id: int,
                   session: Session = Depends(get_session),
                   current_user: User = Depends(get_current_user)
                   ):
    """function for user to follow another user """
    user_2_unfollow = session.get(User, user_id)
    current_user.unfollow_user(session, user_2_unfollow)
    return {"message": f"You Have unfollow {user_2_unfollow.username}"}


@user.post("/{user_id}/block")
async def block(
        user_id: int,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)):
    """function for user to follow another user """
    user_2_block = session.get(User, user_id)
    current_user.block_user(session, user_2_block)
    return {"message": f"You've blocked {user_2_block.username}"}


@user.delete("/{user_id}/unblock")
async def unblock(user_id: int,
                  session: Session = Depends(get_session),
                  current_user: User = Depends(get_current_user)
                  ):
    """function for user to follow another user """
    user_2_unblock = session.get(User, user_id)
    current_user.unblock_user(session, user_2_unblock)
    response = {"status": "success",
                "message": f"You Have unblock {user_2_unblock.username}"}
    return response

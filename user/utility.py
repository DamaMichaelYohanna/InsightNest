from fastapi import HTTPException
from sqlmodel import select
from passlib.context import CryptContext

from user.models import get_db_session, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate(username, password):
    session = get_db_session()
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    print(user)
    if user:
        if verify_password(password, user.password):
            return user
        else:
            raise HTTPException(status_code=401, detail="Authentication failed")
    else:

        raise HTTPException(status_code=401, detail="Authentication failed")

# authenticate(username="Dama l", password="password123")
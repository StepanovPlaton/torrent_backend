from typing import Annotated, Any
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from jose import JWTError, jwt

import database as db
from env import Env

SECRET_KEY = Env.get_strict("JWT_SECRET_KEY", str)
ACCESS_TOKEN_EXPIRE_MINUTES = \
    Env.get_strict("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", int)


crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    email: str


def check_password(password, hash): return crypt.verify(password, hash)
def get_hash(password): return crypt.hash(password)


async def get_user(token: str = Depends(oauth2_scheme),
                   db_session: AsyncSession = Depends(db.get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY)
        token_data = TokenData(**payload)
    except Exception:
        raise credentials_exception
    user = await db.get_user(db_session, token_data.username)
    if user is None:
        raise credentials_exception
    return user


def create_token(user: db.User):
    access_token_expires = \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + access_token_expires
    to_encode = {
        "username": user.name,
        "email": user.email,
        "expire": str(expire)
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)
    return Token(access_token=encoded_jwt, token_type="bearer")


@auth_router.post("/registration")
async def registration_user(
    user_data: db.UserCreate,
    db_session: AsyncSession = Depends(db.get_session)
) -> Token:
    if (not await db.check_email(db_session, user_data.email)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This email is occupied by another user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif (await db.get_user(db_session, user_data.name) is not None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with the same name already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        user = await db.add_user(db_session, user_data,
                                 get_hash(user_data.password))
        return create_token(user)


@auth_router.post("")
async def login_user(
    auth_data: OAuth2PasswordRequestForm = Depends(),
    db_session: AsyncSession = Depends(db.get_session)
) -> Token:
    user = await db.get_user(db_session, auth_data.username)
    if (user is None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if (not check_password(auth_data.password, user.hash_of_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_token(user)


@auth_router.get("/me", response_model=db.User)
async def read_me(user: db.User = Depends(get_user)):
    return user

from typing import Optional
from fastapi import Body
from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    email: str = Field(examples=["email@gmail.com"])
    name: str = Field(examples=["username"])


class UserCreate(UserBase):
    password: str = Field(examples=["password"])


class UserOpenData(UserBase):
    id: int = Field(examples=[1])


class User(UserOpenData):
    hash_of_password: str = Field(examples=["hash_of_password"])

    model_config = ConfigDict(from_attributes=True)

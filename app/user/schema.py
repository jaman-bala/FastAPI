from datetime import date
from pydantic import BaseModel, EmailStr
from fastapi import Form
from enum import Enum


class UserSchema(BaseModel):
    email: EmailStr
    username: str
    password: str

    class Config:
        orm_mode =True


class Roles(Enum):
    user = "user"
    admin = "admin"
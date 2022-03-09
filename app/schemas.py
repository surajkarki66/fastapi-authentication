from pydantic import BaseModel, Field, EmailStr, validator, SecretStr
from datetime import datetime
from enum import Enum


class UserCreateSchema(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=32)
    last_name: str = Field(..., min_length=2, max_length=32)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)


class UserUpdateSchema(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=32)
    last_name: str = Field(..., min_length=2, max_length=32)


class PasswordUpdateSchema(BaseModel):
    old_password: str = Field(..., min_length=6)
    password: str = Field(..., min_length=6)


class Role(str, Enum):
    subscriber = "subscriber"
    admin = "admin"


class UserSchema(BaseModel):
    id: int = Field(...)
    first_name: str = Field(..., min_length=2, max_length=32)
    last_name: str = Field(..., min_length=2, max_length=32)
    email: EmailStr = Field(...)
    password: SecretStr = Field(...)
    role: Role = Field(...)
    isActive: bool = Field(...)
    created_at: datetime = Field(...)

    @validator("id")
    def validate_id(cls, v):
        if v < 0:
            raise ValueError("id must be zero and greater than zero")
        return v

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)


class TokenSchema(BaseModel):
    access_token: str = Field(...)


class PostBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=256)
    content: str = Field(..., min_length=5, max_length=1000)

    class Config:
        orm_mode = True


class PostCreateSchema(PostBase):
    pass


class PostSchema(PostBase):
    id: int = Field(...)
    user_id: int = Field(...)

    created_at: datetime = Field(...)

    @validator("user_id")
    def validate_user_id(cls, v):
        if v < 0:
            raise ValueError("user_id must be zero and greater than zero")
        return v

    @validator("id")
    def validate_id(cls, v):
        if v < 0:
            raise ValueError("id must be zero and greater than zero")
        return v

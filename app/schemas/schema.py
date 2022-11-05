from datetime import datetime
from typing import Optional, Generic, TypeVar

from pydantic import BaseModel, Field, UUID4, validator
from pydantic.generics import GenericModel

T = TypeVar('T')


class UserSchema(BaseModel):
    id: Optional[int] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    id: Optional[int] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        orm_mode = True


class UserId(BaseModel):
    id: Optional[int] = None

    class Config:
        orm_mode = True

class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)


class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)

class RequestUserId(BaseModel):
    parameter: UserId = Field(...)

class RequestUpdateUser(BaseModel):
    parameter: UpdateUser = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]

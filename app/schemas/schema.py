from datetime import datetime
from typing import Optional, Generic, TypeVar

from pydantic import BaseModel, Field, UUID4, validator
from pydantic.generics import GenericModel

T = TypeVar('T')


# class TokenBase(BaseModel):
#     token: UUID4 = Field(..., alias="access_token")
#     expires: datetime
#     token_type: Optional[str] = "bearer"
#
#     class Config:
#         allow_population_by_field_name = True
#
#     @validator("token")
#     def hexlify_token(cls, value):
#         return value.hex
#

class UserSchema(BaseModel):
    id: Optional[int] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True


# class User(UserSchema):
#     token: TokenBase = {}


class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)


class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]

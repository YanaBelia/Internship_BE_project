from typing import List

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str

class User_Register(UserBase):
    password: str
    first_name: str
    last_name: str

class User_Sign_in(UserBase):
    first_name: str

class User_Update(UserBase):
    password: str

class User(UserBase):
    id: int
    user_id: int
    is_active: bool
    class Config:
        orm_mode = True

class User_List(UserBase):
    id: int
    is_active: bool
    users: List[User] = []

    class Config:
        orm_mode = True
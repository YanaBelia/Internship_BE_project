from typing import List

import passlib.hash as _hash
from sqlalchemy import select

from app.models.models import User
from app.schemas import schema as schema


class UserCrud:

    def __init__(self, db):
        self.db = db

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        user = await self.db.execute(select(User).offset(skip).limit(limit))
        return user.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.db.execute(select(User).filter(User.id == user_id))
        return user.scalars().first()


    async def create_user(self, user: schema.UserSchema) -> User:
        _user = User(password=_hash.bcrypt.hash(user.password), first_name=user.first_name, last_name=user.last_name,
                     email=user.email)
        self.db.add(_user)
        await self.db.commit()
        await self.db.refresh(_user)
        return _user

    async def remove_user(self, user_id: int):
        _user = await self.get_user_by_id(user_id=user_id)
        await self.db.delete(_user)
        await self.db.commit()


    async def update_user(self, user_id: int, password: str, first_name: str, last_name: str) -> User:
        _user = await self.get_user_by_id(user_id=user_id)
        _user.password = password
        _user.first_name = first_name
        _user.last_name = last_name
        await self.db.commit()
        await self.db.refresh(_user)
        return _user

    async def create_user_by_email(self, email:str, password:str, first_name:str, last_name:str) -> User:
        _user = User(email=email, password=_hash.bcrypt.hash(password),
                     first_name=first_name, last_name=last_name)
        self.db.add(_user)
        await self.db.commit()
        await self.db.refresh(_user)
        return _user

import passlib.hash as _hash
from app.models.models import User
from app.schemas import schema as schema
from sqlalchemy.orm import Session, query


# def get_db(request: Request) -> Database:
#     return request.app.state.database
#


async def get_user(db: Session, skip: int = 0, limit: int = 100) -> query:
    return db.query(User).offset(skip).limit(limit).all()


async def get_user_by_id(db: Session, user_id: int) -> query:
    return db.query(User).filter(User.id == user_id).first()


async def create_user(db: Session, user: schema.UserSchema) -> User:
    _user = User(password=_hash.bcrypt.hash(user.password), first_name=user.first_name, last_name=user.last_name, email=user.email)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


async def remove_user(db: Session, user_id: int):
    _user = await get_user_by_id(db=db, user_id=user_id)
    db.delete(_user)
    db.commit()


async def update_user(db: Session, user_id: int, password: str, first_name: str, last_name: str) -> User:
    _user = await get_user_by_id(db=db, user_id=user_id)
    _user.password = password
    _user.first_name = first_name
    _user.last_name = last_name
    #_user.email = email
    db.commit()
    db.refresh(_user)
    return _user

# class Crud:
#     def __init__(self, db):
#         self.db = db
#
#     async def get_user(self, skip: int = 0, limit: int = 100) -> query:
#         return self.db.query(User).offset(skip).limit(limit).all()
#
#     async def get_user_by_id(self, user_id: int) -> query:
#         return self.db.query(User).filter(User.id == user_id).first()
#
#     async def create_user(self, user: schema.UserSchema) -> User:
#         _user = User(password=user.password, first_name=user.first_name, last_name=user.last_name, email=user.email)
#         self.db.add(_user)
#         self.db.commit()
#         self.db.refresh(_user)
#         return _user
#
#     async def remove_user(self, user_id: int):
#         _user = await self.get_user_by_id(user_id=user_id)
#         self.db.delete(_user)
#         self.db.commit()
#
#     async def update_user(self, user_id: int, password: str, first_name: str, last_name: str,
#                           email: str) -> User:
#         _user = await self.get_user_by_id(user_id=user_id)
#         _user.password = password
#         _user.first_name = first_name
#         _user.last_name = last_name
#         _user.email = email
#         self.db.commit()
#         self.db.refresh(_user)
#         return _user
#
#
# if __name__ == '__main__':
#     obj = Crud(get_db)

from app.models.models import User
from app.schemas import schema as schema
from sqlalchemy.orm import Session, query
import jwt
import fastapi
import fastapi.security as security
from fastapi import Depends, HTTPException
from app.my_data.database import get_db

from app.schemas.schema import UserSchema

# put it in .env
JWT_SECRET = "myjwtsecret"
oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/auth/signin")



async def get_user_by_email(db: Session, email: str) -> query:
    return db.query(User).filter(User.email == email).first()


async def sign_in(db: Session, email: str, password: str):
    _user = await get_user_by_email(db=db, email=email)
    if not _user:
        return False
    if not _user.verify_password(password):
        return False

    return _user


async def create_token(user: User):
    obj = schema.UserSchema.from_orm(user)
    token = jwt.encode(obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type="bearer")


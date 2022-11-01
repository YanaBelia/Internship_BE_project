from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import User
from app.schemas import schema as schema
import jwt
import fastapi.security as security
from fastapi import Depends, HTTPException
from app.my_data.database import get_db
from fastapi.security import HTTPBearer

token_auth_scheme = HTTPBearer()


JWT_SECRET = "myjwtsecret"
JWT_ALGORITHM = "RS256"


oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/auth/signin")


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    user = await db.execute(select(User).filter(User.email == email))
    return user.scalars().first()


async def sign_in(db: AsyncSession, email: str, password: str) -> User:
    _user = await get_user_by_email(db=db, email=email)
    if not _user:
        raise HTTPException(status_code=404, detail="User email is not found")
    if not _user.verify_password(password):
        raise HTTPException(status_code=404, detail="User password is not found")
    return _user


async def create_token(user: User) -> dict:
    obj = schema.UserSchema.from_orm(user)
    token = jwt.encode(obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type="bearer")


async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(token_auth_scheme)) -> User:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], verify_signature=False)
    user = await db.execute(select(User).get(payload["id"]))
    return user



from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app import crud
from app.models.models import User
from app.schemas import schema as schema
import jwt
import fastapi.security as security
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from app.token.config import JWT_SECRET, JWT_ALGORITHM
from app.token.utils import VerifyToken
from app.token.config import password, first_name, last_name




class AuthService:
    token_auth_scheme = HTTPBearer()

    oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/auth/signin")

    def __init__(self, db):
        self.db = db

    async def get_user_by_email(self, email: str) -> User:
        user = await self.db.execute(select(User).filter(User.email == email))
        return user.scalars().first()

    async def sign_in(self, email: str, password: str) -> User:
        _user = await self.get_user_by_email(email=email)
        if not _user:
            raise HTTPException(status_code=404, detail="User email is not found")
        if not _user.verify_password(password):
            raise HTTPException(status_code=404, detail="User password is not found")
        return _user

    async def create_token(email: str) -> dict:
        obj = schema.UserSchema.from_orm(email)
        token = jwt.encode(obj.dict(), JWT_SECRET)
        return dict(access_token=token, token_type="bearer")

    async def get_current_user_email(token: str):
        credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Invalid data")
        try:
            payload = VerifyToken(token.credentials).verify_my()
            user_email: str = payload.get("email")
            if user_email is None:
                raise credential_exception
        except JWTError:
            raise credential_exception
        return user_email

    async def get_current_auth_email(self, token: str):
        credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Invalid data")
        auth0_email = "https://example.com/email"

        try:
            pyload = VerifyToken(token.credentials).verify_auth0()
            if pyload is None:
                raise credential_exception
        except JWTError:
            raise credential_exception
        user = await self.get_user_by_email(email=pyload.get(auth0_email))
        if user is None:
            await crud.UserCrud(self.db).create_user_by_email(email=pyload.get(auth0_email), password=password,
                                                              first_name=first_name, last_name=last_name)

        return pyload.get(auth0_email)




import jwt
from fastapi import Depends, HTTPException, APIRouter, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth import services
from app.my_data.database import get_db
from fastapi.security import HTTPBearer
from app.token.config import ALGORITHMS, JWT_ALGORITHM

token_auth_scheme = HTTPBearer()
router1 = APIRouter()


@router1.post("/signin")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(),
                         db: AsyncSession = Depends(get_db)) -> dict:
    user = await services.AuthService(db).sign_in(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=404, detail="Invalid data")
    return await services.AuthService.create_token(user)


@router1.get("/get_email_by_token")
async def get_user_or_auth(db: AsyncSession = Depends(get_db),
                           token: str = Depends(token_auth_scheme),
                           ):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="token is not correct")
    if jwt.get_unverified_header(token.credentials)['alg'] == ALGORITHMS:
        return await services.AuthService(db).get_current_auth_email(token=token)
    elif jwt.get_unverified_header(token.credentials)['alg'] == JWT_ALGORITHM:
        return await services.AuthService.get_current_user_email(token=token)
    else:
        return credential_exception

from fastapi import Depends, HTTPException, APIRouter, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.auth.services import sign_in, create_token, get_current_user
from app import crud
from app.my_data.database import get_db
from app.schemas.schema import UserSchema, RequestUser
from fastapi.security import HTTPBearer
from app.models.models import User
from app.token.utils import VerifyToken

token_auth_scheme = HTTPBearer()
router1 = APIRouter()


@router1.post("/signin")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(),
                         db: AsyncSession = Depends(get_db)) -> dict:
    user = await sign_in(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=404, detail="Invalid data")
    return await create_token(user)


@router1.get("/me")  # don't work
async def private(response: Response,
                  token: str = Depends(token_auth_scheme),
                  db: AsyncSession = Depends(get_db)) -> User:
    result = VerifyToken(token.credentials).verify()

    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result

    user_id = result.get("id")
    user = await crud.UserCrud(db).get_user_by_id(user_id=user_id)
    return user

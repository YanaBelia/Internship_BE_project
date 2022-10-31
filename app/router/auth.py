from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth.services import sign_in, create_token
from app import crud
from app.my_data.database import get_db
from app.schemas.schema import UserSchema, RequestUser
from fastapi.security import HTTPBearer



token_auth_scheme = HTTPBearer()
router1 = APIRouter()



@router1.post('/signup', response_model=UserSchema)
async def create_user(request: RequestUser, db: Session = Depends(get_db)) -> UserSchema:
    _user = await crud.create_user(db, user=request.parameter)
    if not _user:
        raise HTTPException(status_code=404, detail="User with this email already exist")
    return _user


@router1.post("/signin")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(),
                         db: Session = Depends(get_db)):
    user = await sign_in(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=404, detail="Invalid data")
    return await create_token(user)




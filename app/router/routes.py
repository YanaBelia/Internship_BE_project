from typing import List
from app.exceptions.exceptions import UserInfoNotFoundError, UserInfoAlreadyExist
from databases import Database
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.models.models import User
# from fastapi.encoders import jsonable_encoder
from app.schemas.schema import RequestUser, Response, UserSchema

from app import crud
from app.my_data.database import get_db

router = APIRouter()


@router.post('/create', response_model=UserSchema)
async def create_user(request: RequestUser, data: Session = Depends(get_db)) -> UserSchema:
    created = crud.create_user(data, user=request.parameter)
    if not created:
        #raise UserInfoAlreadyExist
        raise HTTPException(status_code=404, detail="User is not created")
    return await crud.create_user(data, user=request.parameter)


@router.get("/", response_model=List[UserSchema])
async def get_users(skip: int = 0, limit: int = 100, data: Session = Depends(get_db)) -> User:
    _user = crud.get_user(data, skip, limit)
    if not _user:
        raise UserInfoNotFoundError
        # raise HTTPException(status_code=404, detail="Users are not found")
    return await _user


@router.get("/{id}", response_model=UserSchema)
async def get_by_id(id: int, data: Session = Depends(get_db)) -> UserSchema:
    _user = crud.get_user_by_id(data, id)
    if not _user:
        #raise UserInfoNotFoundError
        raise HTTPException(status_code=404, detail="User id not found")
    return await _user


@router.patch("/update", response_model=UserSchema)
async def update_user(request: RequestUser, data: Session = Depends(get_db)) -> UserSchema:
    _user = crud.update_user(data, user_id=request.parameter.id,
                             password=request.parameter.password,
                             first_name=request.parameter.first_name,
                             last_name=request.parameter.last_name,
                             )
    if _user is None:
        raise UserInfoNotFoundError
    return await _user


@router.delete("/{id}", response_model=UserSchema)
async def delete_user(id: int, data: Session = Depends(get_db)):
    await crud.remove_user(data, user_id=id)
    return Response(code="200", status="ok", message="User deleted successfully").dict(exclude_none=True)

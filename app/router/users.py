from typing import List
from databases import Database
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import User
from app.schemas.schema import RequestUser, Response, UserSchema, RequestUpdateUser

from app import crud
from app.my_data.database import get_db

router = APIRouter()


@router.post('/create', response_model=UserSchema, status_code=201)
async def create_user(request: RequestUser,
                      data: AsyncSession = Depends(get_db)) -> User:
    _user = await crud.UserCrud(data).create_user(user=request.parameter)
    if not _user:
        raise HTTPException(status_code=404, detail="User is not created")
    return _user


@router.get("/", response_model=List[UserSchema], status_code=201)
async def get_users(skip: int = 0, limit: int = 100,
                    data: AsyncSession = Depends(get_db)) -> List[User]:
    _user = await crud.UserCrud(data).get_users(skip, limit)
    if not _user:
        raise HTTPException(status_code=404, detail="Users are not found")
    return _user


@router.get("/{id}", response_model=UserSchema, status_code=201)
async def get_by_id(id: int, data: AsyncSession = Depends(get_db)) -> User:
    _user = await crud.UserCrud(data).get_user_by_id(id)
    if not _user:
        raise HTTPException(status_code=404, detail="User id not found")
    return _user


@router.patch("/update", response_model=UserSchema, status_code=201)
async def update_user(request: RequestUpdateUser,
                      data: AsyncSession = Depends(get_db)) -> User:
    _user = await crud.UserCrud(data).update_user(user_id=request.parameter.id,
                                                  password=request.parameter.password,
                                                  first_name=request.parameter.first_name,
                                                  last_name=request.parameter.last_name,
                                                  )
    if _user is None:
        raise HTTPException(status_code=404, detail="User is not updated")
    return _user


@router.delete("/{id}", response_model=UserSchema, status_code=201)
async def delete_user(id: int, data: AsyncSession = Depends(get_db)):
    try:
        await crud.UserCrud(data).remove_user(user_id=id)
    except:
        raise HTTPException(status_code=404, detail="User id not found")
    return Response(code="200", status="ok", message="User deleted successfully").dict(exclude_none=True)


@router.get("/{id}", response_model=UserSchema, status_code=201)
async def get_by_id(id: int, data: AsyncSession = Depends(get_db)) -> User:
    _user = await crud.UserCrud(data).get_user_by_id(id)
    if not _user:
        raise HTTPException(status_code=404, detail="User id not found")
    return _user

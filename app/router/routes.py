from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
# from fastapi.encoders import jsonable_encoder
from app.schemas.schema import RequestUser, Response
from app import crud
from app.my_data.database import get_db

router = APIRouter()


@router.post('/create')
async def create_user(request: RequestUser, data: Session = Depends(get_db)):
    crud.create_user(data, user=request.parameter)
    return Response(code="200", status="ok",
                    message="User created successfully").dict(exclude_none=True)


@router.get("/")
async def get_users(skip: int = 0, limit: int = 100, data: Session = Depends(get_db)):
    _user = crud.get_user(data, skip, limit)
    return Response(code="200", status="ok",
                    message="Successfully Fetch data", result=_user)


@router.get("/{id}")
async def get_by_id(id: int, data: Session = Depends(get_db)):
    _user = crud.get_user_by_id(data, id)
    return Response(code="200", status="ok", message="Get user by id", result=_user).dict(exclude_none=True)


@router.patch("/update")
async def update_user(request: RequestUser, data: Session = Depends(get_db)):
    _user = crud.update_user(data, user_id=request.parameter.id,
                             password=request.parameter.password,
                             first_name=request.parameter.first_name,
                             last_name=request.parameter.last_name,
                             email=request.parameter.email)
    return Response(code="200", status="ok", message="User updated", result=_user)


@router.delete("/delete")
async def delete_user(request: RequestUser, data: Session = Depends(get_db)):
    crud.remove_user(data, user_id=request.parameter.id)
    return Response(code="200", status="ok", message="User deleted successfully").dict(exclude_none=True)

from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas import schema as schema


def get_user(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: schema.UserRegister):
    _user = User(password=user.password, first_name=user.first_name, last_name=user.last_name, email=user.email)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def remove_user(db: Session, user_id: int):
    _user = get_user_by_id(db=db, user_id=user_id)
    db.delete(_user)
    db.commit()


def update_user(db: Session, user_id: int, password: str, first_name: str, last_name: str, email: str):
    _user = get_user_by_id(db=db, user_id=user_id)
    _user.password = password
    _user.first_name = first_name
    _user.last_name = last_name
    _user.email = email
    db.commit()
    db.refresh(_user)
    return _user

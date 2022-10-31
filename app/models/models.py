from sqlalchemy import Column, String, Integer, DateTime, Boolean
from app.my_data.database import Base
from sqlalchemy.ext.declarative import declarative_base
import passlib.hash as _hash


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    date = Column(DateTime)
    is_active = Column(Boolean, default=False)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.password)

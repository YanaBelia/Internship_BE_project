# from typing import Optional, MutableMapping, List, Union
# from datetime import datetime, timedelta
#
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm.session import Session
# from jose import jwt
#
# from app.auth.security import verify_password
# from app.models.models import User
# from app.config import settings
#
#
#
# JWTPayloadMapping = MutableMapping[
#     str, Union[datetime, bool, str, List[str], List[int]]
# ]
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/auth/login")
#
#
# def authenticate(
#     *,
#     email: str,
#     password: str,
#     db: Session,
# ) -> Optional[User]:
#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         return None
#     if not verify_password(password, user.hashed_password):  # 1
#         return None
#     return user
#
#
# def create_access_token(*, sub: str) -> str:  # 2
#     return _create_token(
#         token_type="access_token",
#         lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),  # 3
#         sub=sub,
#     )
#
#
# def _create_token(
#     token_type: str,
#     lifetime: timedelta,
#     sub: str,
# ) -> str:
#     payload = {}
#     expire = datetime.utcnow() + lifetime
#     payload["type"] = token_type
#     payload["exp"] = expire  # 4
#     payload["iat"] = datetime.utcnow()  # 5
#     payload["sub"] = str(sub)  # 6
#
#     return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
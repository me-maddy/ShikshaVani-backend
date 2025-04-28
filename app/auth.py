from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer
from app.models.user import UserDb

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def hash_password(plain_password: str):
    return pass_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str):
    return pass_context.verify(plain_password, hashed_password)


def get_current_user(
    token: str = Depends(oauth_scheme), db: Session = Depends(get_db)
) -> UserDb:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db_user = db.query(UserDb).filter(UserDb.email == email).first()
    if db_user is None:
        raise credentials_exception
    return db_user


def is_faculty(current_user=Depends(get_current_user)):
    if current_user.role != "faculty":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Faculty access only"
        )
    return current_user


def is_student(current_user=Depends(get_current_user)):
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="student access only"
        )
    return current_user

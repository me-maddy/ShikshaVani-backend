from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserLogin
from app.crud.user import login_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    return await login_user(db, email=user.email, password=user.password)

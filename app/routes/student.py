from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserProfileDetails
from app.auth import get_db, is_student
from sqlalchemy.orm import Session
from app.crud.user import create_user, update_student_profile
from app.models import UserDb

router = APIRouter(prefix="/student", tags=["Student"])


@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return await create_user(db, user, role="student")


@router.post("/profile_details")
async def upload_profile_details(
    user_profile: UserProfileDetails,
    db: Session = Depends(get_db),
    current_user: UserDb = Depends(is_student),
):
    return await update_student_profile(
        db, user_profile=user_profile, user_id=current_user.id
    )

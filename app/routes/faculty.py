from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate
from app.auth import get_db, is_faculty
from sqlalchemy.orm import Session
from app.crud.user import create_user
from app.crud.faculty_subject import (
    create_faculty,
    get_all_faculties,
    get_faculty_summary,
    get_faculty_students,
)
from app.schemas.faculty_subject import FacultyCreate
from app.models import UserDb

router = APIRouter(prefix="/faculty", tags=["Faculty"])


@router.get("/")
def list_all_faculties(db: Session = Depends(get_db)):
    return get_all_faculties(db)


@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return await create_user(db, user, role="faculty")


@router.post("/faculty_profile")
async def update_faculty_details(
    faculty: FacultyCreate,
    db: Session = Depends(get_db),
    current_user: UserDb = Depends(is_faculty),
):
    return await create_faculty(db, faculty, user_id=current_user.id)


@router.get("/summary")
async def get_summary(
    db: Session = Depends(get_db), current_user: UserDb = Depends(is_faculty)
):
    return await get_faculty_summary(db, user_id=current_user.id)


@router.get("/students")
async def get_all_faculty_students(
    db: Session = Depends(get_db), current_user: UserDb = Depends(is_faculty)
):
    return await get_faculty_students(db, user_id=current_user.id)

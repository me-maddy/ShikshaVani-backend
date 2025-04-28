from fastapi import APIRouter, Depends
from app.schemas.class_schema import ClassCreate
from sqlalchemy.orm import Session
from app.auth import get_db, is_faculty
from app.models.user import UserDb
from app.crud.classes import (
    add_class,
    get_all_classes_by_faculty_id,
    get_faculty_all_classes,
)

router = APIRouter(prefix="/faculty/class", tags=["Faculty Class"])


@router.get("/")
async def get_all_classes(
    db: Session = Depends(get_db), current_user: UserDb = Depends(is_faculty)
):
    return await get_faculty_all_classes(db, user_id=current_user.id)


@router.get("/{faculty_id}")
async def get_all_classes(faculty_id: int, db: Session = Depends(get_db)):
    return await get_all_classes_by_faculty_id(db, faculty_id)


@router.post("/add")
async def create_class(
    data: ClassCreate,
    db: Session = Depends(get_db),
    current_user: UserDb = Depends(is_faculty),
):
    return await add_class(db=db, name=data.name, user_id=current_user.id)

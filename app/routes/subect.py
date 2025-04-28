from fastapi import APIRouter, Depends
from app.schemas.faculty_subject import SubjectCreate
from app.database import get_db
from sqlalchemy.orm import Session
from app.crud.faculty_subject import (
    create_subject,
    get_all_subjects,
)
from app.models.user import UserDb
from app.auth import is_faculty

router = APIRouter(prefix="/subjects", tags=["Subject"])


@router.post("/add")
async def add_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: UserDb = Depends(is_faculty),
):
    return await create_subject(
        db, name=subject.name, class_id=subject.class_id, user_id=current_user.id
    )


@router.get("/{class_id}")
def list_subjects(class_id:str,db: Session = Depends(get_db)):
    return get_all_subjects(db,class_id)

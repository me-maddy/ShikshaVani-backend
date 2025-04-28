from sqlalchemy.orm import Session
from app.schemas.faculty_subject import FacultyCreate
from app.models import FacultyProfileDb, SubjectDb
from app.models.class_model import ClassDb
from fastapi import HTTPException
from app.crud.classes import get_faculty_by_user_id
from sqlalchemy import update
from app.models import UserDb


async def get_faculty_by_user_id(db: Session, user_id: int):
    return (
        db.query(FacultyProfileDb).filter(FacultyProfileDb.user_id == user_id).first()
    )


async def create_faculty(db: Session, faculty: FacultyCreate, user_id: int):
    user_faculty = db.query(FacultyProfileDb).filter_by(user_id=user_id).first()
    if user_faculty:
        raise HTTPException(status_code=400, detail="Faculty already exist")

    new_faculty = FacultyProfileDb(
        name=faculty.name, email=faculty.email, user_id=user_id
    )

    db.add(new_faculty)

    query = (
        update(UserDb)
        .where(UserDb.id == user_id)
        .values(is_registered=True)
        .execution_options(synchronize_session="fetch")
    )

    db.execute(query)

    db.commit()
    db.refresh(new_faculty)

    return new_faculty


async def create_subject(db: Session, name: str, class_id: int, user_id: int):
    faculty = await get_faculty_by_user_id(db, user_id)
    if faculty is None:
        raise ValueError("Faculty not exist")

    faculty_class = (
        db.query(ClassDb).filter_by(id = class_id, faculty_id=faculty.id).first()
    )
    if not faculty_class:
        raise HTTPException(status_code=404, detail="Class not found or unauthorized")

    new_subject = SubjectDb(name=name, class_id=class_id)
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return {"msg": "Subject added", "subject": new_subject}


def get_all_faculties(db: Session):
    return db.query(FacultyProfileDb).all()


def get_all_subjects(db: Session,class_id:str):
    return db.query(SubjectDb).filter(SubjectDb.class_id == class_id).all()

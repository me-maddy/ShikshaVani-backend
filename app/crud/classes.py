from sqlalchemy.orm import Session
from app.models import ClassDb, FacultyProfileDb


async def get_faculty_all_classes(db: Session, user_id: int):
    faculty = await get_faculty_by_user_id(db, user_id)
    if faculty is None:
        raise ValueError("Faculty not exist")
    all_classes = db.query(ClassDb).filter(ClassDb.faculty_id == faculty.id).all()
    return all_classes


async def get_faculty_by_user_id(db: Session, user_id: int):
    return (
        db.query(FacultyProfileDb).filter(FacultyProfileDb.user_id == user_id).first()
    )


async def get_all_classes_by_faculty_id(db: Session, faculty_id: int):
    return db.query(ClassDb).filter(ClassDb.faculty_id == faculty_id).all()


async def add_class(db: Session, name: str, user_id: int):
    faculty = await get_faculty_by_user_id(db, user_id)
    if faculty is None:
        raise ValueError("Faculty not exist")
    new_class = ClassDb(name=name, faculty_id=faculty.id)
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return {"class": new_class}

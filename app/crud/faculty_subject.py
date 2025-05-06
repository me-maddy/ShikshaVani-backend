from sqlalchemy.orm import Session, joinedload
from app.schemas.faculty_subject import FacultyCreate
from app.models import FacultyProfileDb, SubjectDb, ClassDb, StudentProfileDb
from fastapi import HTTPException
from app.crud.classes import get_faculty_by_user_id
from sqlalchemy import update, select
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
        db.query(ClassDb).filter_by(id=class_id, faculty_id=faculty.id).first()
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


def get_all_subjects(db: Session, class_id: str):
    return db.query(SubjectDb).filter(SubjectDb.class_id == class_id).all()


async def get_faculty_summary(db: Session, user_id: int):
    result = db.execute(
        select(FacultyProfileDb).where(FacultyProfileDb.user_id == user_id)
    )
    faculty = result.scalar_one_or_none()

    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    result = db.execute(
        select(ClassDb)
        .options(joinedload(ClassDb.subjects).joinedload(SubjectDb.feedbacks))
        .where(ClassDb.faculty_id == faculty.id)
    )

    faculty_classes = result.unique().scalars().all()

    summary = {"classes": 0, "subjects": 0, "feedbacks": 0}

    for class_obj in faculty_classes:
        summary["classes"] += 1
        for subject in class_obj.subjects:
            summary["subjects"] += 1
            summary["feedbacks"] += len(subject.feedbacks)

    return summary


async def get_faculty_students(db: Session, user_id: int):
    result = db.execute(
        select(FacultyProfileDb)
        .options(
            joinedload(FacultyProfileDb.students).joinedload(StudentProfileDb.user),
            joinedload(FacultyProfileDb.students).joinedload(
                StudentProfileDb.class_obj
            ),
        )
        .where(FacultyProfileDb.user_id == user_id)
    )
    faculty = result.unique().scalar_one_or_none()

    if not faculty or not faculty.students:
        raise HTTPException(status_code=404, detail="Students not found")

    response = []
    for student in faculty.students:
        if student.user and student.class_obj:
            response.append(
                {
                    "id": student.user.id,
                    "student_name": student.user.name,
                    "student_email": student.user.email,
                    "student_class_name": student.class_obj.name,
                }
            )

    return response

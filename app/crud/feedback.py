from app.schemas import feedback
from sqlalchemy.orm import Session,joinedload
from app.models import FeedbackDb,UserDb,FacultyProfileDb,StudentProfileDb,SubjectDb,ClassDb
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def create_feedback(db: Session, feedback: feedback.FeedbackCreate, student_id: int):
    existing_feedback = db.query(FeedbackDb).filter(FeedbackDb.student_id == student_id, FeedbackDb.subject_id == feedback.subject_id).first()

    if existing_feedback:
        raise HTTPException(status_code=400, detail="Feedback already submitted for this subject.")
    
    new_feedback = FeedbackDb(
        student_id=student_id,
        subject_id=feedback.subject_id,
        rating=feedback.rating,
        comment=feedback.comment,
    )
    db.add(new_feedback)
    
    try:
       db.commit()
       db.refresh(new_feedback)
       return new_feedback
    except IntegrityError:
        db.rollback()
        raise ValueError("Feedback already submitted for this subject.")


async def get_feedback_by_student(db: AsyncSession, student_id: int):
     result = await db.execute(
        select(FeedbackDb)
        .options(
            joinedload(FeedbackDb.subject)
            .joinedload(SubjectDb.class_)
        )
        .where(FeedbackDb.student_id == student_id)
     )
     
     feedbacks = result.scalars().all()
     
     student_feedback_data = []
     for feedback in feedbacks:
        student_feedback_data.append({
            "className": feedback.subject.class_.name,
            "subjectName": feedback.subject.name,
            "rating": feedback.rating,
            "comment": feedback.comment,
        })

     return student_feedback_data

async def get_faculty_feedbacks(db:Session, user_id:int):
     result = db.execute(
        select(FacultyProfileDb).where(FacultyProfileDb.user_id == user_id)
     )
     faculty = result.scalar_one_or_none()

     if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
     

     result = db.execute(
        select(ClassDb)
        .options(
            joinedload(ClassDb.subjects)
            .joinedload(SubjectDb.feedbacks)
            .joinedload(FeedbackDb.student)  # assuming relationship banaoge
        )
        .where(ClassDb.faculty_id == faculty.id)
    )
     
     classes = result.unique().scalars().all()

     feedback_data = []
     for class_obj in classes:
        class_dict = {
            "class": class_obj.name,
            "subjects": []
        }
        for subject in class_obj.subjects:
            if subject.feedbacks:
                subject_dict = {
                    "subjectName": subject.name,
                    "feedbacks": []
                }
                for feedback in subject.feedbacks:
                    subject_dict["feedbacks"].append({
                        "rating": feedback.rating,
                        "comment": feedback.comment,
                        "studentName": feedback.student.name,
                        "studentEmail": feedback.student.email,
                    })
                class_dict["subjects"].append(subject_dict)
        
        if class_dict["subjects"]:
            feedback_data.append(class_dict)

     return feedback_data
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.feedback import FeedbackCreate
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import UserDb
from app.auth import get_current_user,is_student,is_faculty
from app.crud.feedback import create_feedback, get_feedback_by_student,get_faculty_feedbacks

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/")
async def submit_feedback(
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: UserDb = Depends(is_student),
):
    try:
        await create_feedback(db, feedback=data, student_id=current_user.id)
        return {"message": "Feedback submitted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/faculty")
async def view_faculty_feedbacks(db:Session = Depends(get_db), current_user:UserDb = Depends(is_faculty)):
    return await get_faculty_feedbacks(db,user_id=current_user.id)


@router.get("/student")
def view_my_feedback(
    db: Session = Depends(get_db), current_user: UserDb = Depends(is_student)
):
    return get_feedback_by_student(db, student_id=current_user.id)

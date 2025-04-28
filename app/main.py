from fastapi import FastAPI
from app.models import (
    UserDb,
    StudentProfileDb,
    SubjectDb,
    FeedbackDb,
    FacultyProfileDb,
    ClassDb,
)
from app.database import engine
from app.routes import auth, feedback, class_router, subect, faculty, student
from app.database import Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(subect.router)
app.include_router(feedback.router)
app.include_router(class_router.router)
app.include_router(faculty.router)
app.include_router(student.router)


@app.get("/")
def read_root():
    return {"message": "College Feedback API Running 🚀"}

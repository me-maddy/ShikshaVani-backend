from sqlalchemy import Column, String, Integer, Boolean
from app.database import Base
from sqlalchemy.orm import relationship


class UserDb(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(String, default="student")
    is_registered = Column(Boolean, default=False)

    feedbacks = relationship("FeedbackDb", back_populates="student")
    faculty = relationship("FacultyProfileDb", back_populates="user")
    studentProfile = relationship("StudentProfileDb", back_populates="user")

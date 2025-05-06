from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class StudentProfileDb(Base):
    __tablename__ = "student_profile_table"

    id = Column(Integer, primary_key=True)
    faculty_id = Column(Integer, ForeignKey("faculty_profile_table.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    is_registered = Column(Boolean, default=False)

    class_obj = relationship("ClassDb", back_populates="students")
    faculty = relationship("FacultyProfileDb", back_populates="students")
    user = relationship("UserDb", back_populates="studentProfile")

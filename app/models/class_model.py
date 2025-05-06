from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class ClassDb(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    faculty_id = Column(Integer, ForeignKey("faculty_profile_table.id"))

    __table_args__ = (
        UniqueConstraint("name", "faculty_id", name="class_faculty_unique"),
    )

    subjects = relationship("SubjectDb", back_populates="class_obj")
    students = relationship("StudentProfileDb", back_populates="class_obj")
    faculty = relationship("FacultyProfileDb", back_populates="classes")

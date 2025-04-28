from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean


class StudentProfileDb(Base):
    __tablename__ = "student_profile_table"

    id = Column(Integer, primary_key=True)
    faculty_id = Column(Integer, ForeignKey("faculty_profile_table.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    is_registered = Column(Boolean, default=False)

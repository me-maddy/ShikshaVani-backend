from app.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint


class FacultyProfileDb(Base):
    __tablename__ = "faculty_profile_table"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    __table_args__ = (UniqueConstraint("user_id", name="unique_user_faculty_profile"),)

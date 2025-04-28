from sqlalchemy import Column, String, Integer, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class SubjectDb(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))

    class_obj = relationship("ClassDb", back_populates="subjects")
    feedbacks = relationship("FeedbackDb", back_populates="subject")

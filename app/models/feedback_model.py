from sqlalchemy import Column, ForeignKey, Integer, Text, UniqueConstraint
from app.database import Base
from sqlalchemy.orm import relationship


class FeedbackDb(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    rating = Column(Integer)
    comment = Column(Text)

    student = relationship("UserDb", back_populates="feedbacks")
    subject = relationship("SubjectDb", back_populates="feedbacks")

    __table_args__ = (
        UniqueConstraint(
            "student_id", "subject_id", name="unique_student_subject_feedback"
        ),
    )

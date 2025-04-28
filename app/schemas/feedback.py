from pydantic import BaseModel
from typing import Optional


class FeedbackCreate(BaseModel):
    subject_id: int
    rating: int
    comment: Optional["str"] = None

from pydantic import BaseModel

class SubjectWithFaculty(BaseModel):
    subject_id: int
    subject_name: str
    faculty_id: int
    faculty_name: str

    class Config:
        from_attributes = True
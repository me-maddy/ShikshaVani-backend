from pydantic import BaseModel


class FacultyCreate(BaseModel):
    name: str
    email: str


class SubjectCreate(BaseModel):
    name: str
    class_id: int

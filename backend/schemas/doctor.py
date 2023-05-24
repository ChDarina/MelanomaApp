from typing import Optional

from pydantic import BaseModel
from schemas.user import UserModel, UserCreate, UserUpdate


class DoctorModel(UserModel):
    description: Optional[str]
    work_years: int

    class Config:
        orm_mode = True


class DoctorCreate(UserCreate):
    description: Optional[str]
    work_years: int


class DoctorUpdate(UserUpdate):
    description: Optional[str]
    work_years: int


class DoctorResponseModel(BaseModel):
    id: int
    name: str
    description: str
    work_years: int


class DoctorsAnswer(BaseModel):
    question_id: int
    content: str


class DoctorsArticle(BaseModel):
    doctor_id: int
    title: str
    content: str

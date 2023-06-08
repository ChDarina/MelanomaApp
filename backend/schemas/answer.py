from datetime import datetime

from pydantic import BaseModel


class AnswerModel(BaseModel):
    id: int
    doctor_id: int
    question_id: int
    content: str
    datetime_created: datetime

    class Config:
        orm_mode = True


class AnswerCreate(BaseModel):
    doctor_id: int
    question_id: int
    content: str
    datetime_created: datetime


class AnswerUpdate(BaseModel):
    content: str


class AnswerResponse(BaseModel):
    id: int
    doctor_id: int
    doctor_name: str
    work_years: int
    question_id: int
    content: str
    datetime_created: datetime

    class Config:
        orm_mode = True

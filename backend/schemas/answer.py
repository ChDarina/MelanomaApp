from datetime import datetime

from pydantic import BaseModel


class AnswerModel(BaseModel):
    id: int
    title: str
    doctor_id: int
    question_id: int
    content: str
    datetime_created: datetime

    class Config:
        orm_mode = True


class AnswerCreate(BaseModel):
    title: str
    doctor_id: int
    question_id: int
    content: str
    datetime_created: datetime


class AnswerUpdate(BaseModel):
    title: str
    content: str


class AnswerResponse(BaseModel):
    id: int
    title: str
    doctor_id: int
    doctor_name: str
    work_years: int
    question_id: int
    content: str
    datetime_created: datetime

    class Config:
        orm_mode = True

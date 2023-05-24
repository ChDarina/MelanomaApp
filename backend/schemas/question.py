from datetime import datetime

from pydantic import BaseModel


class QuestionModel(BaseModel):
    id: int
    patient_id: int
    title: str
    content: str
    datetime_created: datetime

    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    patient_id: int
    title: str
    content: str
    datetime_created: datetime


class QuestionUpdate(BaseModel):
    title: str
    content: str


class QuestionResponse(BaseModel):
    id: int
    patient_id: int
    title: str
    content: str
    datetime_created: datetime

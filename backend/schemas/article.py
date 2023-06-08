from datetime import datetime

from pydantic import BaseModel


class ArticleModel(BaseModel):
    id: int
    doctor_id: int
    doctor_name: str
    work_years: int
    title: str
    content: str
    datetime_created: datetime

    class Config:
        orm_mode = True


class ArticleCreate(BaseModel):
    id: int
    doctor_id: int
    title: str
    content: str
    datetime_created: datetime


class ArticleUpdate(BaseModel):
    id: int
    doctor_id: int
    title: str
    content: str


class ArticleResponse(BaseModel):
    id: int
    doctor_id: int
    doctor_name: str
    work_years: int
    title: str
    content: str
    datetime_created: datetime

    class Config:
        orm_mode = True


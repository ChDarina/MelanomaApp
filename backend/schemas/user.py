from datetime import date

from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    photo_id: int
    name: str
    birthday_date: date
    residence: str
    email: str
    telephone: str
    password: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    photo_id: int = 10
    birthday_date: date
    residence: str
    email: str
    telephone: str
    password: str
    confirm_password: str


class UserUpdate(BaseModel):
    name: str
    photo_id: int
    birthday_date: date
    residence: str
    email: str
    telephone: str
    password: str

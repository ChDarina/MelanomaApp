from datetime import date

from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    photo_id: int
    full_name: str
    birthday_date: date
    residence: str
    email: str
    telephone: str
    password: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    full_name: str
    birthday_date: date
    residence: str
    email: str
    telephone: str
    password: str
    confirm_password: str


class UserUpdate(BaseModel):
    full_name: str
    birthday_date: date
    residence: str
    email: str
    telephone: str
    password: str

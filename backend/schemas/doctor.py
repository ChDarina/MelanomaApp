from typing import Optional

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

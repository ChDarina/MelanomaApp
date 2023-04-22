from typing import Optional

from schemas.user import UserModel, UserCreate, UserUpdate


class DoctorModel(UserModel):
    specialty_id: int
    education_id: int
    description: Optional[str]
    work_years: int

    class Config:
        orm_mode = True


class DoctorCreate(UserCreate):
    specialty_id: int
    education_id: int
    description: Optional[str]
    work_years: int


class DoctorUpdate(UserUpdate):
    specialty_id: int
    education_id: int
    description: Optional[str]
    work_years: int

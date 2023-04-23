from pydantic import BaseModel


class DoctorJobsModel(BaseModel):
    id: int
    doctor_id: int
    work_place_id: int

    class Config:
        orm_mode = True


class DoctorJobsCreate(BaseModel):
    doctor_id: int
    work_place_id: int


class DoctorJobsUpdate(BaseModel):
    doctor_id: int
    work_place_id: int

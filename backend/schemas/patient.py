from pydantic import BaseModel


class PatientModel(BaseModel):
    id: int
    user_id: int
    status_id: int

    class Config:
        orm_mode = True


class PatientCreate(BaseModel):
    user_id: int
    status_id: int


class PatientUpdate(BaseModel):
    status_id: int

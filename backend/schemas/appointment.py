from datetime import datetime

from pydantic import BaseModel


class AppointmentModel(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    description: str
    appointment_datetime: datetime
    doctor_approved: bool

    class Config:
        orm_mode = True


class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    description: str
    appointment_datetime: datetime
    doctor_approved: bool


class AppointmentUpdate(BaseModel):
    doctor_id: int
    patient_id: int
    description: str
    appointment_datetime: datetime
    doctor_approved: bool

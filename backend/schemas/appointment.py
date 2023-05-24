from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AppointmentModel(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    description: str
    appointment_datetime: datetime
    doctor_approved: Optional[bool]

    class Config:
        orm_mode = True


class AppointmentResponse(AppointmentModel):
    doctor_name: str
    patient_name: str


class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    description: str
    appointment_datetime: datetime
    doctor_approved: Optional[bool] = None


class AppointmentUpdate(BaseModel):
    doctor_id: int
    patient_id: int
    description: str
    appointment_datetime: datetime
    doctor_approved: Optional[bool]


class AppointmentApproval(BaseModel):
    description: Optional[str]
    doctor_approved: bool

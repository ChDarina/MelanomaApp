from typing import List

from sqlalchemy.orm import Session
from db.appointment import Appointment

from schemas.appointment import AppointmentCreate, AppointmentUpdate


def create_appointment(db: Session, appointment: AppointmentCreate) -> Appointment:
    db_appointment = Appointment(
        doctor_id=appointment.doctor_id,
        patient_id=appointment.patient_id,
        description=appointment.description,
        appointment_datetime=appointment.appointment_datetime
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def read_appointment(db: Session, appointment_id: int) -> Appointment:
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise ValueError(f"Appointment not found with id {appointment_id}")
    return db_appointment


def read_appointments(db: Session) -> List[Appointment]:
    return db.query(Appointment).all()


def update_appointment(db: Session, appointment_id: int, appointment: AppointmentUpdate) -> Appointment:
    db_appointment = read_appointment(db, appointment_id)
    for key, value in appointment.dict(exclude_unset=True).items():
        setattr(db_appointment, key, value)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def delete_appointment(db: Session, appointment_id: int) -> None:
    db_appointment = read_appointment(db, appointment_id)
    db.delete(db_appointment)
    db.commit()

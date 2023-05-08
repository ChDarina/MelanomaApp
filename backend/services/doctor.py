from passlib.handlers.bcrypt import bcrypt
from sqlalchemy.orm import Session
from db.doctor import Doctor
from schemas.doctor import DoctorCreate, DoctorUpdate
from typing import List

from errors.badrequest import BadRequestError
from errors.forbidden import ForbiddenError
from services.token import get_user_by_email, create_token

from schemas.appointment import AppointmentUpdate
from services.appointment import read_appointment, update_appointment


def create_doctor(db: Session, doctor: DoctorCreate) -> Doctor:
    if get_user_by_email(db, doctor.email):
        raise ForbiddenError(f"User: {doctor}. User with this email already exists")
    if doctor.password != doctor.confirm_password:
        raise BadRequestError(f"User: {doctor}. Password and confirm password do not match")
    hashed_password = bcrypt.hash(doctor.password)
    db_doctor = Doctor(
        full_name=doctor.full_name,
        photo_id=0,
        birthday_date=doctor.birthday_date,
        residence=doctor.residence,
        email=doctor.email,
        telephone=doctor.telephone,
        password=hashed_password,
        description=doctor.description,
        work_years=doctor.work_years
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    content = create_token(db, doctor.email, doctor.password)
    content['id'] = db_doctor.id
    return content


def read_doctor(db: Session, doctor_id: int) -> Doctor:
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if db_doctor is None:
        raise ValueError(f"Doctor not found with id {doctor_id}")
    return db_doctor


def read_doctors(db: Session) -> List[Doctor]:
    return db.query(Doctor).all()


def update_doctor(db: Session, doctor_id: int, doctor: DoctorUpdate) -> Doctor:
    db_doctor = read_doctor(db, doctor_id)
    for key, value in doctor.dict(exclude_unset=True).items():
        setattr(db_doctor, key, value)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def delete_doctor(db: Session, doctor_id: int) -> None:
    db_doctor = read_doctor(db, doctor_id)
    db.delete(db_doctor)
    db.commit()


def confirm_appointment(db: Session, appointment_id: int, description: str):
    appointment = read_appointment(db, appointment_id)
    appointment_update = AppointmentUpdate(doctor_id=appointment.doctor_id,
                                           patient_id=appointment.patient_id,
                                           description=description,
                                           appointment_datetime=appointment.appointment_datetime,
                                           doctor_approved=True)
    return update_appointment(db, appointment_id, appointment_update)

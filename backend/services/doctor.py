from passlib.handlers.bcrypt import bcrypt
from sqlalchemy.orm import Session
from db.doctor import Doctor
from schemas.doctor import DoctorCreate, DoctorUpdate
from typing import List

from errors.badrequest import BadRequestError
from errors.forbidden import ForbiddenError
from services.token import get_user_by_email, create_token


def create_doctor(db: Session, doctor: DoctorCreate) -> Doctor:
    if get_user_by_email(db, doctor.email):
        raise ForbiddenError(f"User: {doctor}. User with this email already exists")
    if doctor.password != doctor.confirm_password:
        raise BadRequestError(f"User: {doctor}. Password and confirm password do not match")
    hashed_password = bcrypt.hash(doctor.password)
    db_doctor = Doctor(
        name=doctor.name,
        age=doctor.age,
        email=doctor.email,
        password=hashed_password,
        specialty_id=doctor.specialty_id,
        education_id=doctor.education_id,
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

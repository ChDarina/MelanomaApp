import io
import os
from datetime import datetime
from typing import List

from PIL import Image
from db.patient import Patient
from errors.badrequest import BadRequestError
from errors.forbidden import ForbiddenError
from fastapi import UploadFile
from passlib.handlers.bcrypt import bcrypt
from schemas.appointment import AppointmentCreate
from schemas.patient import PatientCreate, PatientUpdate
from schemas.photo import PhotoCreate
from services.appointment import create_appointment
from services.photo import create_photo
from services.token import get_user_by_email, create_token
from sqlalchemy.orm import Session


def read_patients(db: Session) -> List[Patient]:
    return db.query(Patient).all()


def create_patient(db: Session, patient: PatientCreate) -> Patient:
    if get_user_by_email(db, patient.email):
        raise ForbiddenError(f"User: {patient}. User with this email already exists")
    if patient.password != patient.confirm_password:
        raise BadRequestError(f"User: {patient}. Password and confirm password do not match")
    hashed_password = bcrypt.hash(patient.password)
    db_patient = Patient(
        name=patient.name,
        birthday_date=patient.birthday_date,
        residence=patient.residence,
        telephone=patient.telephone,
        email=patient.email,
        password=hashed_password,
        status_id=1,
        photo_id=10)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    content = create_token(db, patient.email, patient.password)
    return content


def read_patient(db: Session, patient_id: int) -> Patient:
    if db_patient := db.query(Patient).filter(Patient.id == patient_id).first():
        return db_patient
    raise ValueError(f"User not found with id {[patient_id]}")


def update_patient(db: Session, patient_id: int, patient: PatientUpdate) -> Patient:
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if db_patient:
        for key, value in patient.dict(exclude_unset=True).items():
            setattr(db_patient, key, value)
        db.commit()
        db.refresh(db_patient)
        return db_patient
    else:
        raise ValueError(f'Patient with id {patient_id} not found')


def delete_patient(db: Session, patient_id: int) -> Patient:
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if db_patient:
        db.delete(db_patient)
        db.commit()
        return db_patient
    else:
        raise ValueError(f'Patient with id {patient_id} not found')


async def is_image_format(photo: UploadFile):
    try:
        contents = await photo.read()
        img = Image.open(io.BytesIO(contents))
        img.verify()
        return True
    except Exception:
        return False


async def upload(db: Session, user_id: int, file: UploadFile):
    if await is_image_format(file):
        photo_dir = f'{os.getcwd()}/data/{user_id}/photos/'
        exists = os.path.exists(photo_dir)
        if not exists:
            os.makedirs(photo_dir)
        now = datetime.now()
        file_location = f"{photo_dir}{now.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
        with Image.open(file.file) as img:
            img.convert('RGB').save(file_location, 'JPEG')
        photo_schema = PhotoCreate(path=file_location)
        photo = create_photo(db, photo_schema)
        return photo.id
    raise ValueError("File should be an image")


def make_appointment(db: Session, patient_id: int, appointment: AppointmentCreate):
    if patient_id != appointment.patient_id:
        raise BadRequestError("Patient id and appointment patient id do not match")
    return create_appointment(db, appointment)

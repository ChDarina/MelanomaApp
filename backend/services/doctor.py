from datetime import datetime

from passlib.handlers.bcrypt import bcrypt
from sqlalchemy.orm import Session
from db.doctor import Doctor
from schemas.doctor import DoctorCreate, DoctorUpdate, DoctorResponseModel, DoctorsAnswer, DoctorsArticle
from typing import List

from errors.badrequest import BadRequestError
from errors.forbidden import ForbiddenError
from services.token import get_user_by_email, create_token

from schemas.appointment import AppointmentUpdate, AppointmentResponse
from services.appointment import read_appointment, update_appointment

from db.appointment import Appointment
from errors.internalserver import InternalServerError
from schemas.appointment import AppointmentModel, AppointmentApproval

from services.user import read_user

from schemas.answer import AnswerCreate
from services.answer import create_answer

from schemas.article import ArticleCreate
from services.article import create_article


def create_doctor(db: Session, doctor: DoctorCreate) -> Doctor:
    if get_user_by_email(db, doctor.email):
        raise ForbiddenError(f"User: {doctor}. User with this email already exists")
    if doctor.password != doctor.confirm_password:
        raise BadRequestError(f"User: {doctor}. Password and confirm password do not match")
    hashed_password = bcrypt.hash(doctor.password)
    db_doctor = Doctor(
        name=doctor.name,
        photo_id=10,
        birthday_date=doctor.birthday_date,
        residence=doctor.residence,
        email=doctor.email,
        telephone=doctor.telephone,
        password=hashed_password,
        description=doctor.description,
        work_years=doctor.work_years,
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    content = create_token(db, doctor.email, doctor.password)
    return content


def read_doctor(db: Session, doctor_id: int) -> Doctor:
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if db_doctor is None:
        raise ValueError(f"Doctor not found with id {doctor_id}")
    return db_doctor


def read_doctors(db: Session) -> List[DoctorResponseModel]:
    doctors_db = db.query(Doctor).all()
    doctors: List = []
    for doctor_db in doctors_db:
        doctors.append(DoctorResponseModel(id=doctor_db.id,
                                           name=doctor_db.name,
                                           description=doctor_db.description,
                                           work_years=doctor_db.work_years))
    return doctors


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


def approve_decision_appointment(db: Session, appointment_id: int, appointment_approval: AppointmentApproval):
    appointment = read_appointment(db, appointment_id)
    appointment_update = AppointmentUpdate(doctor_id=appointment.doctor_id,
                                           patient_id=appointment.patient_id,
                                           description=appointment_approval.description,
                                           appointment_datetime=appointment.appointment_datetime,
                                           doctor_approved=appointment_approval.doctor_approved)
    return update_appointment(db, appointment_id, appointment_update)


def get_appointments(db: Session, doctor_id):
    try:
        appointments = db.query(Appointment).filter_by(doctor_id=doctor_id).all()
        doctor = read_doctor(db, doctor_id)

        appointment_list = []
        for appointment in appointments:
            dto = AppointmentResponse(
                id=appointment.id, doctor_id=appointment.doctor_id,
                patient_id=appointment.patient_id, description=appointment.description,
                appointment_datetime=appointment.appointment_datetime,
                doctor_approved=appointment.doctor_approved,
                doctor_name=doctor.name,
                patient_name=read_user(db, appointment.patient_id).name
            )
            appointment_list.append(dto)
        return appointment_list
    except Exception as e:
        raise InternalServerError(f"Could not get appointments for doctor with "
                                  f"id = {doctor_id}. Error: {str(e)}")


def get_appointment(db: Session, doctor_id: int, appointment_id: int):
    try:
        appointment = db.query(Appointment).filter_by(id=appointment_id).first()
        if appointment.doctor_id != doctor_id:
            raise ForbiddenError(f"Could not get appointment with id = {appointment_id} for doctor with "
                                 f"id = {doctor_id}. Doctor does not have access for this appointment")
        doctor = read_doctor(db, doctor_id)
        return AppointmentResponse(
            id=appointment.id, doctor_id=doctor_id,
            patient_id=appointment.patient_id, description=appointment.description,
            appointment_datetime=appointment.appointment_datetime,
            doctor_approved=appointment.doctor_approved,
            doctor_name=doctor.name,
            patient_name=read_user(db, appointment.patient_id).name
        )
    except Exception as e:
        raise InternalServerError(f"Could not get appointments for patient with "
                                  f"id = {doctor_id}. Error: {str(e)}")


def publish_answer(db: Session, doctor_id: int, body: DoctorsAnswer):
    question = AnswerCreate(doctor_id=doctor_id,
                            question_id=body.question_id,
                            content=body.content,
                            datetime_created=datetime.now())
    return create_answer(db, question)


def publish_article(db: Session, body: DoctorsArticle):
    article = ArticleCreate(doctor_id=body.doctor_id,
                            title=body.title,
                            content=body.content,
                            datetime_created=datetime.now())
    return create_article(db, article)

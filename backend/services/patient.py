from typing import List
from sqlalchemy.orm import Session
from db.patient import Patient
from schemas.patient import PatientCreate, PatientUpdate


def read_patients(db: Session) -> List[Patient]:
    return db.query(Patient).all()


def create_patient(db: Session, patient: PatientCreate) -> Patient:
    db_patient = Patient(user_id=patient.user_id, status_id=patient.status_id)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


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

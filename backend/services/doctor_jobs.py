from typing import List

from sqlalchemy.orm import Session
from db.doctor_jobs import DoctorJobs

from schemas.doctor_jobs import DoctorJobsCreate, DoctorJobsUpdate


def create_doctor_jobs(db: Session, doctor_jobs: DoctorJobsCreate) -> DoctorJobs:
    db_doctor_jobs = DoctorJobs(
        doctor_id=doctor_jobs.doctor_id,
        work_place_id=doctor_jobs.work_place_id)
    db.add(db_doctor_jobs)
    db.commit()
    db.refresh(db_doctor_jobs)
    return db_doctor_jobs


def read_doctor_jobs(db: Session, doctor_jobs_id: int) -> DoctorJobs:
    db_doctor_jobs = db.query(DoctorJobs).filter(DoctorJobs.id == doctor_jobs_id).first()
    if db_doctor_jobs is None:
        raise ValueError(f"DoctorJobs not found with id {doctor_jobs_id}")
    return db_doctor_jobs


def read_doctors_jobs(db: Session) -> List[DoctorJobs]:
    return db.query(DoctorJobs).all()


def update_doctor_jobs(db: Session, doctor_jobs_id: int, doctor_jobs: DoctorJobsUpdate) -> DoctorJobs:
    db_doctor_jobs = read_doctor_jobs(db, doctor_jobs_id)
    for key, value in doctor_jobs.dict(exclude_unset=True).items():
        setattr(db_doctor_jobs, key, value)
    db.commit()
    db.refresh(db_doctor_jobs)
    return db_doctor_jobs


def delete_doctor_jobs(db: Session, doctor_jobs_id: int) -> None:
    db_doctor_jobs = read_doctor_jobs(db, doctor_jobs_id)
    db.delete(db_doctor_jobs)
    db.commit()

import logging
from typing import List

from db.base import Base, engine, get_db
from fastapi import Depends, HTTPException, APIRouter
from schemas.doctor_jobs import DoctorJobsModel, DoctorJobsCreate, DoctorJobsUpdate
from sqlalchemy.orm import Session
from starlette import status

from services.doctor_jobs import delete_doctor_jobs, update_doctor_jobs, read_doctor_jobs, read_doctors_jobs, create_doctor_jobs

Base.metadata.create_all(engine)

router = APIRouter(prefix="/doctor_jobs",
                   tags=["doctors_jobs"],
                   responses={404: {"description": "DoctorsJobs router not found"}})

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


@router.post("/", response_model=DoctorJobsModel)
def create_doctor_jobs_route(doctor_jobs: DoctorJobsCreate, db: Session = Depends(get_db)):
    try:
        return create_doctor_jobs(db, doctor_jobs)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{doctor_jobs_id}", response_model=DoctorJobsModel)
def get_doctor_jobs_route(doctor_jobs_id: int, db: Session = Depends(get_db)):
    try:
        return read_doctor_jobs(db, doctor_jobs_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[DoctorJobsModel])
def get_doctors_jobs_route(db: Session = Depends(get_db)):
    try:
        return read_doctors_jobs(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{doctor_jobs_id}", response_model=DoctorJobsModel)
def update_doctor_jobs_route(doctor_jobs_id: int, doctor_jobs: DoctorJobsUpdate, db: Session = Depends(get_db)):
    try:
        return update_doctor_jobs(db, doctor_jobs_id, doctor_jobs)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{doctor_jobs_id}")
def delete_doctor_jobs_route(doctor_jobs_id: int, db: Session = Depends(get_db)):
    try:
        delete_doctor_jobs(db, doctor_jobs_id)
        return {"detail": f"DoctorJobs with id {doctor_jobs_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

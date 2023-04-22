import logging
from typing import List

from db.base import Base, engine, get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.patient import PatientCreate, PatientUpdate, PatientModel
from services.patient import create_patient, read_patient, update_patient, delete_patient, read_patients
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

router = APIRouter(prefix="/patient",
                   tags=["patients"],
                   responses={404: {"description": "Patients router not found"}})

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


@router.post("/", response_model=PatientModel)
def create_patient_route(patient: PatientCreate, db: Session = Depends(get_db)):
    try:
        return create_patient(db, patient)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{patient_id}", response_model=PatientModel)
def read_patient_route(patient_id: int, db: Session = Depends(get_db)):
    try:
        return read_patient(db, patient_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[PatientModel])
def read_patients_route(db: Session = Depends(get_db)):
    try:
        return read_patients(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{patient_id}", response_model=PatientModel)
def update_patient_route(patient_id: int, patient: PatientUpdate, db: Session = Depends(get_db)):
    try:
        return update_patient(db, patient_id, patient)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{patient_id}")
def delete_patient_route(patient_id: int, db: Session = Depends(get_db)):
    try:
        delete_patient(db, patient_id)
        return {"detail": f"Patient with id {patient_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

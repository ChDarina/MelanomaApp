import logging
from typing import List

from db.base import Base, engine, get_db
from fastapi import Depends, HTTPException, APIRouter
from schemas.appointment import AppointmentModel, AppointmentCreate, AppointmentUpdate
from sqlalchemy.orm import Session
from starlette import status

from services.appointment import delete_appointment, update_appointment, read_appointment, read_appointments, create_appointment

Base.metadata.create_all(engine)

router = APIRouter(prefix="/appointment",
                   tags=["appointments"],
                   responses={404: {"description": "Appointments router not found"}})

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


@router.post("/", response_model=AppointmentModel)
def create_appointment_route(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    try:
        return create_appointment(db, appointment)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{appointment_id}", response_model=AppointmentModel)
def get_appointment_route(appointment_id: int, db: Session = Depends(get_db)):
    try:
        return read_appointment(db, appointment_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[AppointmentModel])
def get_appointments_route(db: Session = Depends(get_db)):
    try:
        return read_appointments(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{appointment_id}", response_model=AppointmentModel)
def update_appointment_route(appointment_id: int, appointment: AppointmentUpdate, db: Session = Depends(get_db)):
    try:
        return update_appointment(db, appointment_id, appointment)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{appointment_id}")
def delete_appointment_route(appointment_id: int, db: Session = Depends(get_db)):
    try:
        delete_appointment(db, appointment_id)
        return {"detail": f"Appointment with id {appointment_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

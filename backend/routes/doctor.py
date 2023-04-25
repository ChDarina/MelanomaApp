import logging
from typing import List

from db.base import Base, engine, get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.doctor import DoctorCreate, DoctorUpdate, DoctorModel
from services.doctor import create_doctor, read_doctor, update_doctor, delete_doctor, read_doctors
from sqlalchemy.orm import Session

from errors.badrequest import BadRequestError
from errors.forbidden import ForbiddenError

from db.user import User
from services.token import is_correct_user, get_current_user
from starlette.responses import JSONResponse

Base.metadata.create_all(engine)

router = APIRouter(prefix="/doctor",
                   tags=["doctors"],
                   responses={404: {"description": "Doctors router not found"}})

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


@router.post("/")
def create_doctor_route(doctor: DoctorCreate, db: Session = Depends(get_db)):
    try:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=create_doctor(db, doctor))
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{doctor_id}", response_model=DoctorModel)
def read_doctor_route(doctor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    is_correct_user(doctor_id, current_user.id)
    try:
        return read_doctor(db, doctor_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[DoctorModel])
def read_doctors_route(db: Session = Depends(get_db)):
    try:
        return read_doctors(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{doctor_id}", response_model=DoctorModel)
def update_doctor_route(doctor_id: int, doctor: DoctorUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    is_correct_user(doctor_id, current_user.id)
    try:
        return update_doctor(db, doctor_id, doctor)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{doctor_id}")
def delete_doctor_route(doctor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    is_correct_user(doctor_id, current_user.id)
    try:
        delete_doctor(db, doctor_id)
        return {"detail": f"Doctor with id {doctor_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

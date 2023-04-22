import logging
from typing import List

from db.base import Base, engine, get_db
from fastapi import Depends, HTTPException, APIRouter
from schemas.specialty import SpecialtyModel, SpecialtyCreate, SpecialtyUpdate
from sqlalchemy.orm import Session
from starlette import status

from services.specialty import delete_specialty, update_specialty, read_specialty, read_specialties, create_specialty

Base.metadata.create_all(engine)

router = APIRouter(prefix="/specialty",
                   tags=["specialties"],
                   responses={404: {"description": "Specialties router not found"}})

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


@router.post("/", response_model=SpecialtyModel)
def create_specialty_route(specialty: SpecialtyCreate, db: Session = Depends(get_db)):
    try:
        return create_specialty(db, specialty)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{specialty_id}", response_model=SpecialtyModel)
def get_specialty_route(specialty_id: int, db: Session = Depends(get_db)):
    try:
        return read_specialty(db, specialty_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[SpecialtyModel])
def get_specialties_route(db: Session = Depends(get_db)):
    try:
        return read_specialties(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{specialty_id}", response_model=SpecialtyModel)
def update_specialty_route(specialty_id: int, specialty: SpecialtyUpdate, db: Session = Depends(get_db)):
    try:
        return update_specialty(db, specialty_id, specialty)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{specialty_id}")
def delete_specialty_route(specialty_id: int, db: Session = Depends(get_db)):
    try:
        delete_specialty(db, specialty_id)
        return {"detail": f"Specialty with id {specialty_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

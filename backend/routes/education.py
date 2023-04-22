import logging
from typing import List

from db.base import Base, engine, get_db
from fastapi import Depends, HTTPException, APIRouter
from schemas.education import EducationModel, EducationCreate, EducationUpdate
from sqlalchemy.orm import Session
from starlette import status

from services.education import delete_education, update_education, read_education, read_educations, create_education

Base.metadata.create_all(engine)

router = APIRouter(prefix="/education",
                   tags=["educations"],
                   responses={404: {"description": "Educations router not found"}})

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


@router.post("/", response_model=EducationModel)
def create_education_route(education: EducationCreate, db: Session = Depends(get_db)):
    try:
        return create_education(db, education)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{education_id}", response_model=EducationModel)
def get_education_route(education_id: int, db: Session = Depends(get_db)):
    try:
        return read_education(db, education_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[EducationModel])
def get_educations_route(db: Session = Depends(get_db)):
    try:
        return read_educations(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{education_id}", response_model=EducationModel)
def update_education_route(education_id: int, education: EducationUpdate, db: Session = Depends(get_db)):
    try:
        return update_education(db, education_id, education)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{education_id}")
def delete_education_route(education_id: int, db: Session = Depends(get_db)):
    try:
        delete_education(db, education_id)
        return {"detail": f"Education with id {education_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

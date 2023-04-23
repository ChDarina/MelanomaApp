import logging
from typing import List

from db.base import Base, engine, get_db
from fastapi import Depends, HTTPException, APIRouter
from schemas.work_place import WorkPlaceModel, WorkPlaceCreate, WorkPlaceUpdate
from sqlalchemy.orm import Session
from starlette import status

from services.work_place import delete_work_place, update_work_place, read_work_place, read_work_places, create_work_place

Base.metadata.create_all(engine)

router = APIRouter(prefix="/work_place",
                   tags=["work_places"],
                   responses={404: {"description": "WorkPlaces router not found"}})

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


@router.post("/", response_model=WorkPlaceModel)
def create_work_place_route(work_place: WorkPlaceCreate, db: Session = Depends(get_db)):
    try:
        return create_work_place(db, work_place)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{work_place_id}", response_model=WorkPlaceModel)
def get_work_place_route(work_place_id: int, db: Session = Depends(get_db)):
    try:
        return read_work_place(db, work_place_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[WorkPlaceModel])
def get_work_places_route(db: Session = Depends(get_db)):
    try:
        return read_work_places(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{work_place_id}", response_model=WorkPlaceModel)
def update_work_place_route(work_place_id: int, work_place: WorkPlaceUpdate, db: Session = Depends(get_db)):
    try:
        return update_work_place(db, work_place_id, work_place)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{work_place_id}")
def delete_work_place_route(work_place_id: int, db: Session = Depends(get_db)):
    try:
        delete_work_place(db, work_place_id)
        return {"detail": f"WorkPlace with id {work_place_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

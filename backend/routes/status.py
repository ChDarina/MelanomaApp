import logging
from typing import List

from db.base import Base, engine, get_db
from fastapi import Depends, HTTPException, APIRouter
from schemas.status import StatusModel, StatusCreate, StatusUpdate
from sqlalchemy.orm import Session
from starlette import status

from services.status import delete_status, update_status, read_status, read_statuses, create_status

Base.metadata.create_all(engine)

router = APIRouter(prefix="/status",
                   tags=["statuses"],
                   responses={404: {"description": "Statuses router not found"}})

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


@router.post("/", response_model=StatusModel)
def create_status_route(status_entity: StatusCreate, db: Session = Depends(get_db)):
    try:
        return create_status(db, status_entity)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{status_id}", response_model=StatusModel)
def get_status_route(status_id: int, db: Session = Depends(get_db)):
    try:
        return read_status(db, status_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[StatusModel])
def get_statuses_route(db: Session = Depends(get_db)):
    try:
        return read_statuses(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{status_id}", response_model=StatusModel)
def update_status_route(status_id: int, status_entity: StatusUpdate, db: Session = Depends(get_db)):
    try:
        return update_status(db, status_id, status_entity)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{status_id}")
def delete_status_route(status_id: int, db: Session = Depends(get_db)):
    try:
        delete_status(db, status_id)
        return {"detail": f"Status with id {status_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

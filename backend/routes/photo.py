import logging
from typing import List

from db.base import Base, engine, get_db
from fastapi import Depends, HTTPException, APIRouter
from schemas.photo import PhotoModel, PhotoCreate, PhotoUpdate
from sqlalchemy.orm import Session
from starlette import status

from services.photo import delete_photo, update_photo, read_photo, read_photos, create_photo

Base.metadata.create_all(engine)

router = APIRouter(prefix="/photo",
                   tags=["photos"],
                   responses={404: {"description": "Photos router not found"}})

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


@router.post("/", response_model=PhotoModel)
def create_photo_route(photo: PhotoCreate, db: Session = Depends(get_db)):
    try:
        return create_photo(db, photo)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{photo_id}", response_model=PhotoModel)
def get_photo_route(photo_id: int, db: Session = Depends(get_db)):
    try:
        return read_photo(db, photo_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[PhotoModel])
def get_photos_route(db: Session = Depends(get_db)):
    try:
        return read_photos(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{photo_id}", response_model=PhotoModel)
def update_photo_route(photo_id: int, photo: PhotoUpdate, db: Session = Depends(get_db)):
    try:
        return update_photo(db, photo_id, photo)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{photo_id}")
def delete_photo_route(photo_id: int, db: Session = Depends(get_db)):
    try:
        delete_photo(db, photo_id)
        return {"detail": f"Photo with id {photo_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

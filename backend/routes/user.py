import logging
from typing import List

from db.base import Base, engine, get_db
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from schemas.user import UserCreate, UserUpdate, UserModel
from services.user import create_user, read_user, update_user, delete_user, read_users
from sqlalchemy.orm import Session

from services.user import upload

Base.metadata.create_all(engine)

router = APIRouter(prefix="/user",
                   tags=["users"],
                   responses={404: {"description": "Users router not found"}})

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


@router.post("/", response_model=UserModel)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{user_id}", response_model=UserModel)
def read_user_route(user_id: int, db: Session = Depends(get_db)):
    try:
        return read_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[UserModel])
def read_users_route(db: Session = Depends(get_db)):
    try:
        return read_users(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{user_id}", response_model=UserModel)
def update_user_route(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        return update_user(db, user_id, user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    try:
        delete_user(db, user_id)
        return {"detail": f"User with id {user_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{user_id}/upload")
def upload_photo_route(user_id: int, file: UploadFile, db: Session = Depends(get_db)):
    try:
        return upload(db, user_id, file)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

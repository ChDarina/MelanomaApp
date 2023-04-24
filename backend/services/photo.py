from typing import List

from db.photo import Photo
from schemas.photo import PhotoCreate, PhotoUpdate
from sqlalchemy.orm import Session


def create_photo(db: Session, photo: PhotoCreate) -> Photo:
    db_photo = Photo(path=photo.path)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo


def read_photo(db: Session, photo_id: int) -> Photo:
    db_photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if db_photo is None:
        raise ValueError(f"Photo not found with id {photo_id}")
    return db_photo


def read_photos(db: Session) -> List[Photo]:
    return db.query(Photo).all()


def update_photo(db: Session, photo_id: int, photo: PhotoUpdate) -> Photo:
    db_photo = read_photo(db, photo_id)
    for key, value in photo.dict(exclude_unset=True).items():
        setattr(db_photo, key, value)
    db.commit()
    db.refresh(db_photo)
    return db_photo


def delete_photo(db: Session, photo_id: int) -> None:
    db_photo = read_photo(db, photo_id)
    db.delete(db_photo)
    db.commit()

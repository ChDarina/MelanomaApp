import io
import os
from datetime import datetime

from PIL import Image
from fastapi import UploadFile
from sqlalchemy.orm import Session
from db.user import User
from schemas.user import UserCreate, UserUpdate
from typing import List

from schemas.photo import PhotoCreate

from services.photo import create_photo


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        name=user.name,
        age=user.age,
        email=user.email,
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def read_user(db: Session, user_id: int) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise ValueError(f"User not found with id {user_id}")
    return db_user


def read_users(db: Session) -> List[User]:
    return db.query(User).all()


def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
    db_user = read_user(db, user_id)
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> None:
    db_user = read_user(db, user_id)
    db.delete(db_user)
    db.commit()


async def is_image_format(photo: UploadFile):
    try:
        contents = await photo.read()
        img = Image.open(io.BytesIO(contents))
        img.verify()
        return True
    except Exception:
        return False


def upload(db: Session, user_id: int, file: UploadFile):
    if is_image_format(file):
        photo_dir = f'{os.getcwd()}/{user_id}/photos/'
        exists = os.path.exists(photo_dir)
        if not exists:
            os.makedirs(photo_dir)
        now = datetime.now()
        file_location = f"{photo_dir}{now.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
        with Image.open(file.file) as img:
            img.convert('RGB').save(file_location, 'JPEG')
        photo_schema = PhotoCreate(path=file_location)
        return create_photo(db, photo_schema)
    raise ValueError("Файл должен быть изображением")

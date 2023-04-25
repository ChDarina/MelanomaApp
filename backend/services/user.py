from typing import List

from db.user import User
from passlib.handlers.bcrypt import bcrypt
from schemas.user import UserCreate, UserUpdate
from sqlalchemy.orm import Session

from errors.badrequest import BadRequestError
from errors.forbidden import ForbiddenError
from services.token import get_user_by_email, create_token


def create_user(db: Session, user: UserCreate) -> User:
    if get_user_by_email(user.email):
        return ForbiddenError(f"User: {user}. User with this email already exists")
    if user.password != user.confirm_password:
        raise BadRequestError(f"User: {user}. Password and confirm password do not match")
    hashed_password = bcrypt.hash(user.password)
    db_user = User(
        name=user.name,
        age=user.age,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    content = create_token(user.email, user.password)
    content['id'] = user.id
    return content


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

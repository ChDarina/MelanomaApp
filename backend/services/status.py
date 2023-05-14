from typing import List

from sqlalchemy.orm import Session
from db.status import Status

from schemas.status import StatusCreate, StatusUpdate


def create_status(db: Session, status: StatusCreate) -> Status:
    db_status = Status(name=status.name)
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status


def read_status(db: Session, status_id: int) -> Status:
    db_status = db.query(Status).filter(Status.id == status_id).first()
    if db_status is None:
        raise ValueError(f"Status not found with id {status_id}")
    return db_status


def read_healthy_status(db: Session):
    db_status = db.query(Status).filter(Status.name.lower() == 'здоров').first()
    if db_status is None:
        status_create = StatusCreate(name='здоров')
        return create_status(db, status_create)
    return db_status


def read_status_by_name(db: Session, status_name: str) -> Status:
    return db.query(Status).filter(Status.name == status_name).first()


def read_statuses(db: Session) -> List[Status]:
    return db.query(Status).all()


def update_status(db: Session, status_id: int, status: StatusUpdate) -> Status:
    db_status = read_status(db, status_id)
    for key, value in status.dict(exclude_unset=True).items():
        setattr(db_status, key, value)
    db.commit()
    db.refresh(db_status)
    return db_status


def delete_status(db: Session, status_id: int) -> None:
    db_status = read_status(db, status_id)
    db.delete(db_status)
    db.commit()

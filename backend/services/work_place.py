from typing import List

from sqlalchemy.orm import Session
from db.work_place import WorkPlace

from schemas.work_place import WorkPlaceCreate, WorkPlaceUpdate


def create_work_place(db: Session, work_place: WorkPlaceCreate) -> WorkPlace:
    db_work_place = WorkPlace(
        company_id=work_place.company_id,
        start_date=work_place.start_date,
        end_date=work_place.end_date,
        description=work_place.description
    )
    db.add(db_work_place)
    db.commit()
    db.refresh(db_work_place)
    return db_work_place


def read_work_place(db: Session, work_place_id: int) -> WorkPlace:
    db_work_place = db.query(WorkPlace).filter(WorkPlace.id == work_place_id).first()
    if db_work_place is None:
        raise ValueError(f"WorkPlace not found with id {work_place_id}")
    return db_work_place


def read_work_places(db: Session) -> List[WorkPlace]:
    return db.query(WorkPlace).all()


def update_work_place(db: Session, work_place_id: int, work_place: WorkPlaceUpdate) -> WorkPlace:
    db_work_place = read_work_place(db, work_place_id)
    for key, value in work_place.dict(exclude_unset=True).items():
        setattr(db_work_place, key, value)
    db.commit()
    db.refresh(db_work_place)
    return db_work_place


def delete_work_place(db: Session, work_place_id: int) -> None:
    db_work_place = read_work_place(db, work_place_id)
    db.delete(db_work_place)
    db.commit()

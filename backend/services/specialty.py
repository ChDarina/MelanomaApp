from typing import List

from sqlalchemy.orm import Session
from db.specialty import Specialty

from schemas.specialty import SpecialtyCreate, SpecialtyUpdate


def create_specialty(db: Session, specialty: SpecialtyCreate) -> Specialty:
    db_specialty = Specialty(name=specialty.name)
    db.add(db_specialty)
    db.commit()
    db.refresh(db_specialty)
    return db_specialty


def read_specialty(db: Session, specialty_id: int) -> Specialty:
    db_specialty = db.query(Specialty).filter(Specialty.id == specialty_id).first()
    if db_specialty is None:
        raise ValueError(f"Specialty not found with id {specialty_id}")
    return db_specialty


def read_specialties(db: Session) -> List[Specialty]:
    return db.query(Specialty).all()


def update_specialty(db: Session, specialty_id: int, specialty: SpecialtyUpdate) -> Specialty:
    db_specialty = read_specialty(db, specialty_id)
    for key, value in specialty.dict(exclude_unset=True).items():
        setattr(db_specialty, key, value)
    db.commit()
    db.refresh(db_specialty)
    return db_specialty


def delete_specialty(db: Session, specialty_id: int) -> None:
    db_specialty = read_specialty(db, specialty_id)
    db.delete(db_specialty)
    db.commit()

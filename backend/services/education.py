from typing import List

from sqlalchemy.orm import Session
from db.education import Education

from schemas.education import EducationCreate, EducationUpdate


def create_education(db: Session, education: EducationCreate) -> Education:
    db_education = Education(name=education.name)
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education


def read_education(db: Session, education_id: int) -> Education:
    db_education = db.query(Education).filter(Education.id == education_id).first()
    if db_education is None:
        raise ValueError(f"Education not found with id {education_id}")
    return db_education


def read_educations(db: Session) -> List[Education]:
    return db.query(Education).all()


def update_education(db: Session, education_id: int, education: EducationUpdate) -> Education:
    db_education = read_education(db, education_id)
    for key, value in education.dict(exclude_unset=True).items():
        setattr(db_education, key, value)
    db.commit()
    db.refresh(db_education)
    return db_education


def delete_education(db: Session, education_id: int) -> None:
    db_education = read_education(db, education_id)
    db.delete(db_education)
    db.commit()

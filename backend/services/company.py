from typing import List

from sqlalchemy.orm import Session
from db.company import Company

from schemas.company import CompanyCreate, CompanyUpdate


def create_company(db: Session, company: CompanyCreate) -> Company:
    db_company = Company(name=company.name)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def read_company(db: Session, company_id: int) -> Company:
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if db_company is None:
        raise ValueError(f"Company not found with id {company_id}")
    return db_company


def read_companies(db: Session) -> List[Company]:
    return db.query(Company).all()


def update_company(db: Session, company_id: int, company: CompanyUpdate) -> Company:
    db_company = read_company(db, company_id)
    for key, value in company.dict(exclude_unset=True).items():
        setattr(db_company, key, value)
    db.commit()
    db.refresh(db_company)
    return db_company


def delete_company(db: Session, company_id: int) -> None:
    db_company = read_company(db, company_id)
    db.delete(db_company)
    db.commit()

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.base import get_db
from db.company import Company

router = APIRouter()


@router.get('/companies')
def get_companies(db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    return companies

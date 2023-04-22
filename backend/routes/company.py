import logging
from typing import List

from db.base import Base, engine, get_db
from fastapi import Depends, HTTPException, APIRouter
from schemas.company import CompanyModel, CompanyCreate, CompanyUpdate
from sqlalchemy.orm import Session
from starlette import status

from services.company import delete_company, update_company, read_company, read_companies, create_company

Base.metadata.create_all(engine)

router = APIRouter(prefix="/company",
                   tags=["companies"],
                   responses={404: {"description": "Compainies router not found"}})

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


@router.post("/", response_model=CompanyModel)
def create_company_route(company: CompanyCreate, db: Session = Depends(get_db)):
    try:
        return create_company(db, company)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{company_id}", response_model=CompanyModel)
def get_company_route(company_id: int, db: Session = Depends(get_db)):
    try:
        return read_company(db, company_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[CompanyModel])
def get_companies_route(db: Session = Depends(get_db)):
    try:
        return read_companies(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{company_id}", response_model=CompanyModel)
def update_company_route(company_id: int, company: CompanyUpdate, db: Session = Depends(get_db)):
    try:
        return update_company(db, company_id, company)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{company_id}")
def delete_company_route(company_id: int, db: Session = Depends(get_db)):
    try:
        delete_company(db, company_id)
        return {"detail": f"Company with id {company_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

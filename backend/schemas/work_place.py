from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class WorkPlaceModel(BaseModel):
    id: int
    company_id: int
    start_date: date
    end_date: Optional[date]
    description: Optional[str]

    class Config:
        orm_mode = True


class WorkPlaceCreate(BaseModel):
    company_id: int
    start_date: date
    end_date: Optional[date]
    description: Optional[str]


class WorkPlaceUpdate(BaseModel):
    company_id: int
    start_date: date
    end_date: Optional[date]
    description: Optional[str]

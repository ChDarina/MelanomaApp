from datetime import datetime

from pydantic import BaseModel


class PredictSessionModel(BaseModel):
    id: int
    patient_id: int
    photo_id: int
    predict_score: float
    start_datetime: datetime

    class Config:
        orm_mode = True


class PredictSessionCreate(BaseModel):
    patient_id: int
    photo_id: int
    predict_score: float
    start_datetime: datetime


class PredictSessionUpdate(BaseModel):
    photo_id: int
    predict_score: float
    start_datetime: datetime

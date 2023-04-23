from typing import List

from sqlalchemy.orm import Session
from db.predict_session import PredictSession

from schemas.predict_session import PredictSessionCreate, PredictSessionUpdate


def create_predict_session(db: Session, predict_session: PredictSessionCreate) -> PredictSession:
    db_predict_session = PredictSession(
        patient_id=predict_session.patient_id,
        photo_id=predict_session.photo_id,
        predict_score=predict_session.predict_score,
        start_datetime=predict_session.start_datetime)
    db.add(db_predict_session)
    db.commit()
    db.refresh(db_predict_session)
    return db_predict_session


def read_predict_session(db: Session, predict_session_id: int) -> PredictSession:
    db_predict_session = db.query(PredictSession).filter(PredictSession.id == predict_session_id).first()
    if db_predict_session is None:
        raise ValueError(f"PredictSession not found with id {predict_session_id}")
    return db_predict_session


def read_predict_sessions(db: Session) -> List[PredictSession]:
    return db.query(PredictSession).all()


def update_predict_session(db: Session, predict_session_id: int, predict_session: PredictSessionUpdate) -> \
        PredictSession:
    db_predict_session = read_predict_session(db, predict_session_id)
    for key, value in predict_session.dict(exclude_unset=True).items():
        setattr(db_predict_session, key, value)
    db.commit()
    db.refresh(db_predict_session)
    return db_predict_session


def delete_predict_session(db: Session, predict_session_id: int) -> None:
    db_predict_session = read_predict_session(db, predict_session_id)
    db.delete(db_predict_session)
    db.commit()

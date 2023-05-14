import logging
from typing import List

from db.base import Base, engine, get_db
from fastapi import Depends, HTTPException, APIRouter
from schemas.predict_session import PredictSessionModel, PredictSessionCreate, PredictSessionUpdate
from sqlalchemy.orm import Session
from starlette import status

from services.predict_session import delete_predict_session, update_predict_session, read_predict_session, \
    read_predict_sessions, create_predict_session

from services.predict_session import predict

Base.metadata.create_all(engine)

router = APIRouter(prefix="/predict_session",
                   tags=["predict_sessions"],
                   responses={404: {"description": "PredictSessions router not found"}})

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


@router.post("/", response_model=PredictSessionModel)
def create_predict_session_route(predict_session: PredictSessionCreate, db: Session = Depends(get_db)):
    try:
        return create_predict_session(db, predict_session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{predict_session_id}", response_model=PredictSessionModel)
def get_predict_session_route(predict_session_id: int, db: Session = Depends(get_db)):
    try:
        return read_predict_session(db, predict_session_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[PredictSessionModel])
def get_predict_sessions_route(db: Session = Depends(get_db)):
    try:
        return read_predict_sessions(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{predict_session_id}", response_model=PredictSessionModel)
def update_predict_session_route(predict_session_id: int, predict_session: PredictSessionUpdate,
                                 db: Session = Depends(get_db)):
    try:
        return update_predict_session(db, predict_session_id, predict_session)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{predict_session_id}")
def delete_predict_session_route(predict_session_id: int, db: Session = Depends(get_db)):
    try:
        delete_predict_session(db, predict_session_id)
        return {"detail": f"PredictSession with id {predict_session_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{predict_session_id}/predict")
def predict_route(predict_session_id: int, db: Session = Depends(get_db)):
    try:
        return predict(db, predict_session_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

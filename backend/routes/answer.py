import logging
from typing import List

from db.base import Base, engine, get_db
from fastapi import Depends, HTTPException, APIRouter
from schemas.answer import AnswerModel, AnswerCreate, AnswerUpdate, AnswerResponse
from sqlalchemy.orm import Session
from starlette import status

from services.answer import delete_answer, update_answer, read_answer, read_answers, create_answer

Base.metadata.create_all(engine)

router = APIRouter(prefix="/answer",
                   tags=["answers"],
                   responses={404: {"description": "Answers router not found"}})

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


@router.post("/", response_model=AnswerModel)
def create_answer_route(answer: AnswerCreate, db: Session = Depends(get_db)):
    try:
        return create_answer(db, answer)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{answer_id}", response_model=AnswerResponse)
def get_answer_route(answer_id: int, db: Session = Depends(get_db)):
    try:
        return read_answer(db, answer_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[AnswerResponse])
def get_answers_route(db: Session = Depends(get_db)):
    try:
        return read_answers(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{answer_id}", response_model=AnswerModel)
def update_answer_route(answer_id: int, answer: AnswerUpdate, db: Session = Depends(get_db)):
    try:
        return update_answer(db, answer_id, answer)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{answer_id}")
def delete_answer_route(answer_id: int, db: Session = Depends(get_db)):
    try:
        delete_answer(db, answer_id)
        return {"detail": f"Answer with id {answer_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

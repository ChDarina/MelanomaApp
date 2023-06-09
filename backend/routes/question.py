import logging
from typing import List

from db.base import Base, engine, get_db
from fastapi import Depends, HTTPException, APIRouter
from schemas.question import QuestionModel, QuestionCreate, QuestionUpdate, QuestionResponse
from sqlalchemy.orm import Session
from starlette import status

from services.question import delete_question, update_question, read_question, read_questions, create_question, \
    get_question_answers

from schemas.answer import AnswerResponse

Base.metadata.create_all(engine)

router = APIRouter(prefix="/question",
                   tags=["questions"],
                   responses={404: {"description": "Questions router not found"}})

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


@router.post("/", response_model=QuestionModel)
def create_question_route(question: QuestionCreate, db: Session = Depends(get_db)):
    try:
        return create_question(db, question)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question_route(question_id: int, db: Session = Depends(get_db)):
    try:
        return read_question(db, question_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[QuestionResponse])
def get_questions_route(db: Session = Depends(get_db)):
    try:
        return read_questions(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{question_id}", response_model=QuestionModel)
def update_question_route(question_id: int, question: QuestionUpdate, db: Session = Depends(get_db)):
    try:
        return update_question(db, question_id, question)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{question_id}")
def delete_question_route(question_id: int, db: Session = Depends(get_db)):
    try:
        delete_question(db, question_id)
        return {"detail": f"Question with id {question_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{question_id}/answers", response_model=List[AnswerResponse])
def get_answers_route(question_id: int, db: Session = Depends(get_db)):
    return get_question_answers(db, question_id)

from typing import List

from sqlalchemy.orm import Session
from db.answer import Answer

from schemas.answer import AnswerCreate, AnswerUpdate


def create_answer(db: Session, answer: AnswerCreate) -> Answer:
    db_answer = Answer(doctor_id=answer.doctor_id,
                       question_id=answer.question_id,
                       content=answer.content,
                       datetime_created=answer.datetime_created)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def read_answer(db: Session, answer_id: int) -> Answer:
    db_answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if db_answer is None:
        raise ValueError(f"Answer not found with id {answer_id}")
    return db_answer


def read_answers(db: Session) -> List[Answer]:
    return db.query(Answer).all()


def update_answer(db: Session, answer_id: int, answer: AnswerUpdate) -> Answer:
    db_answer = read_answer(db, answer_id)
    for key, value in answer.dict(exclude_unset=True).items():
        setattr(db_answer, key, value)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def delete_answer(db: Session, answer_id: int) -> None:
    db_answer = read_answer(db, answer_id)
    db.delete(db_answer)
    db.commit()

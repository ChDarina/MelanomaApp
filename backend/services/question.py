from typing import List

from sqlalchemy.orm import Session
from db.question import Question

from schemas.question import QuestionCreate, QuestionUpdate

from db.answer import Answer


def create_question(db: Session, question: QuestionCreate) -> Question:
    db_question = Question(patient_id=question.patient_id,
                           title=question.title,
                           content=question.content,
                           datetime_created=question.datetime_created)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def read_question(db: Session, question_id: int) -> Question:
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question is None:
        raise ValueError(f"Question not found with id {question_id}")
    return db_question


def read_questions(db: Session) -> List[Question]:
    return db.query(Question).all()


def update_question(db: Session, question_id: int, question: QuestionUpdate) -> Question:
    db_question = read_question(db, question_id)
    for key, value in question.dict(exclude_unset=True).items():
        setattr(db_question, key, value)
    db.commit()
    db.refresh(db_question)
    return db_question


def delete_question(db: Session, question_id: int) -> None:
    db_question = read_question(db, question_id)
    db.delete(db_question)
    db.commit()


def get_question_answers(db: Session, question_id: int) -> List[Answer]:
    return db.query(Answer).filter(Answer.id == question_id).all()

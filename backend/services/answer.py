from typing import List

from sqlalchemy.orm import Session
from db.answer import Answer

from schemas.answer import AnswerCreate, AnswerUpdate, AnswerResponse
from services.doctor import read_doctor


def create_answer(db: Session, answer: AnswerCreate) -> Answer:
    db_answer = Answer(doctor_id=answer.doctor_id,
                       question_id=answer.question_id,
                       content=answer.content,
                       datetime_created=answer.datetime_created)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def read_answer(db: Session, answer_id: int) -> AnswerResponse:
    db_answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if db_answer is None:
        raise ValueError(f"Answer not found with id {answer_id}")
    doctor = read_doctor(db, db_answer.doctor_id)
    return AnswerResponse(
        id=db_answer.id,
        doctor_id=db_answer.doctor_id,
        doctor_name=doctor.name,
        work_years=doctor.work_years,
        question_id=db_answer.question_id,
        content=db_answer.content,
        datetime_created=db_answer.datetime_created)


def read_answers(db: Session) -> List[AnswerResponse]:
    db_answers = db.query(Answer).all()
    response: List[AnswerResponse] = []
    for db_answer in db_answers:
        doctor = read_doctor(db, db_answer.doctor_id)
        response.append(AnswerResponse(
            id=db_answer.id,
            doctor_id=db_answer.doctor_id,
            doctor_name=doctor.name,
            work_years=doctor.work_years,
            question_id=db_answer.question_id,
            content=db_answer.content,
            datetime_created=db_answer.datetime_created))
    return response


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

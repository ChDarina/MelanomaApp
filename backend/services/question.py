from typing import List

from db.answer import Answer
from db.question import Question
from schemas.question import QuestionCreate, QuestionUpdate, QuestionResponse
from sqlalchemy.orm import Session

from db.patient import Patient

from db.doctor import Doctor
from schemas.answer import AnswerResponse


def create_question(db: Session, question: QuestionCreate) -> Question:
    db_question = Question(patient_id=question.patient_id,
                           title=question.title,
                           content=question.content,
                           datetime_created=question.datetime_created)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def read_question(db: Session, question_id: int) -> QuestionResponse:
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question is None:
        raise ValueError(f"Question not found with id {question_id}")
    patient = db.query(Patient).filter(Patient.id == db_question.patient_id).first()
    return QuestionResponse(
        id=db_question.id,
        patient_id=db_question.patient_id,
        patient_name=patient.name,
        answers_count=len(get_question_answers(db, db_question.id)),
        title=db_question.title,
        content=db_question.content,
        datetime_created=db_question.datetime_created)


def read_questions(db: Session) -> List[QuestionResponse]:
    db_questions = db.query(Question).all()
    response: List[QuestionResponse] = []
    for db_question in db_questions:
        patient = db.query(Patient).filter(Patient.id == db_question.patient_id).first()
        response.append(QuestionResponse(
            id=db_question.id,
            patient_id=db_question.patient_id,
            patient_name=patient.name,
            answers_count=len(get_question_answers(db, db_question.id)),
            title=db_question.title,
            content=db_question.content,
            datetime_created=db_question.datetime_created))
    return response


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


def get_question_answers(db: Session, question_id: int) -> List[AnswerResponse]:
    db_answers = db.query(Answer).filter(Answer.id == question_id).all()
    response: List[Answer] = []
    for db_answer in db_answers:
        doctor = db.query(Doctor).filter(Doctor.id == db_answer.doctor_id).first()
        response.append(AnswerResponse(
            id=db_answer.id,
            title=db_answer.title,
            doctor_id=db_answer.doctor_id,
            doctor_name=doctor.name,
            work_years=doctor.work_years,
            question_id=db_answer.question_id,
            content=db_answer.content,
            datetime_created=db_answer.datetime_created))
    return response

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from db.base import Base, engine


class Answer(Base):
    __tablename__ = 'Answer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    doctor_id = Column(Integer, ForeignKey('Doctor.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('Question.id'), nullable=False)
    content = Column(String(1000), nullable=False)
    datetime_created = Column(DateTime, nullable=False)

    doctor = relationship('Doctor')
    question = relationship('Question')


from db.base import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship


class Question(Base):
    __tablename__ = 'Question'

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('Patient.id'), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    datetime_created = Column(DateTime, nullable=False)

    patient = relationship('Patient')


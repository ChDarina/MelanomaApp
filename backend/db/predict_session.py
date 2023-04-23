from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base, engine


class PredictSession(Base):
    __tablename__ = 'PredictSession'

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('Patient.id'), nullable=False)
    photo_id = Column(Integer, ForeignKey('Photo.id'), nullable=False)
    predict_score = Column(Float, nullable=False)
    start_datetime = Column(DateTime, nullable=False)

    patient = relationship('Patient')
    photo = relationship('Photo', uselist=False)


# create the table in the database
Base.metadata.create_all(engine)

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base, engine
from photo import Photo


class PredictSession(Base):
    __tablename__ = 'PredictSession'

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('Patient.id'), nullable=False)
    photo_id = Column(Integer, ForeignKey('Photo.id'), nullable=False)
    predict_score = Column(Float, nullable=False)
    datetime = Column(DateTime, nullable=False)

    patient = relationship('Patient')
    photo = relationship('Photo', uselist=False, back_populates='predict_session')


# create the table in the database
Base.metadata.create_all(engine)

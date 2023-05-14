from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean

from db.base import Base, engine


class Appointment(Base):
    __tablename__ = 'Appointment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey('Doctor.id'))
    patient_id = Column(Integer, ForeignKey('Patient.id'))
    description = Column(String(255), nullable=False)
    appointment_datetime = Column(DateTime, nullable=False)
    doctor_approved = Column(Boolean, nullable=True)
